from flask import render_template, request, session
from src.app import app
from src.db import db
from src.routes.decorators import login_required
from src.repositories.quizzes import QuizRepository


@app.route("/quiz", methods=["GET"])
@login_required
def quiz():
    return render_template("quiz.html")


@app.route("/quiz", methods=["POST"])
@login_required
def new_quiz():
    title = request.form["quiztitle"]
    description = request.form["quizdescription"]
    user_id = session["user_id"]
    quiz_id = QuizRepository(db).create_new_quiz(user_id, title, description)
    # TODO: redirect to individual quiz view using quiz_id
    return render_template("quiz.html")
