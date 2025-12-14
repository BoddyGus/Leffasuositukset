from flask import Blueprint, render_template, request, redirect, session, url_for
from datetime import datetime
import db
from user import current_username, current_user_id
from queries.review_queries import (
    list_reviews_for_item,
    get_avg_for_item,
    find_user_review,
    create_review,
)
from queries.item_queries import (
    get_item,
    list_items as list_items_query,
    list_tags,
    list_tags_for_item,
    set_item_tags,
)
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

ALLOWED_AGE_RATINGS = {
    "U": "Sallittu kaikenikäisille",
    "PG": "Vanhempien harkinta suositeltavaa",
    "12": "Kielletty alle 12-vuotiailta",
    "15": "Kielletty alle 15-vuotiailta",
    "18": "Kielletty alle 18-vuotiailta",
}

reviews_bp = Blueprint("reviews_bp", __name__)


@reviews_bp.route("/")
def index():
    search_query = request.args.get("q", "").strip()
    items = [dict(row) for row in list_items_query(search_query)]
    for item in items:
        item["tags"] = list_tags_for_item(item["id"])
    return render_template("index.html", items=items, q=search_query)


@reviews_bp.route("/about")
def about():
    return render_template("about.html")


@reviews_bp.route("/new_item")
def new_item():
    if not current_username():
        return redirect(url_for("user_bp.login"))
    tags = list_tags()
    current_year = datetime.now().year
    return render_template(
        "new_item.html",
        allowed_genres=ALLOWED_GENRES,
        tags=tags,
        current_year=current_year,
    )


@reviews_bp.route("/items/create", methods=["POST"])
def items_create():
    check_csrf()
    if not current_username():
        return redirect(url_for("user_bp.login"))

    title = request.form.get("title", "").strip()
    genre = request.form.get("genre", "").strip()
    age_rating = request.form.get("age_rating", "").strip()
    year = request.form.get("year", "").strip()
    description = request.form.get("description", "").strip()
    tag_ids_raw = request.form.getlist("tags")

    if not title:
        return "VIRHE: nimi puuttuu"
    if not genre:
        return "VIRHE: genre on pakollinen"
    if not age_rating:
        return "VIRHE: ikäraja on pakollinen"
    if not year:
        return "VIRHE: vuosi on pakollinen"

    try:
        yval = int(year)
    except ValueError:
        return "VIRHE: vuosi ei ole numero"

    MAX_TITLE_LEN = 75
    if len(title) > MAX_TITLE_LEN:
        return f"VIRHE: nimi on liian pitkä (max {MAX_TITLE_LEN} merkkiä)"

    current_year = datetime.now().year
    if yval > current_year:
        return f"VIRHE: vuosi ei voi olla tulevaisuudessa (max {current_year})"

    uid = current_user_id()
    if not uid:
        return "VIRHE: käyttäjää ei löytynyt"

    if genre and genre not in ALLOWED_GENRES:
        return "VIRHE: genre ei ole sallittu. Sallitut genret: " + ", ".join(ALLOWED_GENRES)
    if age_rating and age_rating not in ALLOWED_AGE_RATINGS:
        return "VIRHE: ikäraja ei ole sallittu. Sallitut: " + ", ".join(ALLOWED_AGE_RATINGS.keys())

    if description and len(description) > 350:
        return "VIRHE: kuvaus on liian pitkä (max 350 merkkiä)"
    if description and description.count("\n") > 9:
        return "VIRHE: kuvaus saa sisältää enintään 10 riviä"

    all_tags = {str(t["id"]): t for t in list_tags()}
    for tid in tag_ids_raw:
        if tid not in all_tags:
            return "VIRHE: tuntematon tunniste tagille"

    sql = """
        INSERT INTO items (user_id, title, genre, age_rating, description, year)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    db.execute(sql, [uid, title, genre, age_rating, description, yval])
    item_id = db.last_insert_id()
    set_item_tags(item_id, [int(tid) for tid in tag_ids_raw])
    return redirect(url_for("reviews_bp.index"))


@reviews_bp.route("/items/<int:item_id>/edit")
def items_edit(item_id):
    if not current_username():
        return redirect(url_for("user_bp.login"))

    rows = db.query(
        "SELECT id, user_id, title, genre, age_rating, description, year, created_at "
        "FROM items WHERE id = ?",
        [item_id],
    )

    if not rows:
        return "VIRHE: tietokohdetta ei löytynyt"
    item = rows[0]
    if item["user_id"] != current_user_id():
        return "VIRHE: ei oikeuksia muokata"

    tags = list_tags()
    selected_tags = list_tags_for_item(item_id)
    selected_ids = {t["id"] for t in selected_tags}
    current_year = datetime.now().year
    return render_template(
        "edit_item.html",
        item=item,
        allowed_genres=ALLOWED_GENRES,
        tags=tags,
        selected_tag_ids=selected_ids,
        current_year=current_year,
    )


@reviews_bp.route("/items/<int:item_id>/update", methods=["POST"])
def items_update(item_id):
    check_csrf()
    if not current_username():
        return redirect(url_for("user_bp.login"))

    rows = db.query("SELECT user_id FROM items WHERE id = ?", [item_id])
    if not rows:
        return "VIRHE: tietokohdetta ei löytynyt"
    if rows[0]["user_id"] != current_user_id():
        return "VIRHE: ei oikeuksia muokata"

    title = request.form.get("title", "").strip()
    genre = request.form.get("genre", "").strip()
    age_rating = request.form.get("age_rating", "").strip()
    year = request.form.get("year", "").strip()
    description = request.form.get("description", "").strip()
    tag_ids_raw = request.form.getlist("tags")

    if not title:
        return "VIRHE: nimi puuttuu"
    if not genre:
        return "VIRHE: genre on pakollinen"
    if not age_rating:
        return "VIRHE: ikäraja on pakollinen"
    if not year:
        return "VIRHE: vuosi on pakollinen"

    try:
        yval = int(year)
    except ValueError:
        return "VIRHE: vuosi ei ole numero"

    MAX_TITLE_LEN = 75
    if len(title) > MAX_TITLE_LEN:
        return f"VIRHE: nimi on liian pitkä (max {MAX_TITLE_LEN} merkkiä)"

    current_year = datetime.now().year
    if yval > current_year:
        return f"VIRHE: vuosi ei voi olla tulevaisuudessa (max {current_year})"

    if genre and genre not in ALLOWED_GENRES:
        return "VIRHE: genre ei ole sallittu. Sallitut genret: " + ", ".join(ALLOWED_GENRES)
    if age_rating and age_rating not in ALLOWED_AGE_RATINGS:
        return "VIRHE: ikäraja ei ole sallittu. Sallitut: " + ", ".join(ALLOWED_AGE_RATINGS.keys())

    if description and len(description) > 350:
        return "VIRHE: kuvaus on liian pitkä (max 350 merkkiä)"
    if description and description.count("\n") > 9:
        return "VIRHE: kuvaus saa sisältää enintään 10 riviä"

    all_tags = {str(t["id"]): t for t in list_tags()}
    for tid in tag_ids_raw:
        if tid not in all_tags:
            return "VIRHE: tuntematon tunniste tagille"

    sql = """
        UPDATE items
            SET title = ?, genre = ?, age_rating = ?, description = ?, year = ?
         WHERE id = ?
        """
    db.execute(sql, [title, genre, age_rating, description, yval, item_id])
    set_item_tags(item_id, [int(tid) for tid in tag_ids_raw])
    return redirect(url_for("reviews_bp.index"))


@reviews_bp.route("/items/<int:item_id>/delete", methods=["POST"])
def items_delete(item_id):
    check_csrf()
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
    row = get_item(item_id)
    if row:
        item = dict(row)
    else:
        item = None
    if not item:
        flash("Kohdetta ei löytynyt", "error")
        return redirect(url_for("reviews_bp.index"))

    item_tags = list_tags_for_item(item_id)

    reviews = list_reviews_for_item(item_id)
    avg = get_avg_for_item(item_id)
    my_review = None
    uid = current_user_id()
    if uid:
        my_review = find_user_review(item_id, uid)

    rating_label = None
    try:
        rating_label = ALLOWED_AGE_RATINGS.get(item["age_rating"])
    except Exception:
        rating_label = None

    return render_template(
        "item_detail.html",
        item=item,
        age_rating_label=rating_label,
        item_tags=item_tags,
        reviews=reviews,
        avg_rating=avg["avg_rating"],
        review_count=avg["review_count"],
        my_review=my_review,
    )
@reviews_bp.route("/items/<int:item_id>/reviews/create", methods=["POST"])
def reviews_create(item_id):
    check_csrf()
    item = get_item(item_id)
    if not item:
        flash("Kohdetta ei löytynyt", "error")
        return redirect(url_for("reviews_bp.index"))

    uid = current_user_id()
    if not uid:
        flash("Kirjaudu ensin", "error")
        return redirect(url_for("user_bp.login"))

    rating_raw = request.form.get("rating", "").strip()
    comment = request.form.get("comment", "").strip()

    try:
        rating = int(rating_raw)
    except ValueError:
        flash("Arvosana on pakollinen", "error")
        return redirect(url_for("reviews_bp.items_show", item_id=item_id))

    if rating < 1 or rating > 5:
        flash("Arvosanan tulee olla 1–5", "error")
        return redirect(url_for("reviews_bp.items_show", item_id=item_id))

    if comment and len(comment) > 350:
        flash("Kommentti on liian pitkä (max 350 merkkiä)", "error")
        return redirect(url_for("reviews_bp.items_show", item_id=item_id))
    if comment and comment.count("\n") > 9:
        flash("Kommentti saa sisältää enintään 10 riviä", "error")
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