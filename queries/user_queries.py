from typing import Optional
import db

def find_user_credentials(username: str):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    return db.query(sql, [username])

def create_user(username: str, password_hash: str) -> bool:
    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            [username, password_hash]
        )
        return True
    except Exception:
        return False

def find_user_id(username: str) -> Optional[int]:
    rows = db.query("SELECT id FROM users WHERE username = ?", [username])
    return rows[0]["id"] if rows else None