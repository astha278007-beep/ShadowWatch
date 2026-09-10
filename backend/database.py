import sqlite3
import os
from datetime import datetime


# Database file will be stored inside the database folder
DATABASE_NAME = "database/shadowwatch.db"


def initialize_database():
    """Create the incidents table if it does not exist."""

    os.makedirs("database", exist_ok=True)

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            reason TEXT,
            evidence_file TEXT,
            evidence_hash TEXT,
            status TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_incident(reason, evidence_file, evidence_hash):
    """Save a tampering incident in the database."""

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO incidents
        (timestamp, reason, evidence_file, evidence_hash, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        timestamp,
        reason,
        evidence_file,
        evidence_hash,
        "ACTIVE"
    ))

    connection.commit()
    connection.close()


def get_incidents():
    """Get all saved incidents."""

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, timestamp, reason, evidence_file, status
        FROM incidents
        ORDER BY id DESC
    """)

    incidents = cursor.fetchall()

    connection.close()

    return incidents