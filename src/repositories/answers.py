from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text


class AnswerRepository:
    def __init__(self, db: 'SQLAlchemy'):
        self.db = db

    def create_new_answer(self, answer_text: str, is_correct=False) -> int:
        query_string = """
            INSERT INTO answer (answer_text, is_correct)
            VALUES (:answer_text, :is_correct)
            RETURNING id;
        """
        cursor = self.db.session.execute(
            _text(query_string), {"answer_text": answer_text, "is_correct": is_correct})
        self.db.session.commit()
        answer_id, = cursor.fetchone()
        return answer_id

    def get_answers_linked_to_question(self, question_id: int):
        query_string = """
            SELECT ans.* FROM question_answer
            JOIN answer ans ON ans.id = question_answer.answer_id
            WHERE question_answer.question_id = :question_id;
        """
        cursor = self.db.session.execute(
            _text(query_string), {"question_id": question_id})
        return cursor.fetchall()
