from datetime import datetime, timezone
from src.app import app


def _text(sql: str) -> str:
    return app.extensions["sqlalchemy"].text(sql)


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
