from jinja2.utils import markupsafe


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
