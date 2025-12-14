"""Database helper functions for SQLite access."""

import sqlite3
from flask import g


def get_connection():
    """Return a new SQLite connection with foreign keys enabled."""
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=None):
    """Execute a write query and store last inserted row id in ``g``."""
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()


def last_insert_id():
    """Return the last inserted row id from the current request context."""
    return getattr(g, "last_insert_id", None)


def query(sql, params=None):
    """Run a SELECT query and return all rows."""
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
