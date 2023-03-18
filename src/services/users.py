from src.app import app
from src.db import db


def _text(sql: str) -> str:
    return app.extensions['sqlalchemy'].text(sql)


def get_user(user_id: int):
    sql = _text("SELECT * FROM quizuser WHERE id = :id")
    cursor = db.session.execute(sql, {"id": user_id})
    res = cursor.fetchall()
    if len(res) == 0:
        return res
    return res[0]
