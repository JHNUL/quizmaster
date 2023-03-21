from flask import render_template
from src.app import app


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    # TODO
    return render_template("login.html")
