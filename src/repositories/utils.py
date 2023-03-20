from src.app import app


def _text(sql: str) -> str:
    return app.extensions['sqlalchemy'].text(sql)
