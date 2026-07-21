"""SQLite storage layer for Case Intake Suite."""

import sqlite3
import uuid
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("cases/cases.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id TEXT PRIMARY KEY,
            subject_url TEXT NOT NULL,
            handle TEXT,
            category TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'open',
            reporter_notes TEXT,
            reviewer_notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            file_path TEXT,
            url TEXT,
            description TEXT,
            added_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(id)
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database initialised at {DB_PATH}")


def create_case(subject_url, handle, category, description, reporter_notes):
    """Insert a new case and return its ID."""
    case_id = str(uuid.uuid4())[:8]
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    conn.execute("""
        INSERT INTO cases (id, subject_url, handle, category, description,
                           status, reporter_notes, reviewer_notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'open', ?, '', ?, ?)
    """, (case_id, subject_url, handle, category, description, reporter_notes, now, now))
    conn.commit()
    conn.close()
    return case_id


def get_all_cases():
    """Return all cases as list of dicts."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM cases ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_case(case_id):
    """Return a single case dict or None."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_case_status(case_id, status, reviewer_notes=""):
    """Update case status and reviewer notes."""
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    conn.execute("""
        UPDATE cases SET status = ?, reviewer_notes = ?, updated_at = ?
        WHERE id = ?
    """, (status, reviewer_notes, now, case_id))
    conn.commit()
    conn.close()


def add_evidence(case_id, description, file_path=None, url=None):
    """Add an evidence item to a case."""
    ev_id = str(uuid.uuid4())[:8]
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    conn.execute("""
        INSERT INTO evidence (id, case_id, file_path, url, description, added_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ev_id, case_id, file_path, url, description, now))
    conn.commit()
    conn.close()
    return ev_id


def get_evidence(case_id):
    """Return all evidence items for a case."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM evidence WHERE case_id = ? ORDER BY added_at",
        (case_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
