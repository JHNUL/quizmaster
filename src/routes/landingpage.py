from flask import render_template, session
from werkzeug.exceptions import (
    NotFound,
    BadRequest,
    Unauthorized,
    InternalServerError,
    Forbidden,
)
from src.app import app
from src.db import db
from src.routes.decorators import login_required
from src.repositories.quizzes import QuizRepository


@app.route("/", methods=["GET"])
@login_required
def landingpage():
    user_id = session["user_id"]
    quizzes = QuizRepository(db).get_all_visible_quizzes(user_id)
    return render_template("views/index.html", quizzes=quizzes, user_id=user_id)


@app.errorhandler(BadRequest)
def bad_request(error):
    return render_template("views/400.html", description=str(error)), 400


@app.errorhandler(Unauthorized)
def unauthorized(error):
    return render_template("views/401.html"), 401


@app.errorhandler(Forbidden)
def forbidden(error):
    return render_template("views/403.html"), 403


@app.errorhandler(NotFound)
def not_found(error):
    return render_template("views/404.html"), 404


@app.errorhandler(InternalServerError)
def internal_error(error):
    return render_template("views/500.html"), 500
