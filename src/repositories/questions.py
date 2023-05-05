from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text, _utcnow


class QuestionRepository:
    def __init__(self, database: "SQLAlchemy"):
        self.database = database

    def get_question_by_id(self, question_id: int):
        """Parameters: (int) question_id

        Returns:
            tuple: question with the following fields
            id: (int) question id
            question_name: (str) question name
        """
        query_string = "SELECT * FROM question WHERE id = :id;"
        cursor = self.database.session.execute(_text(query_string), {"id": question_id})
        questions = cursor.fetchall()
        if len(questions) == 0:
            return None
        return questions[0]

    def create_new_question(self, name: str) -> int:
        query_string = """
            INSERT INTO question (question_name)
            VALUES (:question_name)
            RETURNING id;
        """
        cursor = self.database.session.execute(
            _text(query_string), {"question_name": name}
        )
        self.database.session.commit()
        (question_id,) = cursor.fetchone()
        return question_id

    def delete_question(self, question_id: int) -> int:
        """
        Note that user access has to be checked before.
        """
        query_string_question = """
            UPDATE question
            SET is_active = FALSE
            WHERE id = :id;
        """
        query_string_answer = """
            UPDATE answer a
            SET is_active = FALSE
            WHERE a.id IN (
                SELECT answer_id FROM question_answer qa WHERE qa.question_id = :question_id
            );
        """
        self.database.session.execute(_text(query_string_question), {"id": question_id})
        self.database.session.execute(
            _text(query_string_answer), {"question_id": question_id}
        )
        self.database.session.commit()
        return True

    def get_questions_linked_to_quiz(self, quiz_id: int) -> list:
        query_string = """
            SELECT q.* FROM question q
            JOIN quiz_question qq ON qq.question_id = q.id
            WHERE qq.quiz_id = :quiz_id
            ORDER BY q.id ASC;
        """
        cursor = self.database.session.execute(
            _text(query_string), {"quiz_id": quiz_id}
        )
        return cursor.fetchall()

    def get_questions_linked_to_quiz_by_quiz_instance_id(
        self, quiz_insance_id: int
    ) -> list:
        query_string = """
            SELECT q.* FROM question q
            JOIN quiz_question qq ON qq.question_id = q.id
            WHERE qq.quiz_id = (SELECT quiz_id FROM quiz_instance WHERE quiz_instance.id = :id)
            ORDER BY q.id ASC;
        """
        cursor = self.database.session.execute(
            _text(query_string), {"id": quiz_insance_id}
        )
        return cursor.fetchall()

    def get_question_instances_by_quiz_instance(self, quiz_instance_id: int):
        query_string = """
            SELECT * FROM question_instance
            WHERE quiz_instance_id = :quiz_instance_id;
        """
        cursor = self.database.session.execute(
            _text(query_string), {"quiz_instance_id": quiz_instance_id}
        )
        return cursor.fetchall()

    def create_new_question_instance(
        self, quiz_instance_id: int, question_id: int, answer_id: int, user_id: int
    ):
        query_string = """
            INSERT INTO question_instance (
                quizuser_id,
                quiz_instance_id,
                question_id,
                answer_id,
                answered_at
            )
            VALUES (
                :quizuser_id,
                :quiz_instance_id,
                :question_id,
                :answer_id,
                :answered_at
            )
            RETURNING id;
        """
        cursor = self.database.session.execute(
            _text(query_string),
            {
                "quizuser_id": user_id,
                "quiz_instance_id": quiz_instance_id,
                "question_id": question_id,
                "answer_id": answer_id,
                "answered_at": _utcnow(),
            },
        )
        self.database.session.commit()
        (question_instance_id,) = cursor.fetchone()
        return question_instance_id

    def get_question_instance(self, quiz_instance_id: int, question_id: int):
        query_string = """
            SELECT * FROM question_instance
            WHERE quiz_instance_id = :quiz_instance_id
            AND question_id = :question_id;
        """
        cursor = self.database.session.execute(
            _text(query_string),
            {"quiz_instance_id": quiz_instance_id, "question_id": question_id},
        )
        instances = cursor.fetchall()
        if len(instances) == 0:
            return None
        return instances[0]

    def get_full_question(
        self, quiz_instance_id: int, question_id: int, quizuser_id: int
    ):
        """Parameters:
            quiz_instance_id: (int)
            question_id: (int)
            quizuser_id: (int)

        Returns: question with answer options if question belongs to this
        quiz instance and quiz instance belongs to this user. Also returns
        given answer if question was already answered.
        """
        query_string = """
            SELECT
                qq.*,
                q.question_name,
                qui.id as question_instance_id,
                qui.question_id as qui_question_id,
                qui.answer_id,
                qui.answered_at,
                a.id as answer_option_id,
                a.answer_text as answer_text,
                a.is_correct as is_correct
            FROM quiz_instance qi
            LEFT JOIN quiz_question qq ON qq.quiz_id = qi.quiz_id
            LEFT JOIN question q ON q.id = qq.question_id
            LEFT JOIN question_instance qui ON qui.quiz_instance_id = qi.id AND qui.question_id = qq.question_id
            LEFT JOIN question_answer qa ON qa.question_id = qq.question_id
            LEFT JOIN answer a ON qa.answer_id = a.id
            WHERE qi.id = :id AND qi.quizuser_id = :quizuser_id AND qq.question_id = :question_id;
        """
        cursor = self.database.session.execute(
            _text(query_string),
            {
                "id": quiz_instance_id,
                "quizuser_id": quizuser_id,
                "question_id": question_id,
            },
        )
        return cursor.fetchall()

    def get_count_of_question_instances_by_user(self, user_id: int):
        query_string = """
            SELECT COUNT(*) FROM question_instance qi
            JOIN question q ON q.id = qi.question_id
            WHERE quizuser_id = :quizuser_id
            AND q.is_active = TRUE;
        """
        cursor = self.database.session.execute(
            _text(query_string), {"quizuser_id": user_id}
        )
        return cursor.fetchone()[0]

    def get_correct_answer_percentage(self, user_id: int):
        query_string = """
            SELECT 100.0*SUM(CAST(a.is_correct AS INTEGER)) / NULLIF(COUNT(*), 0) AS PERCENTAGE
            FROM question_instance qi
            JOIN question q ON q.id = qi.question_id
            JOIN answer a ON qi.answer_id = a.id
            WHERE quizuser_id = :quizuser_id
            AND q.is_active = TRUE
            AND a.is_active = TRUE;
        """
        cursor = self.database.session.execute(
            _text(query_string), {"quizuser_id": user_id}
        )
        res = cursor.fetchone()
        if res[0] is None:
            return 0.0
        return res[0]
