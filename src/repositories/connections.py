from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text


class ConnectionRepository:
    def __init__(self, db: 'SQLAlchemy'):
        self.db = db

    def link_question_to_quiz(self, question_id: int, quiz_id: int):
        query_string = "INSERT INTO quiz_question (quiz_id, question_id) VALUES (:quiz_id, :question_id);"
        cursor = self.db.session.execute(
            _text(query_string), {"quiz_id": quiz_id, "question_id": question_id})
        self.db.session.commit()
        return cursor.rowcount

    def link_answer_to_question(self, answer_id: int, question_id: int):
        query_string = "INSERT INTO question_answer (question_id, answer_id) VALUES (:question_id, :answer_id);"
        cursor = self.db.session.execute(
            _text(query_string), {"question_id": question_id, "answer_id": answer_id})
        self.db.session.commit()
        return cursor.rowcount
