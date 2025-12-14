import db

ITEM_COLUMNS = (
    "i.id AS id, i.user_id, i.title, i.genre, i.age_rating, "
    "i.description, i.year, i.created_at"
)

def list_items(search: str):
    base = f"""
        SELECT {ITEM_COLUMNS}, u.username
        FROM items i
        JOIN users u ON u.id = i.user_id
    """
    if search:
        like = f"%{search}%"
        sql = base + """
            WHERE i.title LIKE ?
               OR i.genre LIKE ?
               OR i.age_rating LIKE ?
               OR i.description LIKE ?
               OR CAST(i.year AS TEXT) LIKE ?
               OR i.id IN (
                    SELECT it.item_id FROM item_tags it
                    JOIN tags t ON t.id = it.tag_id
                    WHERE t.name_fi LIKE ?
               )
            ORDER BY i.created_at DESC
        """
        return db.query(sql, [like, like, like, like, like, like])
    sql = base + " ORDER BY i.created_at DESC"
    return db.query(sql, [])

def get_item(item_id: int):
    sql = """
        SELECT i.id, i.user_id, i.title, i.genre, i.age_rating,
               i.description, i.year, i.created_at, u.username
          FROM items i
          JOIN users u ON u.id = i.user_id
         WHERE i.id = ?
    """
    rows = db.query(sql, [item_id])
    return rows[0] if rows else None

def list_tags():
    return db.query("SELECT id, name_fi FROM tags ORDER BY name_fi", [])

def list_tags_for_item(item_id: int):
    sql = """
                SELECT t.id, t.name_fi
          FROM item_tags it
          JOIN tags t ON t.id = it.tag_id
         WHERE it.item_id = ?
         ORDER BY t.name_fi
    """
    return db.query(sql, [item_id])

def set_item_tags(item_id: int, tag_ids):
    db.execute("DELETE FROM item_tags WHERE item_id = ?", [item_id])
    for tid in tag_ids:
        db.execute("INSERT OR IGNORE INTO item_tags (item_id, tag_id) VALUES (?, ?)", [item_id, tid])

def create_item(user_id, title, genre, age_rating, description, year):
    sql = """
        INSERT INTO items (user_id, title, genre, age_rating, description, year)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    db.execute(sql, [user_id, title, genre, age_rating, description, year])

def update_item(item_id, title, genre, age_rating, description, year):
    sql = """
        UPDATE items
           SET title = ?, genre = ?, age_rating = ?, description = ?, year = ?
         WHERE id = ?
    """
    db.execute(sql, [title, genre, age_rating, description, year, item_id])

def delete_item(item_id):
    db.execute("DELETE FROM items WHERE id = ?", [item_id])