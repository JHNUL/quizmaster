from os import getenv
from flask import Flask
from src.routes.utils import JSDate

app = Flask(__name__, instance_relative_config=True)
app.secret_key = getenv("SECRET_KEY")
app.jinja_env.globals['JSDate'] = JSDate

# Must be after app initialization
# pylint: disable=wrong-import-position,unused-import
import src.routes.landingpage
import src.routes.register
import src.routes.login
import src.routes.logout
import src.routes.quiz
import src.routes.attempt
