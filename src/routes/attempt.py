from flask import render_template, redirect, url_for, request, session
from src.app import app
from src.db import db
from src.routes.decorators import login_required, no_cache
from src.repositories.quizzes import QuizRepository
from src.repositories.questions import QuestionRepository
from src.repositories.answers import AnswerRepository


@app.route("/attempt/<int:quiz_id>", methods=["GET"])
@login_required
@no_cache
def attempt(quiz_id: int):
    user_id = session["user_id"]
    full_quiz_rows = QuizRepository(db).get_full_quiz_by_id(quiz_id)
    full_quiz = {}
    if len(full_quiz_rows) > 0:
        full_quiz["quiz_title"] = full_quiz_rows[0].title
        full_quiz["quiz_id"] = full_quiz_rows[0].quiz_id
        full_quiz["quiz_description"] = full_quiz_rows[0].quiz_description
        full_quiz["quiz_created"] = full_quiz_rows[0].created_at
        full_quiz["quiz_creator"] = full_quiz_rows[0].username
        full_quiz["questions"] = len(
            {q.question_name for q in full_quiz_rows if q.question_name is not None}
        )
    active_instances = QuizRepository(db).get_quiz_instances(user_id, quiz_id)
    if len(full_quiz_rows) == 0 or len(active_instances) > 1:
        # TODO: show some error?
        return redirect(url_for("landingpage"))
    return render_template(
        "views/start_quiz.html",
        quiz=full_quiz,
        has_active_instance=len(active_instances) == 1,
    )


@app.route("/attempt/<int:quiz_id>/instance", methods=["POST"])
@login_required
def start_instance(quiz_id: int):
    quiz = QuizRepository(db).get_quiz_by_id(quiz_id)
    if quiz is None:
        # TODO: show some error?
        return redirect(url_for("landingpage"))
    user_id = session["user_id"]
    active_instances = QuizRepository(db).get_quiz_instances(user_id, quiz_id)
    if len(active_instances) > 1:
        # TODO: show some error?
        return redirect(url_for("landingpage"))
    if len(active_instances) == 1:
        quiz_instance_id = active_instances[0].id
    else:
        quiz_instance_id = QuizRepository(db).create_new_quiz_instance(user_id, quiz_id)
    answered_questions = QuestionRepository(db).get_question_instances_by_quiz_instance(
        quiz_instance_id
    )
    all_questions = QuestionRepository(db).get_questions_linked_to_quiz(quiz_id)
    question = None
    for elem in all_questions:
        print("Finding first unanswered question")
        if len([aq for aq in answered_questions if aq.question_id == elem.id]) == 0:
            print("Selected", elem.id)
            question = elem
            break
    if question is None and len(all_questions > 0):
        # Should not be able to start quiz in this scenario (no unanswered questions left)
        # but for now just show the first one again.
        question = all_questions[0]
    if len(all_questions) == 0:
        # TODO: show some error?
        return redirect(url_for("landingpage"))
    return redirect(
        url_for(
            "attempt_question",
            quiz_instance_id=quiz_instance_id,
            question_id=question.id,
        )
    )


@app.route(
    "/attempt/<int:quiz_instance_id>/question/<int:question_id>", methods=["GET"]
)
@login_required
@no_cache
def attempt_question(quiz_instance_id: int, question_id: int):
    # TODO: common logic for checking that user_id from session has
    # an active quiz instance with the parameter quiz_instance_id
    # and that the question belongs to the quiz.

    # This page should never be cached in the browser, so that
    # when navigating back with the browser, a new GET request
    # is fired.
    question_instance = QuestionRepository(db).get_question_instance(
        quiz_instance_id, question_id
    )
    return render_template(
        "views/question.html",
        quiz_instance_id=quiz_instance_id,
        question=QuestionRepository(db).get_question_by_id(question_id),
        answer_opts=AnswerRepository(db).get_answers_linked_to_question(question_id),
        question_instance=question_instance,
    )


@app.route(
    "/attempt/<int:quiz_instance_id>/question/<int:question_id>", methods=["POST"]
)
@login_required
def save_question(quiz_instance_id: int, question_id: int):
    # TODO: common logic for checking that user_id from session has
    # an active quiz instance with the parameter quiz_instance_id
    # and that the question belongs to the quiz.
    skip_saving = "skipsaved" in request.form
    if not skip_saving:
        if "answeropt" in request.form:
            answer_id = request.form["answeropt"]
        else:
            return redirect(
                url_for(
                    "attempt_question",
                    quiz_instance_id=quiz_instance_id,
                    question_id=question_id,
                )
            )
        QuestionRepository(db).create_new_question_instance(
            quiz_instance_id, question_id, answer_id
        )
    answered_questions = QuestionRepository(db).get_question_instances_by_quiz_instance(
        quiz_instance_id
    )
    all_questions = QuestionRepository(
        db
    ).get_questions_linked_to_quiz_by_quiz_instance_id(quiz_instance_id)
    question = None
    for elem in all_questions:
        if len([aq for aq in answered_questions if aq.question_id == elem.id]) == 0:
            question = elem
            break
    if question is None and len(all_questions) > 0:
        QuizRepository(db).complete_quiz_instance(quiz_instance_id)
        return redirect(url_for("quiz_stats", quiz_instance_id=quiz_instance_id))
    # If attempting to post to quiz with no questions
    if question is None or len(all_questions) == 0:
        # TODO: show some error?
        return redirect(url_for("landingpage"))
    return redirect(
        url_for(
            "attempt_question",
            quiz_instance_id=quiz_instance_id,
            question_id=question.id,
        )
    )


@app.route("/attempt/<int:quiz_instance_id>/stats", methods=["GET"])
@login_required
def quiz_stats(quiz_instance_id: int):
    user_id = session["user_id"]
    quiz_instance_stats = QuizRepository(db).get_quiz_instance_stats(
        quiz_instance_id, user_id
    )
    stats = {}
    if len(quiz_instance_stats) > 0:
        stats["quiz_title"] = quiz_instance_stats[0][0]
        stats["quiz_description"] = quiz_instance_stats[0][1]
        stats["started"] = quiz_instance_stats[0][3]
        stats["completed"] = quiz_instance_stats[0][4]
        stats["questions"] = []
        for row in quiz_instance_stats:
            stats["questions"].append(
                {
                    "question_name": row[5],
                    "answer": row[6],
                    "is_correct": row[7],
                    "answer_time": row[8],
                }
            )
    return render_template("views/quiz_stats.html", stats=stats)
