from flask import render_template
from src.app import app
from src.services.users import get_user


@app.route("/")
def index():
    a = ["Castor", "Pollux", "Troy"]
    r = get_user(2)
    print(f"Got user id 2 {r}")
    return render_template("index.html", items=a, message="FOOOOOO")
