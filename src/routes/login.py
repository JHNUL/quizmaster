from random import randbytes
from flask import render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash
from src.app import app
from src.db import db
from src.repositories.users import UserRepository


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("views/login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_username(username, include_password=True)
    if user is None:
        flash("Username not found!", "error")
        return render_template("views/login.html")

    if check_password_hash(user.pw, password):
        session["username"] = username
        session["user_id"] = user.id
        session["csrf_token"] = randbytes(16).hex()
        user_repo.set_login_time(user.id)
        return redirect("/")

    flash("Incorrect password!", "error")
    return render_template("views/login.html")
