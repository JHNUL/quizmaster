from flask import render_template, session
from src.app import app
from src.db import db
from src.routes.decorators import login_required
from src.routes.utils import (
    _create_time_diff_text,
)
from src.repositories.quizzes import QuizRepository
from src.repositories.questions import QuestionRepository


@app.route("/stats", methods=["GET"])
@login_required
def stats():
    user_id = session["user_id"]
    username = session["username"]
    instances = QuizRepository(db).get_all_quiz_instances_by_user(user_id)
    durations = []
    for instance in instances:
        delta = instance[4] - instance[3]
        durations.append(delta.total_seconds())
    avg_duration = 0 if len(durations) == 0 else sum(durations) / len(durations)
    answers_count = QuestionRepository(db).get_count_of_question_instances_by_user(
        user_id
    )
    correct_percentage = QuestionRepository(db).get_correct_answer_percentage(user_id)
    statistics = {
        "total_quizzes": len(instances),
        "total_answers": answers_count,
        "correct_percentage": f"{correct_percentage:.1f}%",
        "average_duration": _create_time_diff_text(avg_duration),
    }
    return render_template("views/stats.html", username=username, statistics=statistics)
