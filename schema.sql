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

-- Tags (moods) and item-tag join
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    name_fi TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_tags (
    item_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (item_id, tag_id),
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Seed tags (slug, Finnish label)
INSERT OR IGNORE INTO tags (slug, name_fi) VALUES
    ('uplifting', 'Nostattava'),
    ('heartwarming', 'Lämmittävä'),
    ('funny', 'Hauska'),
    ('adventurous', 'Seikkailullinen'),
    ('exciting', 'Jännittävä'),
    ('tense', 'Kireä'),
    ('dark', 'Synkkä'),
    ('thought-provoking', 'Ajatuksia herättävä'),
    ('emotional', 'Tunteikas'),
    ('romantic', 'Romanttinen');