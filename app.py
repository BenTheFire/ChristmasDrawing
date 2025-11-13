from flask import Flask, request, redirect, session, url_for, render_template
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change_this_secret_for_prod")

DATA_PATH = "./data.json"

DEFAULT_DATA = {
    "users": [
        {"username": "Ben", "password": "pw1", "reveal": "You got: Matthew!"},
        {"username": "Matthew", "password": "pw2", "reveal": "You got: Luke!"},
        {"username": "Jhonny", "password": "pw3", "reveal": "You got: Ben!"},
    ]
}

def ensure_data():
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, indent=2)

def load_users():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("users", [])

def find_user(username):
    users = load_users()
    for u in users:
        if u.get("username") == username:
            return u
    return None

ensure_data()

@app.route("/", methods=["GET"])
def index():
    if session.get("username"):
        return redirect(url_for("box"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = find_user(username)
        if not user or user.get("password") != password:
            error = "Invalid username or password."
        else:
            session["username"] = username
            return redirect(url_for("box"))
    return render_template("login.html", error=error)

@app.route("/box", methods=["GET"])
def box():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))
    user = find_user(username)
    if not user:
        session.pop("username", None)
        return redirect(url_for("login"))
    reveal_text = user.get("reveal", "No reveal text set.")
    return render_template("box.html", user=username, reveal_text=reveal_text)

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)