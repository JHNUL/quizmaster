from flask import render_template
from src.app import app


@app.route("/", methods=["GET"])
def landingpage():
    return render_template("index.html")
