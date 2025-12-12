import db

ITEM_COLUMNS = "id, user_id, title, genre, age_rating, description, year, created_at"

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
               OR i.description LIKE ?
               OR CAST(i.year AS TEXT) LIKE ?
            ORDER BY i.created_at DESC
        """
        return db.query(sql, [like, like, like, like])
    sql = base + " ORDER BY i.created_at DESC"
    return db.query(sql, [])

def get_item(item_id: int):
    sql = f"SELECT {ITEM_COLUMNS} FROM items WHERE id = ?"
    rows = db.query(sql, [item_id])
    return rows[0] if rows else None

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