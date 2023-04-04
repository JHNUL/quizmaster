from functools import wraps
from flask import redirect, url_for, session, make_response
from src.db import db
from src.repositories.users import UserRepository


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        user = UserRepository(db).get_user_by_username(session["username"])
        if user is None:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return decorated_function


def no_cache(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers.set("Cache-Control", "no-cache, no-store, must-revalidate")
        response.headers.set("Pragma", "no-cache")
        response.headers.set("Expires", 0)
        return response

    return decorated_function
