from jinja2.utils import markupsafe


# pylint: disable=too-few-public-methods
class JSDate:
    def __init__(self, utc_timestamp):
        self.utc_timestamp = utc_timestamp

    def to_locale_str(self):
        return markupsafe.Markup(
            f"<script>document.write(new Date('{self.utc_timestamp}').toLocaleString(navigator.language));</script>"  # pylint: disable=line-too-long
        )
