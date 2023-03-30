from flask_sqlalchemy import SQLAlchemy
from os import getenv
from src.app import app

# Rage-inducing hack to serve the fly.io postgres cluster
# non-configurable connection string to SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
if getenv("LOG_LEVEL") == "debug":
    app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
