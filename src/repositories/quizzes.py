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
