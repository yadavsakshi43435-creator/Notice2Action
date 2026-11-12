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

    columns = [
        row[1] for row in cursor.fetchall()
    ]

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

    conn.commit()

    conn.close()


# ==================================
# SAVE NOTICE
# ==================================

def save_notice(title, filename, extracted_text, analysis):

    notice_hash = hashlib.sha256(
        extracted_text.strip().encode("utf-8")
    ).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()

    # Duplicate check

    cursor.execute("""
        SELECT id

        FROM notices

        WHERE extracted_text_hash = ?
    """, (notice_hash,))

    existing_notice = cursor.fetchone()

    if existing_notice:

        conn.close()

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

    conn.close()

    return notice_id


# ==================================
# GET ALL NOTICES
# ==================================

def get_all_notices():

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *

        FROM notices

        ORDER BY id DESC
    """)

    notices = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return notices


# ==================================
# UPDATE NOTICE STATUS
# ==================================

def update_notice_status(notice_id, status):

    allowed_statuses = [
        "Pending",
        "Completed"
    ]

    if status not in allowed_statuses:

        raise ValueError("Invalid notice status")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE notices

        SET status = ?

        WHERE id = ?
    """, (status, notice_id))

    conn.commit()

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

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id

        FROM notices

        WHERE id = ?
    """, (notice_id,))

    if cursor.fetchone() is None:

        conn.close()

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

    conn.close()

    return task_id


# ==================================
# SAVE MULTIPLE TASKS
# ==================================

def save_multiple_tasks(notice_id, tasks):

    saved_ids = []

    for task in tasks:

        task_id = save_task(

            notice_id=notice_id,

            task_title=task.get(
                "task_title",
                "Untitled Task"
            ),

            description=task.get(
                "description",
                ""
            ),

            deadline=task.get(
                "deadline"
            ),

            source_text=task.get(
                "source_text",
                ""
            )

        )

        saved_ids.append(task_id)

    return saved_ids


# ==================================
# GET ALL TASKS
# ==================================

def get_all_tasks():

    conn = get_connection()

    conn.row_factory = sqlite3.Row

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

    tasks = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return tasks


# ==================================
# GET TASKS BY NOTICE
# ==================================

def get_tasks_by_notice(notice_id):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *

        FROM tasks

        WHERE notice_id = ?

        ORDER BY id DESC
    """, (notice_id,))

    tasks = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return tasks


# ==================================
# UPDATE TASK STATUS
# ==================================

def update_task_status(task_id, status):

    allowed_statuses = [
        "Pending",
        "Completed"
    ]

    if status not in allowed_statuses:

        raise ValueError("Invalid task status")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks

        SET status = ?

        WHERE id = ?
    """, (status, task_id))

    conn.commit()

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

                due_date = date.fromisoformat(
                    deadline
                )

                if due_date < today:

                    summary["Overdue"] += 1

                else:

                    summary["Upcoming"] += 1

            except ValueError:

                pass

    return summary

def delete_task(task_id):
    """
    Delete a single task using its task ID.
    """
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

def delete_notice(notice_id):
    """
    Delete a notice and all tasks linked to that notice.
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()

        # First delete tasks linked to this notice
        cursor.execute(
            "DELETE FROM tasks WHERE notice_id = ?",
            (notice_id,)
        )

        # Then delete the notice
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