from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text


class QuizRepository:
    def __init__(self, db: 'SQLAlchemy'):
        self.db = db

    def get_all_quizzes(self):
        query_string = "SELECT * FROM quiz;"
        cursor = self.db.session.execute(_text(query_string))
        return cursor.fetchall()

    def get_quiz_by_id(self, quiz_id):
        query_string = f"SELECT * FROM quiz WHERE id = :id"
        cursor = self.db.session.execute(_text(query_string), {"id": quiz_id})
        quizzes = cursor.fetchall()
        if len(quizzes) == 0:
            return None
        return quizzes[0]

    def create_new_quiz(self, user_id: int, title: str, description: str):
        query_string = """
            INSERT INTO quiz (title, quiz_description, quizuser_id)
            VALUES (:title, :quiz_description, :quizuser_id)
            RETURNING id;
        """
        cursor = self.db.session.execute(_text(query_string), {
            "title": title, "quiz_description": description, "quizuser_id": user_id})
        self.db.session.commit()
        quiz_id, = cursor.fetchone()
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
        cursor = self.db.session.execute(_text(query_string), {
            "quizuser_id": user_id, "quiz_id": quiz_id})
        return cursor.fetchall()

    def get_quiz_instance_by_id(self, quiz_instance_id: int):
        query_string = f"SELECT * FROM quiz_instance WHERE id = :id"
        cursor = self.db.session.execute(
            _text(query_string), {"id": quiz_instance_id})
        instances = cursor.fetchall()
        if len(instances) == 0:
            return None
        return instances[0]

    def create_new_quiz_instance(self, user_id: int, quiz_id: int):
        query_string = """
            INSERT INTO quiz_instance (quizuser_id, quiz_id)
            VALUES (:quizuser_id, :quiz_id)
            RETURNING id;
        """
        cursor = self.db.session.execute(_text(query_string), {
            "quizuser_id": user_id, "quiz_id": quiz_id})
        self.db.session.commit()
        quiz_instance_id, = cursor.fetchone()
        return quiz_instance_id

    def complete_quiz_instance(self, quiz_instance_id: int):
        query_string = """
            UPDATE quiz_instance
            SET finished_at = NOW()
            WHERE id = :id;
        """
        cursor = self.db.session.execute(_text(query_string), {
            "id": quiz_instance_id})
        self.db.session.commit()
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
        cursor = self.db.session.execute(_text(query_string), {
            "quizuser_id": user_id, "id": quiz_instance_id})
        return cursor.fetchall()
