from re import match
from flask import render_template, redirect, request, session
from src.app import app
from src.db import db
from src.routes.decorators import login_required
from src.repositories.quizzes import QuizRepository
from src.repositories.questions import QuestionRepository
from src.repositories.connections import ConnectionRepository
from src.repositories.answers import AnswerRepository


@app.route("/quiz", methods=["GET"])
@login_required
def quiz():
    return render_template("views/create_quiz.html")


@app.route("/quiz/<int:quiz_id>", methods=["GET"])
@login_required
def create_question(quiz_id: int):
    user_id = session["user_id"]
    full_quiz_rows = QuizRepository(db).get_user_full_quiz_by_id(quiz_id, user_id)
    if len(full_quiz_rows) == 0:
        return redirect("/")  # TODO: not found page
    full_quiz = {}
    full_quiz["quiz_title"] = full_quiz_rows[0].title
    full_quiz["quiz_id"] = full_quiz_rows[0].quiz_id
    full_quiz["quiz_description"] = full_quiz_rows[0].quiz_description
    full_quiz["quiz_created"] = full_quiz_rows[0].created_at
    full_quiz["quiz_creator"] = full_quiz_rows[0].username
    full_quiz["questions"] = list(
        {
            (q.question_id, q.question_name)
            for q in full_quiz_rows
            if q.question_name is not None
        }
    )
    return render_template("views/create_question.html", quiz=full_quiz)


@app.route("/quiz/<int:quiz_id>/question", methods=["POST"])
@login_required
def quiz_question(quiz_id: int):
    question_name = request.form["questionname"]
    corrects = request.form.getlist("iscorrect")
    fields = request.form.items()
    answers = []  # TODO: fail if request has > max accepted amount of answers
    for name, val in fields:
        if match("^answeropt", name) is not None:
            answers.append((val, len([c for c in corrects if c == name]) > 0))
    question_id = QuestionRepository(db).create_new_question(question_name)
    conn_repo = ConnectionRepository(db)
    conn_repo.link_question_to_quiz(question_id, quiz_id)
    answer_repo = AnswerRepository(db)
    for answer, is_correct in answers:
        answer_id = answer_repo.create_new_answer(answer, is_correct)
        conn_repo.link_answer_to_question(answer_id, question_id)
    return redirect(f"/quiz/{quiz_id}")


@app.route("/quiz", methods=["POST"])
@login_required
def new_quiz():
    title = request.form["quiztitle"]
    description = request.form["quizdescription"]
    user_id = session["user_id"]
    quiz_id = QuizRepository(db).create_new_quiz(user_id, title, description)
    return redirect(f"/quiz/{quiz_id}")
