from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text


class UserRepository:
    def __init__(self, db: 'SQLAlchemy'):
        self.db = db

    def _get_user(self, attribute: str, value):
        if attribute == "id":
            query_string = "SELECT id, username, created_at FROM quizuser WHERE id = :value"
        elif attribute == "username":
            query_string = "SELECT id, username, created_at FROM quizuser WHERE username = :value"
        cursor = self.db.session.execute(_text(query_string), {"value": value})
        return cursor.fetchall()

    def get_user_by_id(self, user_id: int):
        return self._get_user("id", user_id)

    def get_user_by_username(self, username: str):
        return self._get_user("username", username)

    def create_new_user(self, username: str, password: str):
        query_string = "INSERT INTO quizuser (username, pw) VALUES (:username, :pw)"
        self.db.session.execute(_text(query_string), {
                                "username": username, "pw": password})
        self.db.session.commit()
        return username
