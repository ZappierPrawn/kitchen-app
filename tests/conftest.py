import pytest
import sqlite3

from src import inventory

@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    # 1) Create a fresh DB file path
    db_file = tmp_path / "inventory.db"

    # 2) Monkey-patch the module’s DB_PATH
    monkeypatch.setattr(inventory, "DB_PATH", str(db_file))

    # 3) Init schema without AUTOINCREMENT
    conn = sqlite3.connect(str(db_file))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id       INTEGER PRIMARY KEY,
            name     TEXT    UNIQUE NOT NULL,
            quantity REAL    NOT NULL,
            unit     TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    return str(db_file)
