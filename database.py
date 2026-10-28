import sqlite3
from datetime import date

DB_NAME = "job_tracker.db"

STATUSES = ["Applied", "Assessment", "Interview", "Offer", "Rejected", "No Response"]


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                job_title TEXT NOT NULL,
                applied_date TEXT NOT NULL,
                location TEXT,
                job_type TEXT,
                source TEXT,
                status TEXT NOT NULL,
                salary_lpa REAL,
                job_url TEXT,
                notes TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS application_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                event_date TEXT NOT NULL,
                note TEXT,
                FOREIGN KEY (application_id) REFERENCES applications(id)
            )
        """)


def add_application(company, job_title, applied_date, location=None,
                    job_type=None, source=None, salary_lpa=None,
                    job_url=None, notes=None):
    """Insert an application and log its first 'Applied' event."""
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO applications
               (company, job_title, applied_date, location, job_type,
                source, status, salary_lpa, job_url, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (company, job_title, applied_date, location, job_type,
             source, "Applied", salary_lpa, job_url, notes),
        )
        app_id = cur.lastrowid
        conn.execute(
            """INSERT INTO application_events
               (application_id, status, event_date)
               VALUES (?, 'Applied', ?)""",
            (app_id, applied_date),
        )
    return app_id


def update_status(app_id, new_status, event_date=None, note=None):
    """Change the current status AND record the change in the events table."""
    if new_status not in STATUSES:
        raise ValueError(f"Status must be one of {STATUSES}")
    event_date = event_date or date.today().isoformat()
    with get_connection() as conn:
        conn.execute("UPDATE applications SET status = ? WHERE id = ?",
                     (new_status, app_id))
        conn.execute(
            """INSERT INTO application_events
               (application_id, status, event_date, note)
               VALUES (?, ?, ?, ?)""",
            (app_id, new_status, event_date, note),
        )


if __name__ == "__main__":
    create_tables()
    print("Database and tables are ready.")