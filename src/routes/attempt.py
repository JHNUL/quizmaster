from flask import render_template, redirect, url_for, request, session
from src.app import app
from src.db import db
from src.routes.decorators import login_required
from src.repositories.quizzes import QuizRepository
from src.repositories.questions import QuestionRepository
from src.repositories.answers import AnswerRepository


@app.route("/attempt/<int:quiz_id>", methods=["GET"])
@login_required
def attempt(quiz_id: int):
    user_id = session["user_id"]
    quiz = QuizRepository(db).get_quiz_by_id(quiz_id)
    active_instances = QuizRepository(
        db).get_quiz_instances(user_id, quiz_id)
    if quiz is None or len(active_instances) > 1:
        # TODO: show some error?
        return redirect(url_for("landingpage"))
    # TODO: quiz with no questions cannot be attempted
    return render_template("attempt.html", quiz=quiz, has_active_instance=len(active_instances) == 1)


@app.route("/attempt/<int:quiz_id>/instance", methods=["POST"])
@login_required
def start_instance(quiz_id: int):
    quiz = QuizRepository(db).get_quiz_by_id(quiz_id)
    if quiz is None:
        # TODO: show some error?
        return redirect(url_for("landingpage"))
    user_id = session["user_id"]
    active_instances = QuizRepository(
        db).get_quiz_instances(user_id, quiz_id)
    if len(active_instances) > 1:
        # TODO: show some error?
        return redirect(url_for("landingpage"))
    elif len(active_instances) == 1:
        quiz_instance_id = active_instances[0].id
    else:
        quiz_instance_id = QuizRepository(
            db).create_new_quiz_instance(user_id, quiz_id)
    answered_questions = QuestionRepository(
        db).get_question_instances_by_quiz_instance(quiz_instance_id)
    all_questions = QuestionRepository(
        db).get_questions_linked_to_quiz(quiz_id)
    question = None
    for q in all_questions:
        print("Finding first unanswered question")
        if len([aq for aq in answered_questions if aq.question_id == q.id]) == 0:
            print("Selected", q.id)
            question = q
            break
    if question is None and len(all_questions > 0):
        # Should not be able to start quiz in this scenario (no unanswered questions left)
        # but for now just show the first one again.
        question = all_questions[0]
    if len(all_questions) == 0:
        # TODO: show some error?
        return redirect(url_for("landingpage"))
    return redirect(url_for("attempt_question", quiz_instance_id=quiz_instance_id, question_id=question.id))


@app.route("/attempt/<int:quiz_instance_id>/question/<int:question_id>", methods=["GET"])
@login_required
def attempt_question(quiz_instance_id: int, question_id: int):
    # TODO: common logic for checking that user_id from session has
    # an active quiz instance with the parameter quiz_instance_id
    # and that the question belongs to the quiz.
    return render_template(
        "question.html",
        quiz_instance_id=quiz_instance_id,
        question=QuestionRepository(db).get_question_by_id(question_id),
        answer_opts=AnswerRepository(
            db).get_answers_linked_to_question(question_id)
    )


@app.route("/attempt/<int:quiz_instance_id>/question/<int:question_id>", methods=["POST"])
@login_required
def save_question(quiz_instance_id: int, question_id: int):
    # TODO: common logic for checking that user_id from session has
    # an active quiz instance with the parameter quiz_instance_id
    # and that the question belongs to the quiz.
    if "answeropt" in request.form:
        answer_id = request.form["answeropt"]
    else:
        return redirect(url_for("attempt_question", quiz_instance_id=quiz_instance_id, question_id=question_id))
    QuestionRepository(db).create_new_question_instance(
        quiz_instance_id, question_id, answer_id)
    answered_questions = QuestionRepository(
        db).get_question_instances_by_quiz_instance(quiz_instance_id)
    all_questions = QuestionRepository(
        db).get_questions_linked_to_quiz_by_quiz_instance_id(quiz_instance_id)
    question = None
    for q in all_questions:
        if len([aq for aq in answered_questions if aq.question_id == q.id]) == 0:
            question = q
            break
    if question is None and len(all_questions) > 0:
        QuizRepository(db).complete_quiz_instance(quiz_instance_id)
        return redirect(url_for("quiz_stats", quiz_instance_id=quiz_instance_id))
    # If attempting to post to quiz with no questions
    if question is None or len(all_questions) == 0:
        # TODO: show some error?
        return redirect(url_for("landingpage"))
    return redirect(url_for("attempt_question", quiz_instance_id=quiz_instance_id, question_id=question.id))


@app.route("/attempt/<int:quiz_instance_id>/stats", methods=["GET"])
@login_required
def quiz_stats(quiz_instance_id: int):
    user_id = session["user_id"]
    quiz_instance_stats = QuizRepository(
        db).get_quiz_instance_stats(quiz_instance_id, user_id)
    stats = {}
    if len(quiz_instance_stats) > 0:
        stats["quiz_title"] = quiz_instance_stats[0][0]
        stats["quiz_description"] = quiz_instance_stats[0][1]
        stats["started"] = quiz_instance_stats[0][3]
        stats["completed"] = quiz_instance_stats[0][4]
        stats["questions"] = []
        for row in quiz_instance_stats:
            stats["questions"].append({
                "question_name": row[5],
                "answer": row[6],
                "is_correct": row[7],
                "answer_time": row[8]
            })
    return render_template("quiz_stats.html", stats=stats)
