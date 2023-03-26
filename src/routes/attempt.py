from flask import render_template, redirect, url_for
from src.app import app
from src.db import db
from src.routes.decorators import login_required
from src.repositories.quizzes import QuizRepository
from src.repositories.questions import QuestionRepository
from src.repositories.answers import AnswerRepository


@app.route("/attempt/<int:quiz_id>", methods=["GET"])
@login_required
def attempt(quiz_id: int):
    quiz = QuizRepository(db).get_quiz_by_id(quiz_id)
    questions = QuestionRepository(db).get_questions_linked_to_quiz(quiz_id)
    question_id = -1
    if len(questions) > 0:
        question_id = questions[0].id
    if quiz is None:
        return redirect(url_for("landingpage"))
    return render_template("attempt.html", quiz=quiz, question_id=question_id)


@app.route("/attempt/<int:quiz_id>/question/<int:question_id>", methods=["GET"])
@login_required
def attempt_question(quiz_id: int, question_id: int):
    questions = QuestionRepository(db).get_questions_linked_to_quiz(quiz_id)
    question = [q for q in questions if q.id == question_id]
    if len(question) == 0:
        return redirect(url_for("attempt", quiz_id=quiz_id))
    question = question[0]
    answer_opts = AnswerRepository(
        db).get_answers_linked_to_question(question.id)
    return render_template(
        "question.html",
        quiz_id=quiz_id,
        question=question,
        answer_opts=answer_opts
    )


@app.route("/attempt/<int:quiz_id>/question/<int:question_id>", methods=["POST"])
@login_required
def save_question(quiz_id: int, question_id: int):
    # TODO: save answer from form data
    questions = QuestionRepository(db).get_questions_linked_to_quiz(quiz_id)
    next_question_id = -1
    for i in range(len(questions)):
        if questions[i].id == question_id:
            if i < len(questions) - 1:
                next_question_id = questions[i+1].id
    if next_question_id < 0:
        return redirect(url_for("quiz_stats", quiz_id=quiz_id))
    return redirect(url_for('attempt_question', quiz_id=quiz_id, question_id=next_question_id))


@app.route("/attempt/<int:quiz_id>/stats", methods=["GET"])
@login_required
def quiz_stats(quiz_id: int):
    quiz = QuizRepository(db).get_quiz_by_id(quiz_id)
    return render_template("quiz_stats.html", quiz=quiz)
