import os
import sqlite3
from pathlib import Path


def get_db_path() -> Path:
    return Path(os.getenv("DB_PATH", "short_url.db"))


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Shorten(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0
            )
            """
        )
        conn.commit()
