
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

DB_PATH = Path(__file__).resolve().parent / "tasks.db"


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def initialize_database():
    """Create the tasks table if it doesn't exist."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)


def add_task(title: str) -> str:
    """Add a new task to the database."""

    title = title.strip()

    if not title:
        return "Error: Task title cannot be empty."

    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )

        task_id = cursor.lastrowid

    return (
        f"Task added successfully. "
        f"ID: {task_id}, Title: {title}"
    )


def list_tasks() -> str:
    """Retrieve all tasks from the database."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, title, completed
            FROM tasks
            ORDER BY id
            """
        ).fetchall()

    if not rows:
        return "No tasks found."

    result = []

    for row in rows:
        status = "Completed" if row["completed"] else "Pending"

        result.append(
            f"ID: {row['id']} | "
            f"{row['title']} | {status}"
        )

    return "\n".join(result)


def complete_task(task_id: int) -> str:
    """Mark a task as completed."""

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE tasks
            SET completed = 1
            WHERE id = ? AND completed = 0
            """,
            (task_id,)
        )

        if cursor.rowcount == 1:
            return f"Task {task_id} marked as completed."

        row = connection.execute(
            """
            SELECT completed
            FROM tasks
            WHERE id = ?
            """,
            (task_id,)
        ).fetchone()

    if row is None:
        return f"Error: Task {task_id} does not exist."

    return f"Task {task_id} is already completed."


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at: {DB_PATH}")
