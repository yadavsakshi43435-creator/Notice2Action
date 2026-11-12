
import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "notice2action.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            filename TEXT,
            extracted_text TEXT,
            dates TEXT,
            fees TEXT,
            instructions TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_notice(title, filename, extracted_text, analysis):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notices
        (title, filename, extracted_text, dates,
         fees, instructions, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        filename,
        extracted_text,
        json.dumps(analysis.get("dates", [])),
        json.dumps(analysis.get("fees", [])),
        json.dumps(analysis.get("instructions", [])),
        "Pending",
        datetime.now().isoformat(timespec="seconds")
    ))

    conn.commit()
    conn.close()

def get_all_notices():
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notices ORDER BY id DESC")

    notices = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return notices

def update_notice_status(notice_id, status):
    allowed_statuses = ["Pending", "Completed"]

    if status not in allowed_statuses:
        raise ValueError("Invalid status")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notices SET status = ? WHERE id = ?",
        (status, notice_id)
    )

    conn.commit()
    conn.close()