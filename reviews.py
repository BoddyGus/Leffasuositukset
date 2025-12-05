from flask import Blueprint, render_template, request, redirect, session, url_for
import db
from user import current_username, current_user_id
from queries.review_queries import list_reviews_for_item, get_avg_for_item, find_user_review, create_review
from queries.item_queries import get_item
from queries.user_queries import find_user_id
from app import check_csrf
from flask import flash

ALLOWED_GENRES = [
    "toiminta",
    "komedia",
    "draama",
    "kauhu",
    "scifi",
    "fantasia",
    "seikkailu",
    "trilleri",
    "animaatio",
    "dokumentti",
    "romantiikka",
]

reviews_bp = Blueprint("reviews_bp", __name__)


@reviews_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    params = []
    base_sql = """
        SELECT i.id, i.title, i.genre, i.description, i.year, i.user_id, i.created_at, u.username
        FROM items i
        JOIN users u ON u.id = i.user_id
    """
    if q:
        sql = base_sql + """
            WHERE i.title LIKE ?
               OR i.genre LIKE ?
               OR i.description LIKE ?
               OR CAST(i.year AS TEXT) LIKE ?
            ORDER BY i.created_at DESC
        """
        like = f"%{q}%"
        params = [like, like, like, like]
    else:
        sql = base_sql + " ORDER BY i.created_at DESC"

    items = db.query(sql, params)
    return render_template("index.html", items=items, q=q)


@reviews_bp.route("/new_item")
def new_item():
    if not current_username():
        return redirect(url_for("user_bp.login"))
    return render_template("new_item.html", allowed_genres=ALLOWED_GENRES)


@reviews_bp.route("/items/create", methods=["POST"])
def items_create():
    if not current_username():
        return redirect(url_for("user_bp.login"))

    title = request.form.get("title", "").strip()
    genre = request.form.get("genre", "").strip()
    year = request.form.get("year", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        return "VIRHE: nimi puuttuu"
    if not genre:
        return "VIRHE: genre on pakollinen"

    try:
        yval = int(year) if year else None
    except ValueError:
        return "VIRHE: vuosi ei ole numero"

    uid = current_user_id()
    if not uid:
        return "VIRHE: käyttäjää ei löytynyt"

    if genre and genre not in ALLOWED_GENRES:
        return "VIRHE: genre ei ole sallittu. Sallitut genret: " + ", ".join(ALLOWED_GENRES)

    sql = """
        INSERT INTO items (user_id, title, genre, description, year)
        VALUES (?, ?, ?, ?, ?)
    """
    db.execute(sql, [uid, title, genre, description, yval])
    return redirect(url_for("reviews_bp.index"))


@reviews_bp.route("/items/<int:item_id>/edit")
def items_edit(item_id):
    if not current_username():
        return redirect(url_for("user_bp.login"))

    rows = db.query(
    "SELECT id, user_id, title, genre, description, year, created_at FROM items WHERE id = ?",
    [item_id]
    )

    if not rows:
        return "VIRHE: tietokohdetta ei löytynyt"
    item = rows[0]
    if item["user_id"] != current_user_id():
        return "VIRHE: ei oikeuksia muokata"

    return render_template("edit_item.html", item=item, allowed_genres=ALLOWED_GENRES)


@reviews_bp.route("/items/<int:item_id>/update", methods=["POST"])
def items_update(item_id):
    if not current_username():
        return redirect(url_for("user_bp.login"))

    rows = db.query("SELECT user_id FROM items WHERE id = ?", [item_id])
    if not rows:
        return "VIRHE: tietokohdetta ei löytynyt"
    if rows[0]["user_id"] != current_user_id():
        return "VIRHE: ei oikeuksia muokata"

    title = request.form.get("title", "").strip()
    genre = request.form.get("genre", "").strip()
    year = request.form.get("year", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        return "VIRHE: nimi puuttuu"
    if not genre:
        return "VIRHE: genre on pakollinen"

    try:
        yval = int(year) if year else None
    except ValueError:
        return "VIRHE: vuosi ei ole numero"

    if genre and genre not in ALLOWED_GENRES:
        return "VIRHE: genre ei ole sallittu. Sallitut genret: " + ", ".join(ALLOWED_GENRES)

    sql = """
        UPDATE items
           SET title = ?, genre = ?, description = ?, year = ?
         WHERE id = ?
    """
    db.execute(sql, [title, genre, description, yval, item_id])
    return redirect(url_for("reviews_bp.index"))


@reviews_bp.route("/items/<int:item_id>/delete", methods=["POST"])
def items_delete(item_id):
    if not current_username():
        return redirect(url_for("user_bp.login"))

    rows = db.query("SELECT user_id FROM items WHERE id = ?", [item_id])
    if not rows:
        return "VIRHE: tietokohdetta ei löytynyt"
    if rows[0]["user_id"] != current_user_id():
        return "VIRHE: ei oikeuksia poistaa"

    db.execute("DELETE FROM items WHERE id = ?", [item_id])
    return redirect(url_for("reviews_bp.index"))

@reviews_bp.route("/items/<int:item_id>")
def items_show(item_id):
    item = get_item(item_id)
    if not item:
        flash("Kohdetta ei löytynyt", "error")
        return redirect(url_for("reviews_bp.index"))

    reviews = list_reviews_for_item(item_id)
    avg = get_avg_for_item(item_id)
    my_review = None
    uid = current_user_id()
    if uid:
        my_review = find_user_review(item_id, uid)

    return render_template(
        "item_detail.html",
        item=item,
        reviews=reviews,
        avg_rating=avg["avg_rating"],
        review_count=avg["review_count"],
        my_review=my_review,
    )
@reviews_bp.route("/items/<int:item_id>/reviews/create", methods=["POST"])
def reviews_create(item_id):
    item = get_item(item_id)
    if not item:
        flash("Kohdetta ei löytynyt", "error")
        return redirect(url_for("reviews_bp.index"))

    uid = current_user_id()
    if not uid:
        flash("Kirjaudu ensin", "error")
        return redirect(url_for("user_bp.login"))

    rating_raw = request.form.get("rating", "").strip()
    comment = request.form.get("comment", "")

    try:
        rating = int(rating_raw)
    except ValueError:
        flash("Arvosana on pakollinen", "error")
        return redirect(url_for("reviews_bp.items_show", item_id=item_id))

    if rating < 1 or rating > 5:
        flash("Arvosanan tulee olla 1–5", "error")
        return redirect(url_for("reviews_bp.items_show", item_id=item_id))

    if find_user_review(item_id, uid):
        flash("Olet jo arvostellut tämän elokuvan", "error")
        return redirect(url_for("reviews_bp.items_show", item_id=item_id))

    try:
        create_review(item_id, uid, rating, comment)
    except Exception:
        flash("Arvostelun tallennus epäonnistui", "error")
        return redirect(url_for("reviews_bp.items_show", item_id=item_id))

    flash("Arvostelu tallennettu", "success")
    return redirect(url_for("reviews_bp.items_show", item_id=item_id))

def init_reviews(app):
    app.register_blueprint(reviews_bp)

def current_username():
    return session.get("username")

def current_user_id():
    username = current_username()
    if not username:
        return None
    return find_user_id(username)