from functools import wraps
from flask import request, redirect, url_for, session
from src.db import db
from src.repositories.users import UserRepository


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for('login', next=request.url))
        user = UserRepository(db).get_user_by_username(session["username"])
        if user is None:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function
