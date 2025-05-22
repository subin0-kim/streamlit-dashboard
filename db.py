import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Optional

DB_PATH = Path("file_metadata.db")

@contextmanager
def get_conn(db_path: Path = DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_db(db_path: Path = DB_PATH):
    with get_conn(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE,
                alias TEXT,
                description TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def add_file(filename: str, alias: Optional[str] = None, description: Optional[str] = None, db_path: Path = DB_PATH):
    with get_conn(db_path) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO files (filename, alias, description) VALUES (?, ?, ?)",
            (filename, alias or filename, description or ""),
        )


def get_files(search: Optional[str] = None, db_path: Path = DB_PATH):
    with get_conn(db_path) as conn:
        cursor = conn.cursor()
        if search:
            like = f"%{search}%"
            cursor.execute(
                "SELECT id, filename, alias, description, uploaded_at FROM files WHERE filename LIKE ? OR alias LIKE ? OR description LIKE ? ORDER BY uploaded_at DESC",
                (like, like, like),
            )
        else:
            cursor.execute(
                "SELECT id, filename, alias, description, uploaded_at FROM files ORDER BY uploaded_at DESC"
            )
        rows = cursor.fetchall()
    return rows


def delete_files(ids: Iterable[int], db_path: Path = DB_PATH):
    if not ids:
        return
    with get_conn(db_path) as conn:
        conn.executemany("DELETE FROM files WHERE id=?", [(i,) for i in ids])


def update_file(file_id: int, alias: Optional[str], description: Optional[str], db_path: Path = DB_PATH):
    """Update alias and description for a file entry."""
    with get_conn(db_path) as conn:
        conn.execute(
            "UPDATE files SET alias=?, description=? WHERE id=?",
            (alias, description, file_id),
        )
