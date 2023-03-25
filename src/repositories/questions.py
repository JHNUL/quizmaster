from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text


class QuestionRepository:
    def __init__(self, db: 'SQLAlchemy'):
        self.db = db

    def create_new_question(self, name: str) -> int:
        query_string = """
            INSERT INTO question (question_name)
            VALUES (:question_name)
            RETURNING id;
        """
        cursor = self.db.session.execute(
            _text(query_string), {"question_name": name})
        self.db.session.commit()
        question_id, = cursor.fetchone()
        return question_id
