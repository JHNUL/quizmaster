from re import match
from flask import render_template, redirect, request, session, url_for
from werkzeug.exceptions import NotFound
from src.app import app
from src.db import db
from src.routes.decorators import login_required, no_cache, csrf
from src.routes.utils import (
    _create_full_quiz_object,
    _check_question_fields,
    _check_quiz_fields,
)
from src.repositories.quizzes import QuizRepository
from src.repositories.questions import QuestionRepository
from src.repositories.connections import ConnectionRepository
from src.repositories.answers import AnswerRepository


@app.route("/quiz", methods=["GET"])
@login_required
@no_cache
def quiz():
    return render_template("views/create_quiz.html")


@app.route("/quiz", methods=["POST"])
@login_required
@csrf
def new_quiz():
    title = request.form["quiztitle"]
    description = request.form["quizdescription"]
    _check_quiz_fields(title, description)
    publish = False if "publish" not in request.form else request.form["publish"]
    user_id = session["user_id"]
    quiz_id = QuizRepository(db).create_new_quiz(user_id, title, description, publish)
    return redirect(f"/quiz/{quiz_id}")


@app.route("/quiz/<int:quiz_id>/edit", methods=["GET"])
@login_required
@no_cache
def edit_quiz_view(quiz_id: int):
    user_id = session["user_id"]
    full_quiz_rows = QuizRepository(db).get_user_full_quiz_by_id(quiz_id, user_id)
    if len(full_quiz_rows) == 0:
        raise NotFound
    full_quiz = _create_full_quiz_object(full_quiz_rows)
    return render_template("views/edit_quiz.html", quiz=full_quiz)


@app.route("/quiz/<int:quiz_id>/edit", methods=["POST"])
@login_required
@csrf
def edit_quiz(quiz_id: int):
    user_id = session["user_id"]
    title = request.form["quiztitle"]
    description = request.form["quizdescription"]
    _check_quiz_fields(title, description)
    QuizRepository(db).update_quiz(quiz_id, title, description, user_id)
    return redirect(f"/quiz/{quiz_id}")


@app.route("/quiz/<int:quiz_id>/publish", methods=["POST"])
@login_required
@csrf
def publish_quiz(quiz_id: int):
    user_id = session["user_id"]
    QuizRepository(db).publish_quiz(quiz_id, user_id)
    return redirect(url_for("landingpage"))


@app.route("/quiz/<int:quiz_id>/delete", methods=["POST"])
@login_required
@csrf
def delete_quiz(quiz_id: int):
    user_id = session["user_id"]
    if QuizRepository(db).is_user_quiz(quiz_id, user_id):
        QuizRepository(db).delete_quiz(quiz_id, user_id)
    return redirect(url_for("landingpage"))


@app.route("/quiz/<int:quiz_id>", methods=["GET"])
@login_required
@no_cache
def create_question(quiz_id: int):
    user_id = session["user_id"]
    full_quiz_rows = QuizRepository(db).get_user_full_quiz_by_id(quiz_id, user_id)
    if len(full_quiz_rows) == 0:
        raise NotFound
    full_quiz = _create_full_quiz_object(full_quiz_rows)
    return render_template("views/create_question.html", quiz=full_quiz)


@app.route("/quiz/<int:quiz_id>/question", methods=["POST"])
@login_required
@csrf
def quiz_question(quiz_id: int):
    user_id = session["user_id"]
    full_quiz_rows = QuizRepository(db).get_user_full_quiz_by_id(quiz_id, user_id)
    if len(full_quiz_rows) == 0:
        raise NotFound
    question_name = request.form["questionname"]
    corrects = request.form.getlist("iscorrect")
    answers = []
    for name, val in request.form.items():
        if match("^answeropt", name) is not None:
            answers.append((val, len([c for c in corrects if c == name]) > 0))
    _check_question_fields(answers, question_name)
    question_id = QuestionRepository(db).create_new_question(question_name)
    conn_repo = ConnectionRepository(db)
    conn_repo.link_question_to_quiz(question_id, quiz_id)
    answer_repo = AnswerRepository(db)
    for answer, is_correct in answers:
        answer_id = answer_repo.create_new_answer(answer, is_correct)
        conn_repo.link_answer_to_question(answer_id, question_id)
    return redirect(f"/quiz/{quiz_id}")


@app.route("/quiz/<int:quiz_id>/question/<int:question_id>/delete", methods=["POST"])
@login_required
@csrf
def delete_question(quiz_id: int, question_id: int):
    user_id = session["user_id"]
    full_quiz_rows = QuizRepository(db).get_user_full_quiz_by_id(quiz_id, user_id)
    if len(full_quiz_rows) == 0:
        raise NotFound
    full_quiz = _create_full_quiz_object(full_quiz_rows)
    if len([q for q in full_quiz["questions"] if q[0] == question_id]) == 0:
        raise NotFound
    QuestionRepository(db).delete_question(question_id)
    return redirect(f"/quiz/{quiz_id}")
