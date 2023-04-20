from flask import render_template, redirect, url_for, request, session
from werkzeug.exceptions import NotFound
from src.app import app
from src.db import db
from src.routes.decorators import login_required, no_cache
from src.routes.utils import _get_next_unanswered_question, _create_time_diff_text
from src.repositories.quizzes import QuizRepository
from src.repositories.questions import QuestionRepository


@app.route("/attempt/<int:quiz_id>", methods=["GET"])
@login_required
@no_cache
def start_quiz(quiz_id: int):
    user_id = session["user_id"]
    full_quiz_rows = QuizRepository(db).get_full_quiz_by_id(quiz_id)
    if len(full_quiz_rows) == 0:
        raise NotFound
    full_quiz = {}
    full_quiz["quiz_title"] = full_quiz_rows[0].title
    full_quiz["quiz_id"] = full_quiz_rows[0].quiz_id
    full_quiz["quiz_description"] = full_quiz_rows[0].quiz_description
    full_quiz["quiz_created"] = full_quiz_rows[0].created_at
    full_quiz["quiz_creator"] = full_quiz_rows[0].username
    full_quiz["questions"] = len(
        {q.question_name for q in full_quiz_rows if q.question_name is not None}
    )
    active_instances = QuizRepository(db).get_quiz_instances(user_id, quiz_id)
    return render_template(
        "views/start_quiz.html",
        quiz=full_quiz,
        has_active_instance=len(active_instances) == 1,
    )


@app.route("/attempt/<int:quiz_id>/instance", methods=["POST"])
@login_required
def create_quiz_instance(quiz_id: int):
    user_id = session["user_id"]
    active_instances = QuizRepository(db).get_quiz_instances(user_id, quiz_id)
    if len(active_instances) > 0:
        quiz_instance_id = active_instances[0].id
    else:
        quiz_instance_id = QuizRepository(db).create_new_quiz_instance(user_id, quiz_id)

    quiz_progress = QuizRepository(db).get_quiz_instance_progress(
        quiz_instance_id, user_id
    )
    question_id = _get_next_unanswered_question(quiz_progress)
    if question_id is None:
        question_id = quiz_progress[0].question_id
    return redirect(
        url_for(
            "attempt_question",
            quiz_instance_id=quiz_instance_id,
            question_id=question_id,
        )
    )


@app.route(
    "/attempt/<int:quiz_instance_id>/question/<int:question_id>", methods=["GET"]
)
@login_required
@no_cache
def attempt_question(quiz_instance_id: int, question_id: int):
    user_id = session["user_id"]
    question_instance = QuestionRepository(db).get_full_question(
        quiz_instance_id, question_id, user_id
    )
    if len(question_instance) == 0:
        raise NotFound
    question = {}
    question["question_name"] = question_instance[0].question_name
    question["question_id"] = question_instance[0].question_id
    question["answer_id"] = question_instance[0].answer_id
    question["answer_options"] = [
        (row.answer_option_id, row.answer_text) for row in question_instance
    ]
    return render_template(
        "views/question.html",
        quiz_instance_id=quiz_instance_id,
        question=question,
    )


@app.route(
    "/attempt/<int:quiz_instance_id>/question/<int:question_id>", methods=["POST"]
)
@login_required
def save_question(quiz_instance_id: int, question_id: int):
    user_id = session["user_id"]
    question_instance = QuestionRepository(db).get_full_question(
        quiz_instance_id, question_id, user_id
    )
    if len(question_instance) == 0:
        raise NotFound

    already_saved = question_instance[0].answer_id is not None
    if not already_saved:
        if "answeropt" in request.form:
            answer_id = request.form["answeropt"]
            QuestionRepository(db).create_new_question_instance(
                quiz_instance_id, question_id, answer_id
            )
        else:
            return redirect(
                url_for(
                    "attempt_question",
                    quiz_instance_id=quiz_instance_id,
                    question_id=question_id,
                )
            )
    quiz_progress = QuizRepository(db).get_quiz_instance_progress(
        quiz_instance_id, user_id
    )
    next_question_id = _get_next_unanswered_question(quiz_progress)
    if next_question_id is None:
        QuizRepository(db).complete_quiz_instance(quiz_instance_id)
        return redirect(url_for("quiz_stats", quiz_instance_id=quiz_instance_id))
    return redirect(
        url_for(
            "attempt_question",
            quiz_instance_id=quiz_instance_id,
            question_id=next_question_id,
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
        stats["timedelta"] = _create_time_diff_text(
            quiz_instance_stats[0][3], quiz_instance_stats[0][4]
        )
        stats["questions"] = []
        for i, row in enumerate(quiz_instance_stats):
            stats["questions"].append(
                {
                    "question_name": row[5],
                    "answer": row[6],
                    "is_correct": row[7],
                    "timedelta": _create_time_diff_text(
                        stats["started"] if i == 0 else quiz_instance_stats[i - 1][8],
                        row[8],
                    ),
                }
            )
    return render_template("views/quiz_stats.html", stats=stats)
