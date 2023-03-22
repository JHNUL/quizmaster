from flask import render_template
from src.app import app
from src.routes.decorators import login_required


@app.route("/", methods=["GET"])
@login_required
def landingpage():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return "ok"
