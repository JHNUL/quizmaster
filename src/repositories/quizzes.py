from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text


class QuizRepository:
    def __init__(self, db: 'SQLAlchemy'):
        self.db = db

    def create_new_quiz(self, user_id: int, title: str, description: str):
        query_string = """
            INSERT INTO quiz (title, quiz_description, quizuser_id)
            VALUES (:title, :quiz_description, :quizuser_id)
            RETURNING id;
        """
        res = self.db.session.execute(_text(query_string), {
            "title": title, "quiz_description": description, "quizuser_id": user_id})
        self.db.session.commit()
        quiz_id, = res.fetchone()
        return quiz_id
