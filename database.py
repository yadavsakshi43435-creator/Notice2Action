import sqlite3
import json
import hashlib
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

    # Check whether hash column already exists
    cursor.execute("PRAGMA table_info(notices)")
    columns = [row[1] for row in cursor.fetchall()]

    if "extracted_text_hash" not in columns:
        cursor.execute("""
            ALTER TABLE notices
            ADD COLUMN extracted_text_hash TEXT
        """)

    # Generate hashes for previously saved notices
    cursor.execute("""
        SELECT id, extracted_text
        FROM notices
        WHERE extracted_text_hash IS NULL
    """)

    old_notices = cursor.fetchall()

    for notice_id, extracted_text in old_notices:
        if extracted_text:
            notice_hash = hashlib.sha256(
                extracted_text.strip().encode("utf-8")
            ).hexdigest()

            cursor.execute("""
                UPDATE notices
                SET extracted_text_hash = ?
                WHERE id = ?
            """, (notice_hash, notice_id))

    conn.commit()
    conn.close()


def save_notice(title, filename, extracted_text, analysis):

    # Generate unique hash for notice content
    notice_hash = hashlib.sha256(
        extracted_text.strip().encode("utf-8")
    ).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether the same notice already exists
    cursor.execute("""
        SELECT id FROM notices
        WHERE extracted_text_hash = ?
    """, (notice_hash,))

    existing_notice = cursor.fetchone()

    if existing_notice:
        conn.close()
        return False

    # Insert new notice
    cursor.execute("""
        INSERT INTO notices
        (title, filename, extracted_text, dates,
         fees, instructions, status, created_at,
         extracted_text_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        filename,
        extracted_text,
        json.dumps(analysis.get("dates", [])),
        json.dumps(analysis.get("fees", [])),
        json.dumps(analysis.get("instructions", [])),
        "Pending",
        datetime.now().isoformat(timespec="seconds"),
        notice_hash
    ))

    conn.commit()
    conn.close()

    return True


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