from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text, _utcnow


class QuizRepository:
    def __init__(self, database: "SQLAlchemy"):
        self.database = database

    def get_all_quizzes(self):
        query_string = "SELECT * FROM quiz;"
        cursor = self.database.session.execute(_text(query_string))
        return cursor.fetchall()

    def get_quiz_by_id(self, quiz_id):
        query_string = "SELECT * FROM quiz WHERE id = :id"
        cursor = self.database.session.execute(_text(query_string), {"id": quiz_id})
        quizzes = cursor.fetchall()
        if len(quizzes) == 0:
            return None
        return quizzes[0]

    def get_full_quiz_by_id(self, quiz_id):
        """Parameters: (int) quiz_id

        Returns: quiz joined with questions and their answers
        """
        query_string = """
            SELECT
                q.id as quiz_id,
                q.*,
                qu.id as question_id,
                qu.*,
                a.id as answer_id,
                a.*,
                qz.username
            FROM quiz q
            LEFT JOIN quiz_question qq ON qq.quiz_id = q.id
            LEFT JOIN quizuser qz ON qz.id = q.quizuser_id
            LEFT JOIN question qu ON qq.question_id = qu.id
            LEFT JOIN question_answer qa ON qa.question_id = qu.id
            LEFT JOIN answer a ON qa.answer_id = a.id
            WHERE q.id = :id;
        """
        cursor = self.database.session.execute(_text(query_string), {"id": quiz_id})
        return cursor.fetchall()

    def get_user_full_quiz_by_id(self, quiz_id, user_id):
        """Parameters:
            (int) quiz_id
            (int) user_id

        Returns: quiz joined with questions and their answers
        only if that quiz was created by the user.
        """
        query_string = """
            SELECT
                q.id as quiz_id,
                q.*,
                qu.id as question_id,
                qu.*,
                a.id as answer_id,
                a.*,
                qz.username
            FROM quiz q
            LEFT JOIN quiz_question qq ON qq.quiz_id = q.id
            LEFT JOIN quizuser qz ON qz.id = q.quizuser_id
            LEFT JOIN question qu ON qq.question_id = qu.id
            LEFT JOIN question_answer qa ON qa.question_id = qu.id
            LEFT JOIN answer a ON qa.answer_id = a.id
            WHERE q.id = :id AND q.quizuser_id = :quizuser_id;
        """
        cursor = self.database.session.execute(
            _text(query_string), {"id": quiz_id, "quizuser_id": user_id}
        )
        return cursor.fetchall()

    def get_quiz_by_id_attach_user(self, quiz_id):
        query_string = """
            SELECT q.*, qu.username as quiz_creator FROM quiz q
            JOIN quizuser qu ON qu.id = q.quizuser_id
            WHERE q.id = :id;
        """
        cursor = self.database.session.execute(_text(query_string), {"id": quiz_id})
        quizzes = cursor.fetchall()
        if len(quizzes) == 0:
            return None
        return quizzes[0]

    def create_new_quiz(self, user_id: int, title: str, description: str):
        query_string = """
            INSERT INTO quiz (title, quiz_description, quizuser_id, created_at)
            VALUES (:title, :quiz_description, :quizuser_id, :created_at)
            RETURNING id;
        """
        cursor = self.database.session.execute(
            _text(query_string),
            {
                "title": title,
                "quiz_description": description,
                "quizuser_id": user_id,
                "created_at": _utcnow(),
            },
        )
        self.database.session.commit()
        (quiz_id,) = cursor.fetchone()
        return quiz_id

    def update_quiz(self, quiz_id: int, title: str, description: str, user_id: int):
        query_string = """
            UPDATE quiz
            SET title = :title,
                quiz_description = :quiz_description,
                updated_at = :updated_at
            WHERE id = :id AND quizuser_id = :quizuser_id
        """
        cursor = self.database.session.execute(
            _text(query_string),
            {
                "id": quiz_id,
                "quizuser_id": user_id,
                "title": title,
                "quiz_description": description,
                "updated_at": _utcnow(),
            },
        )
        self.database.session.commit()
        return cursor.rowcount

    def get_quiz_instances(self, user_id: int, quiz_id: int, only_active=True):
        query_string = """
            SELECT * FROM quiz_instance
            WHERE quizuser_id = :quizuser_id
            AND quiz_id = :quiz_id;
        """
        if only_active:
            query_string = """
                SELECT * FROM quiz_instance
                WHERE quizuser_id = :quizuser_id
                AND quiz_id = :quiz_id
                AND finished_at IS NULL;
            """
        cursor = self.database.session.execute(
            _text(query_string), {"quizuser_id": user_id, "quiz_id": quiz_id}
        )
        return cursor.fetchall()

    def get_quiz_instance_progress(self, quiz_instance_id: int, quizuser_id: int):
        """Parameters: (int) quiz_instance_id

        Returns: quiz instance rows with all questions and question instances
        """
        query_string = """
            SELECT
                qi.*,
                qq.*,
                qui.id as question_instance_id,
                qui.question_id as qui_question_id,
                qui.answer_id,
                qui.answered_at
            FROM quiz_instance qi
            LEFT JOIN quiz_question qq ON qq.quiz_id = qi.quiz_id
            LEFT JOIN question_instance qui ON qui.quiz_instance_id = qi.id AND qui.question_id = qq.question_id
            WHERE qi.id = :id AND qi.quizuser_id = :quizuser_id
            ORDER BY question_id ASC;
        """
        cursor = self.database.session.execute(
            _text(query_string), {"id": quiz_instance_id, "quizuser_id": quizuser_id}
        )
        return cursor.fetchall()

    def get_quiz_instance_by_id(self, quiz_instance_id: int):
        query_string = "SELECT * FROM quiz_instance WHERE id = :id"
        cursor = self.database.session.execute(
            _text(query_string), {"id": quiz_instance_id}
        )
        instances = cursor.fetchall()
        if len(instances) == 0:
            return None
        return instances[0]

    def create_new_quiz_instance(self, user_id: int, quiz_id: int):
        query_string = """
            INSERT INTO quiz_instance (quizuser_id, quiz_id, started_at)
            VALUES (:quizuser_id, :quiz_id, :started_at)
            RETURNING id;
        """
        cursor = self.database.session.execute(
            _text(query_string),
            {"quizuser_id": user_id, "quiz_id": quiz_id, "started_at": _utcnow()},
        )
        self.database.session.commit()
        (quiz_instance_id,) = cursor.fetchone()
        return quiz_instance_id

    def complete_quiz_instance(self, quiz_instance_id: int):
        query_string = """
            UPDATE quiz_instance
            SET finished_at = :finished_at
            WHERE id = :id;
        """
        cursor = self.database.session.execute(
            _text(query_string), {"finished_at": _utcnow(), "id": quiz_instance_id}
        )
        self.database.session.commit()
        return cursor.rowcount

    def get_quiz_instance_stats(self, quiz_instance_id: int, user_id: int):
        query_string = """
            SELECT
                quiz.title,
                quiz.quiz_description,
                quiz.public,
                qi.started_at,
                qi.finished_at,
                q.question_name,
                a.answer_text,
                a.is_correct,
                qui.answered_at
            FROM quiz_instance qi
            LEFT JOIN quiz ON quiz.id = qi.quiz_id
            LEFT JOIN question_instance qui ON qi.id = qui.quiz_instance_id
            LEFT JOIN question q ON q.id = qui.question_id
            LEFT JOIN answer a ON a.id = qui.answer_id
            WHERE qi.quizuser_id = :quizuser_id AND qi.id = :id;
        """
        cursor = self.database.session.execute(
            _text(query_string), {"quizuser_id": user_id, "id": quiz_instance_id}
        )
        return cursor.fetchall()
