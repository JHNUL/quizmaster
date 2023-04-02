from jinja2.utils import markupsafe 


class JSDate(object):
    def __init__(self, utc_timestamp):
        self.utc_timestamp = utc_timestamp

    def to_locale_str(self):
        return markupsafe.Markup(f"<script>document.write(new Date('{self.utc_timestamp}').toLocaleString(navigator.language));</script>")
