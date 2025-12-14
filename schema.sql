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
    age_rating TEXT,
    description TEXT,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_items_user ON items(user_id);

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

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    name_fi TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS item_tags (
    item_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (item_id, tag_id),
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

INSERT OR IGNORE INTO tags (name_fi) VALUES
    ('Nostattava'),
    ('Lämmittävä'),
    ('Hauska'),
    ('Seikkailullinen'),
    ('Jännittävä'),
    ('Kireä'),
    ('Synkkä'),
    ('Ajatuksia herättävä'),
    ('Tunteikas'),
    ('Romanttinen');