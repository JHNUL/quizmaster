from flask import render_template
from src.app import app


@app.route("/", methods=["GET"])
def landingpage():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return "ok"
