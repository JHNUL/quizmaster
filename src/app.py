from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Must be after app initialization
# pylint: disable=wrong-import-position,unused-import
import src.routes.routes
