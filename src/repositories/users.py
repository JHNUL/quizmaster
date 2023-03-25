from flask_sqlalchemy import SQLAlchemy
from src.repositories.utils import _text


class UserRepository:
    def __init__(self, db: 'SQLAlchemy'):
        self.db = db

    def _get_user(self, attribute: str, value, include_password=False):
        basic_attributes = ["id", "username", "created_at"]
        if include_password:
            basic_attributes.append("pw")
        if attribute == "id":
            query_string = f"SELECT {', '.join(basic_attributes)} FROM quizuser WHERE id = :value"
        elif attribute == "username":
            query_string = f"SELECT {', '.join(basic_attributes)} FROM quizuser WHERE username = :value"
        cursor = self.db.session.execute(_text(query_string), {"value": value})
        users = cursor.fetchall()
        if len(users) == 0:
            return None
        return users[0]

    def get_user_by_id(self, user_id: int):
        return self._get_user("id", user_id)

    def get_user_by_username(self, username: str, include_password=False):
        return self._get_user("username", username, include_password)

    def create_new_user(self, username: str, password: str):
        query_string = "INSERT INTO quizuser (username, pw) VALUES (:username, :pw)"
        self.db.session.execute(_text(query_string), {
                                "username": username, "pw": password})
        self.db.session.commit()
        return username
