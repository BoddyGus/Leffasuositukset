import random
import string
from datetime import datetime

import sqlite3

DB_PATH = "database.db"

GENRES = [
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

AGE_RATINGS = ["U", "PG", "12", "15", "18"]


def random_text(max_len: int) -> str:
    words = []
    while True:
        word = "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        if len(" ".join(words + [word])) > max_len:
            break
        words.append(word)
        if len(words) >= 40:
            break
    text = " ".join(words)
    chunks = [text[i : i + max_len // 3] for i in range(0, len(text), max_len // 3 or 1)]
    return "\n".join(chunks[:5])


def main(users_count: int = 200, items_count: int = 5000, reviews_count: int = 20000) -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("Clearing existing data…")
    cur.execute("DELETE FROM item_reviews")
    cur.execute("DELETE FROM item_tags")
    cur.execute("DELETE FROM items")
    cur.execute("DELETE FROM users WHERE username LIKE 'testuser_%'")
    conn.commit()

    print(f"Inserting {users_count} users…")
    user_ids = []
    for i in range(users_count):
        username = f"testuser_{i}"
        cur.execute(
            "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
            (username, username),
        )
        user_ids.append(cur.lastrowid)
    conn.commit()

    print(f"Inserting {items_count} items…")
    cur.execute("SELECT id FROM tags")
    tag_ids = [row[0] for row in cur.fetchall()]

    item_ids = []
    for i in range(items_count):
        user_id = random.choice(user_ids)
        title = f"Testielokuva {i}"
        genre = random.choice(GENRES)
        age_rating = random.choice(AGE_RATINGS)
        year = random.randint(1950, datetime.now().year)
        description = random_text(330)
        cur.execute(
            """
            INSERT INTO items (user_id, title, genre, age_rating, description, year)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, title, genre, age_rating, description, year),
        )
        item_ids.append(cur.lastrowid)

        if tag_ids:
            chosen = random.sample(tag_ids, k=random.randint(0, min(4, len(tag_ids))))
            for tag_id in chosen:
                cur.execute(
                    "INSERT OR IGNORE INTO item_tags (item_id, tag_id) VALUES (?, ?)",
                    (cur.lastrowid, tag_id),
                )

    conn.commit()

    print(f"Inserting {reviews_count} reviews…")
    for _ in range(reviews_count):
        item_id = random.choice(item_ids)
        user_id = random.choice(user_ids)
        rating = random.randint(1, 5)
        comment = random_text(300)
        try:
            cur.execute(
                """
                INSERT OR IGNORE INTO item_reviews (item_id, user_id, rating, comment)
                VALUES (?, ?, ?, ?)
                """,
                (item_id, user_id, rating, comment),
            )
        except sqlite3.IntegrityError:
            continue

    conn.commit()
    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
