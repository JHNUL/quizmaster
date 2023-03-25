from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash
from src.app import app
from src.db import db
from src.repositories.users import UserRepository


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_username(username, include_password=True)
    if len(user) == 0:
        return render_template("login.html", message="Username not found!")

    if check_password_hash(user[0].pw, password):
        session["username"] = username
        session["user_id"] = user[0].id
        return redirect("/")

    return render_template("login.html", message="Incorrect password!")
