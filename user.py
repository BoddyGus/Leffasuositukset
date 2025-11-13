from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import db

user_bp = Blueprint("user_bp", __name__)


def current_username():
    return session.get("username")


def current_user_id():
    username = current_username()
    if not username:
        return None
    rows = db.query("SELECT id FROM users WHERE username = ?", [username])
    return rows[0]["id"] if rows else None


@user_bp.route("/register")
def register():
    return render_template("register.html")


@user_bp.route("/create", methods=["POST"])
def create():
    username = request.form["username"].strip()
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not username:
        return "VIRHE: tunnus puuttuu"
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except Exception:
        return "VIRHE: tunnus on jo varattu"

    return redirect(url_for("user_bp.login"))


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"].strip()
    password = request.form["password"]

    rows = db.query("SELECT id, password_hash FROM users WHERE username = ?", [username])
    if not rows:
        return "VIRHE: väärä tunnus tai salasana"

    password_hash = rows[0]["password_hash"]
    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect(url_for("reviews_bp.index"))
    else:
        return "VIRHE: väärä tunnus tai salasana"


@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("reviews_bp.index"))


def init_user(app):
    app.register_blueprint(user_bp)
