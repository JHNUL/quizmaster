from flask import redirect, session
from src.app import app


@app.route("/logout", methods=["POST"])
def logout():
    if "username" in session:
        del session["username"]
    return redirect("/login")
