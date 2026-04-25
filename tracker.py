import sqlite3
from datetime import datetime


class Tracker:
    def __init__(self, db_path: str = "uploaded.db"):
        self._conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT NOT NULL,
                md5_hash TEXT NOT NULL UNIQUE,
                uploaded_at TEXT NOT NULL
            )
        """)
        self._conn.commit()

    def is_uploaded(self, md5_hash: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM uploads WHERE md5_hash = ?", (md5_hash,)
        ).fetchone()
        return row is not None

    def mark_uploaded(self, filepath: str, md5_hash: str):
        try:
            self._conn.execute(
                "INSERT INTO uploads (filepath, md5_hash, uploaded_at) VALUES (?, ?, ?)",
                (filepath, md5_hash, datetime.utcnow().isoformat())
            )
            self._conn.commit()
        except sqlite3.IntegrityError:
            pass  # already recorded, safe to ignore

    def close(self):
        self._conn.close()
