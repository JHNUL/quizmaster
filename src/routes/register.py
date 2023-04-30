from re import match
from flask import render_template, request, redirect, flash
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
        flash("Password must be 6-50 characters long", "error")
        return render_template("views/register.html")
    if match("^[a-zA-Z0-9_@.]{6,50}$", username) is None:
        flash("Username must be 6-50 characters long", "error")
        return render_template("views/register.html")
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_username(username)
    if user is None:
        pass_hash = generate_password_hash(password)
        user_repo.create_new_user(username, pass_hash)
        flash("Username created!", "success")
        return redirect("/login")
    flash("Username not available!", "error")
    return render_template("views/register.html")
