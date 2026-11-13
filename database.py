import sqlite3
import json
import hashlib

from pathlib import Path
from datetime import datetime, date


# ==================================
# DATABASE CONFIGURATION
# ==================================

DB_PATH = Path(__file__).resolve().parent / "notice2action.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ==================================
# INITIALIZE DATABASE
# ==================================

def initialize_db():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Notices table
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

        # Check existing columns
        cursor.execute("PRAGMA table_info(notices)")
        columns = [row[1] for row in cursor.fetchall()]

        # Add hash column if missing
        if "extracted_text_hash" not in columns:
            cursor.execute("""
                ALTER TABLE notices
                ADD COLUMN extracted_text_hash TEXT
            """)

        # Generate hashes for old notices
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

        # Individual tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notice_id INTEGER NOT NULL,
                task_title TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                source_text TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TEXT,
                FOREIGN KEY (notice_id)
                    REFERENCES notices(id)
            )
        """)

        # Important dates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS important_dates (
                date_id INTEGER PRIMARY KEY AUTOINCREMENT,
                notice_id INTEGER NOT NULL,
                event_name TEXT,
                event_date TEXT,
                FOREIGN KEY (notice_id)
                    REFERENCES notices(id)
            )
        """)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# ==================================
# SAVE NOTICE
# ==================================

def save_notice(title, filename, extracted_text, analysis):

    notice_hash = hashlib.sha256(
        extracted_text.strip().encode("utf-8")
    ).hexdigest()

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Duplicate check
        cursor.execute("""
            SELECT id
            FROM notices
            WHERE extracted_text_hash = ?
        """, (notice_hash,))

        existing_notice = cursor.fetchone()

        if existing_notice:
            return None

        # Insert notice
        cursor.execute("""
            INSERT INTO notices (
                title,
                filename,
                extracted_text,
                dates,
                fees,
                instructions,
                status,
                created_at,
                extracted_text_hash
            )
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

        notice_id = cursor.lastrowid

        conn.commit()

        return notice_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# ==================================
# GET ALL NOTICES
# ==================================

def get_all_notices():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM notices
            ORDER BY id DESC
        """)

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:
        conn.close()


# ==================================
# UPDATE NOTICE STATUS
# ==================================

def update_notice_status(notice_id, status):

    allowed_statuses = ["Pending", "Completed"]

    if status not in allowed_statuses:
        raise ValueError("Invalid notice status")

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE notices
            SET status = ?
            WHERE id = ?
        """, (status, notice_id))

        conn.commit()

    finally:
        conn.close()


# ==================================
# SAVE INDIVIDUAL TASK
# ==================================

def save_task(
    notice_id,
    task_title,
    description="",
    deadline=None,
    source_text=""
):

    if not task_title or not task_title.strip():
        raise ValueError("Task title cannot be empty")

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM notices
            WHERE id = ?
        """, (notice_id,))

        if cursor.fetchone() is None:
            raise ValueError("Notice not found")

        cursor.execute("""
            INSERT INTO tasks (
                notice_id,
                task_title,
                description,
                deadline,
                source_text,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            notice_id,
            task_title.strip(),
            description,
            deadline,
            source_text,
            "Pending",
            datetime.now().isoformat(timespec="seconds")
        ))

        task_id = cursor.lastrowid

        conn.commit()

        return task_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# ==================================
# SAVE MULTIPLE TASKS
# ==================================

def save_multiple_tasks(notice_id, tasks):

    saved_ids = []

    for task in tasks:

        task_id = save_task(
            notice_id=notice_id,
            task_title=task.get("task_title", "Untitled Task"),
            description=task.get("description", ""),
            deadline=task.get("deadline"),
            source_text=task.get("source_text", "")
        )

        saved_ids.append(task_id)

    return saved_ids


# ==================================
# GET ALL TASKS
# ==================================

def get_all_tasks():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                tasks.*,
                notices.title AS notice_title,
                notices.filename AS notice_filename
            FROM tasks
            JOIN notices
            ON tasks.notice_id = notices.id
            ORDER BY tasks.id DESC
        """)

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:
        conn.close()


# ==================================
# GET TASKS BY NOTICE
# ==================================

def get_tasks_by_notice(notice_id):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tasks
            WHERE notice_id = ?
            ORDER BY id DESC
        """, (notice_id,))

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:
        conn.close()


# ==================================
# UPDATE TASK STATUS
# ==================================

def update_task_status(task_id, status):

    allowed_statuses = ["Pending", "Completed"]

    if status not in allowed_statuses:
        raise ValueError("Invalid task status")

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id = ?
        """, (status, task_id))

        conn.commit()

    finally:
        conn.close()


# ==================================
# EDIT TASK
# ==================================

def update_task(
    task_id,
    task_title,
    description,
    deadline
):

    if not task_title or not task_title.strip():
        raise ValueError("Task title cannot be empty")

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET
                task_title = ?,
                description = ?,
                deadline = ?
            WHERE id = ?
        """, (
            task_title.strip(),
            description,
            deadline,
            task_id
        ))

        conn.commit()

    finally:
        conn.close()


# ==================================
# TASK SUMMARY
# ==================================

def get_task_summary():

    tasks = get_all_tasks()
    today = date.today()

    summary = {
        "Total": len(tasks),
        "Pending": 0,
        "Completed": 0,
        "Upcoming": 0,
        "Overdue": 0
    }

    for task in tasks:

        if task["status"] == "Completed":
            summary["Completed"] += 1
            continue

        summary["Pending"] += 1

        deadline = task.get("deadline")

        if deadline:

            try:
                due_date = date.fromisoformat(deadline)

                if due_date < today:
                    summary["Overdue"] += 1
                else:
                    summary["Upcoming"] += 1

            except ValueError:
                pass

    return summary


# ==================================
# DELETE TASK
# ==================================

def delete_task(task_id):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        deleted = cursor.rowcount > 0

        conn.commit()

        return deleted

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# ==================================
# DELETE NOTICE
# ==================================

def delete_notice(notice_id):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Delete linked tasks
        cursor.execute(
            "DELETE FROM tasks WHERE notice_id = ?",
            (notice_id,)
        )

        # Delete linked important dates
        cursor.execute(
            "DELETE FROM important_dates WHERE notice_id = ?",
            (notice_id,)
        )

        # Delete notice
        cursor.execute(
            "DELETE FROM notices WHERE id = ?",
            (notice_id,)
        )

        deleted = cursor.rowcount > 0

        conn.commit()

        return deleted

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# ==================================
# SAVE IMPORTANT DATE
# ==================================

def save_important_date(notice_id, event_name, event_date):

    if not event_name or not event_name.strip():
        raise ValueError("Event name is required.")

    if not event_date:
        raise ValueError("Event date is required.")

    # Validate date format: YYYY-MM-DD
    try:
        datetime.strptime(event_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        raise ValueError("Date must be in YYYY-MM-DD format.")

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Check notice exists
        cursor.execute(
            "SELECT id FROM notices WHERE id = ?",
            (notice_id,)
        )

        if cursor.fetchone() is None:
            raise ValueError("Notice not found.")

        # Prevent duplicate dates
        cursor.execute("""
            SELECT date_id
            FROM important_dates
            WHERE notice_id = ?
            AND event_name = ?
            AND event_date = ?
        """, (
            notice_id,
            event_name.strip(),
            event_date
        ))

        existing = cursor.fetchone()

        if existing:
            return existing[0]

        cursor.execute("""
            INSERT INTO important_dates (
                notice_id,
                event_name,
                event_date
            )
            VALUES (?, ?, ?)
        """, (
            notice_id,
            event_name.strip(),
            event_date
        ))

        conn.commit()

        return cursor.lastrowid

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# ==================================
# GET IMPORTANT DATES BY NOTICE
# ==================================

def get_important_dates_by_notice(notice_id):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                date_id,
                notice_id,
                event_name,
                event_date
            FROM important_dates
            WHERE notice_id = ?
            ORDER BY event_date
        """, (notice_id,))

        return cursor.fetchall()

    finally:
        conn.close()


# ==================================
# GET ALL IMPORTANT DATES
# ==================================

def get_all_important_dates():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                date_id,
                notice_id,
                event_name,
                event_date
            FROM important_dates
            ORDER BY event_date
        """)

        return cursor.fetchall()

    finally:
        conn.close()