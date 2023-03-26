from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text


class QuestionRepository:
    def __init__(self, db: 'SQLAlchemy'):
        self.db = db

    def create_new_question(self, name: str) -> int:
        # TODO: refactor to add the link to connection table at the same time?
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

    def get_questions_linked_to_quiz(self, quiz_id: int) -> list:
        query_string = """
        SELECT q.* FROM question q
        JOIN quiz_question qq ON qq.question_id = q.id
        WHERE qq.quiz_id = :quiz_id
        ORDER BY q.id ASC;
        """
        cursor = self.db.session.execute(
            _text(query_string), {"quiz_id": quiz_id})
        return cursor.fetchall()
