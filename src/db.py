from os import getenv
from flask_sqlalchemy import SQLAlchemy
from src.app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
if getenv("LOG_LEVEL") == "debug":
    app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
