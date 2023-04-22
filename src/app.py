from os import getenv
from flask import Flask
from src.routes.utils import JSDate

app = Flask(__name__, instance_relative_config=True)
app.config['MAX_CONTENT_LENGTH'] = 1024**2
app.secret_key = getenv("SECRET_KEY")
# pylint: disable=no-member
app.jinja_env.globals['JSDate'] = JSDate

# Must be after app initialization
# pylint: disable=wrong-import-position,unused-import
import src.routes.landingpage
import src.routes.register
import src.routes.login
import src.routes.logout
import src.routes.quiz
import src.routes.attempt
import src.routes.stats
