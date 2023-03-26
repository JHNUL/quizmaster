from os import getenv
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.secret_key = getenv("SECRET_KEY")

# Must be after app initialization
# pylint: disable=wrong-import-position,unused-import
import src.routes.landingpage
import src.routes.register
import src.routes.login
import src.routes.logout
import src.routes.quiz
import src.routes.attempt
