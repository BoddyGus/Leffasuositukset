CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    genre TEXT,
    description TEXT,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS item_reviews (
    id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (item_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_item_reviews_item ON item_reviews(item_id);
CREATE INDEX IF NOT EXISTS idx_item_reviews_user ON item_reviews(user_id);