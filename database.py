"""Database management and SQLite schema for Appointment Scheduler (Idea 2)."""
import os
import sqlite3
import csv
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_SERVICES_CSV = ROOT_DIR / "fixtures" / "idea2-appointments" / "services.csv"


def get_db_connection(db_path):
    """Create a connection with row factory configured."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path, services_csv=None):
    """Initialize database tables and seed services catalog from CSV if empty."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
        service_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        minutes INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id TEXT UNIQUE NOT NULL,
        client TEXT NOT NULL,
        service_id TEXT NOT NULL,
        stylist TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        state TEXT NOT NULL,
        FOREIGN KEY (service_id) REFERENCES services(service_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        actor TEXT NOT NULL,
        request_id TEXT,
        old_state TEXT,
        new_state TEXT,
        outcome TEXT NOT NULL
    );
    """)

    # Check if services table is seeded
    cursor.execute("SELECT COUNT(*) FROM services")
    count = cursor.fetchone()[0]
    if count == 0:
        csv_file = services_csv or DEFAULT_SERVICES_CSV
        if os.path.exists(csv_file):
            with open(csv_file, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cursor.execute(
                        "INSERT INTO services (service_id, name, minutes) VALUES (?, ?, ?)",
                        (row["service_id"].strip(), row["name"].strip(), int(row["minutes"].strip()))
                    )
    conn.commit()
    conn.close()


def log_audit(db_path, actor, request_id, old_state, new_state, outcome):
    """Record an audit trail entry for state changes or rejected actions."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO audit_log (timestamp, actor, request_id, old_state, new_state, outcome)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), actor, request_id, old_state, new_state, outcome)
    )
    conn.commit()
    conn.close()

