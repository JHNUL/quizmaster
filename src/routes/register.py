from re import match
from flask import render_template, request, redirect
from werkzeug.security import generate_password_hash
from src.app import app
from src.db import db
from src.repositories.users import UserRepository


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("views/register.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    if match("^[a-zA-Z0-9_!&#]{6,50}$", password) is None:
        password_message = "Password must be 6-50 characters long"
        return render_template("views/register.html", message=password_message)
    if match("^[a-zA-Z0-9_@.]{6,50}$", username) is None:
        username_message = "Username must be 6-50 characters long"
        return render_template("views/register.html", message=username_message)
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_username(username)
    if user is None:
        pass_hash = generate_password_hash(password)
        user_repo.create_new_user(username, pass_hash)
        return redirect("/login")
    user_message = "Username not available!"
    return render_template("views/register.html", message=user_message)
