import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "private.db"

def init_private_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        duid TEXT PRIMARY KEY,
        enc_name TEXT,
        enc_dob TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS derived_attributes (
        duid TEXT PRIMARY KEY,
        is_adult INTEGER,
        is_student INTEGER,
        is_health_eligible INTEGER
    )
    """)

    conn.commit()
    conn.close()

def store_user(duid, enc_name, enc_dob, is_adult, is_student, is_health_eligible):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
        (duid, enc_name, enc_dob)
    )

    cur.execute(
        "INSERT OR REPLACE INTO derived_attributes VALUES (?, ?, ?, ?)",
        (duid, is_adult, is_student, is_health_eligible)
    )

    conn.commit()
    conn.close()

def get_derived_attributes(duid):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT is_adult, is_student, is_health_eligible FROM derived_attributes WHERE duid = ?",
        (duid,)
    )
    row = cur.fetchone()
    conn.close()
    return row
