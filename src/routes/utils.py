from jinja2.utils import markupsafe
from werkzeug.exceptions import BadRequest
from src.constants import (
    ANSWER_MAX_LEN,
    ANSWERS_MAX,
    ANSWERS_MIN,
    QUESTION_MAX_LEN,
    QUIZ_DESC_MAX_LEN,
    QUIZ_TITLE_MAX_LEN,
)


# pylint: disable=too-few-public-methods
class JSDate:
    def __init__(self, utc_timestamp):
        self.utc_timestamp = utc_timestamp

    def to_locale_str(self):
        return markupsafe.Markup(
            f"<script>document.write(new Date('{self.utc_timestamp}').toLocaleString(navigator.language));</script>"  # pylint: disable=line-too-long
        )


def _get_next_unanswered_question(quiz_progress):
    next_question_id = None
    for row in quiz_progress:
        if row.qui_question_id is None:
            next_question_id = row.question_id
            break
    return next_question_id


def _create_full_quiz_object(full_quiz_rows):
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
    return full_quiz


def _check_question_fields(answers: list, question_name: str):
    invalid_answer_amount = len(answers) < ANSWERS_MIN or len(answers) > ANSWERS_MAX
    invalid_question_len = (
        len(question_name) == 0 or len(question_name) > QUESTION_MAX_LEN
    )
    invalid_answer_len = (
        len(
            [txt for txt, corr in answers if len(txt) > ANSWER_MAX_LEN or len(txt) == 0]
        )
        > 0
    )
    if invalid_answer_amount or invalid_answer_len or invalid_question_len:
        message = ""
        message += (
            f"Must have {ANSWERS_MIN} to {ANSWERS_MAX} answer options\n"
            if invalid_answer_amount
            else ""
        )
        message += (
            f"Question cannot be empty or longer than {QUESTION_MAX_LEN} characters\n"
            if invalid_question_len
            else ""
        )
        message += (
            f"Answer cannot be empty or longer than {ANSWER_MAX_LEN} characters"
            if invalid_answer_len
            else ""
        )
        raise BadRequest(description=message)


def _check_quiz_fields(title: str, description: str):
    if len(title) == 0 or len(title) > QUIZ_TITLE_MAX_LEN:
        message = f"Title can be max {QUIZ_TITLE_MAX_LEN} characters long"
        raise BadRequest(description=message)
    if len(description) == 0 or len(description) > QUIZ_DESC_MAX_LEN:
        message = f"Description can be max {QUIZ_DESC_MAX_LEN} characters long"
        raise BadRequest(description=message)
