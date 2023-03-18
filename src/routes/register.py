from flask import render_template, request
from src.app import app


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    return render_template("register.html")
