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
