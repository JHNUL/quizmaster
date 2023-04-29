from flask import redirect, session
from src.app import app


@app.route("/logout", methods=["POST"])
def logout():
    if "username" in session:
        del session["username"]
    if "user_id" in session:
        del session["user_id"]
    if "csrf_token" in session:
        del session["csrf_token"]
    return redirect("/login")
