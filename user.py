from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import db
from queries.user_queries import create_user, find_user_credentials, find_user_id
from flask import flash

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
        flash("Tunnus puuttuu", "error")
        return render_template("register.html")
    if password1 != password2:
        flash("Salasanat eivät ole samat", "error")
        return render_template("register.html")

    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except Exception:
        flash("Tunnus on jo varattu", "error")
        return render_template("register.html")

    flash("Käyttäjä luotu onnistuneesti. Kirjaudu sisään.", "success")
    return redirect(url_for("user_bp.login"))

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"].strip()
    password = request.form["password"]

    rows = db.query("SELECT id, password_hash FROM users WHERE username = ?", [username])
    if not rows or not check_password_hash(rows[0]["password_hash"], password):
        flash("Väärä tunnus tai salasana", "error")
        return render_template("login.html")

    session["username"] = username
    flash("Kirjautuminen onnistui", "success")
    return redirect(url_for("reviews_bp.index"))

@user_bp.route("/users/<username>")
def profile(username):
    # hae käyttäjä-id
    rows = db.query("SELECT id FROM users WHERE username = ?", [username])
    if not rows:
        flash("Käyttäjää ei löytynyt", "error")
        return redirect(url_for("reviews_bp.index"))
    uid = rows[0]["id"]

    # tilastot ja lista
    count_rows = db.query("SELECT COUNT(*) AS movie_count FROM items WHERE user_id = ?", [uid])
    movie_count = count_rows[0]["movie_count"] if count_rows else 0

    movies = db.query(
        "SELECT id, title, genre, year, created_at FROM items WHERE user_id = ? ORDER BY created_at DESC",
        [uid]
    )

    return render_template("user_profile.html", username=username, movie_count=movie_count, movies=movies)
@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Kirjauduit ulos", "success")
    return redirect(url_for("reviews_bp.index"))


def init_user(app):
    app.register_blueprint(user_bp)
