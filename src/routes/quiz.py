from flask import render_template, redirect, request, session
from re import match
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
    return render_template("quiz.html")


@app.route("/quiz/<int:quiz_id>", methods=["GET"])
@login_required
def quiz_detail(quiz_id: int):
    found_quiz = QuizRepository(db).get_quiz_by_id(quiz_id)
    if found_quiz is None:
        redirect("/")  # TODO: not found page
    questions = QuestionRepository(db).get_questions_linked_to_quiz(quiz_id)
    return render_template(
        "quiz_detail.html",
        quiz_title=found_quiz[2],
        quiz_description=found_quiz[3],
        quiz_created=found_quiz[4],
        quiz_id=found_quiz[0],
        questions=questions
    )


@app.route("/quiz/<int:quiz_id>/question", methods=["POST"])
@login_required
def quiz_question(quiz_id: int):
    question_name = request.form["questionname"]
    fields = request.form.items()
    answers = []  # TODO: fail if request has > max accepted amount of answers
    for name, val in fields:
        if match("^answeropt", name) is not None:
            answers.append(val)
    question_id = QuestionRepository(db).create_new_question(question_name)
    conn_repo = ConnectionRepository(db)
    conn_repo.link_question_to_quiz(question_id, quiz_id)
    answer_repo = AnswerRepository(db)
    for answer in answers:
        answer_id = answer_repo.create_new_answer(answer)
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
