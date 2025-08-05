import sqlite3
from pathlib import Path

DB_PATH = Path.home() / '.ai_sport_agent' / 'data.db'

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY,
        file TEXT UNIQUE,
        date TEXT,
        mode TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS intervals (
        id INTEGER PRIMARY KEY,
        session_id INTEGER,
        type TEXT,
        start TEXT,
        end TEXT,
        duration REAL,
        avg_power REAL,
        FOREIGN KEY(session_id) REFERENCES sessions(id)
    )
    """)
    conn.commit()
    conn.close()

