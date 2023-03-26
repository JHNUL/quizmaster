from flask import render_template
from src.app import app
from src.db import db
from src.routes.decorators import login_required
from src.repositories.quizzes import QuizRepository


@app.route("/", methods=["GET"])
@login_required
def landingpage():
    quizzes = QuizRepository(db).get_all_quizzes()
    return render_template("index.html", quizzes=quizzes)
