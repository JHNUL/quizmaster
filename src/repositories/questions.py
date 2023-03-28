from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text


class QuestionRepository:
    def __init__(self, db: 'SQLAlchemy'):
        self.db = db

    def get_question_by_id(self, question_id: int):
        """Parameters: (int) question_id

        Returns:
            tuple: question with the following fields
            id: (int) question id
            question_name: (str) question name
        """
        query_string = "SELECT * FROM question WHERE id = :id;"
        cursor = self.db.session.execute(
            _text(query_string), {"id": question_id})
        questions = cursor.fetchall()
        if len(questions) == 0:
            return None
        return questions[0]

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

    def get_questions_linked_to_quiz_by_quiz_instance_id(self, quiz_insance_id: int) -> list:
        query_string = """
            SELECT q.* FROM question q
            JOIN quiz_question qq ON qq.question_id = q.id
            WHERE qq.quiz_id = (SELECT quiz_id FROM quiz_instance WHERE quiz_instance.id = :id)
            ORDER BY q.id ASC;
        """
        cursor = self.db.session.execute(
            _text(query_string), {"id": quiz_insance_id})
        return cursor.fetchall()

    def get_question_instances_by_quiz_instance(self, quiz_instance_id: int):
        query_string = """
            SELECT * FROM question_instance
            WHERE quiz_instance_id = :quiz_instance_id;
        """
        cursor = self.db.session.execute(
            _text(query_string), {"quiz_instance_id": quiz_instance_id})
        return cursor.fetchall()

    def create_new_question_instance(self, quiz_instance_id: int, question_id: int, answer_id: int):
        query_string = """
            INSERT INTO question_instance (quiz_instance_id, question_id, answer_id)
            VALUES (:quiz_instance_id, :question_id, :answer_id)
            RETURNING id;
        """
        cursor = self.db.session.execute(
            _text(query_string), {"quiz_instance_id": quiz_instance_id, "question_id": question_id, "answer_id": answer_id})
        self.db.session.commit()
        question_instance_id, = cursor.fetchone()
        return question_instance_id

    def get_question_instance(self, quiz_instance_id: int, question_id: int):
        query_string = """
            SELECT * FROM question_instance
            WHERE quiz_instance_id = :quiz_instance_id
            AND question_id = :question_id;
        """
        cursor = self.db.session.execute(
            _text(query_string), {"quiz_instance_id": quiz_instance_id, "question_id": question_id})
        instances = cursor.fetchall()
        if len(instances) == 0:
            return None
        return instances[0]
