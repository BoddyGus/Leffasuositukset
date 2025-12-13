import db

REVIEW_COLUMNS = "id, item_id, user_id, rating, comment, created_at"

def list_reviews_for_item(item_id: int):
    sql = f"""
        SELECT r.id, r.item_id, r.user_id, r.rating, r.comment, r.created_at, u.username
          FROM item_reviews r
          JOIN users u ON u.id = r.user_id
         WHERE r.item_id = ?
         ORDER BY r.created_at DESC
    """
    return db.query(sql, [item_id])

def get_avg_for_item(item_id: int):
    sql = (
        "SELECT AVG(rating) AS avg_rating, COUNT(*) AS review_count "
        "FROM item_reviews WHERE item_id = ?"
    )
    rows = db.query(sql, [item_id])
    return rows[0] if rows else {"avg_rating": None, "review_count": 0}

def find_user_review(item_id: int, user_id: int):
    sql = f"SELECT {REVIEW_COLUMNS} FROM item_reviews WHERE item_id = ? AND user_id = ?"
    rows = db.query(sql, [item_id, user_id])
    return rows[0] if rows else None

def create_review(item_id: int, user_id: int, rating: int, comment: str):
    sql = "INSERT INTO item_reviews (item_id, user_id, rating, comment) VALUES (?, ?, ?, ?)"
    db.execute(sql, [item_id, user_id, rating, comment])