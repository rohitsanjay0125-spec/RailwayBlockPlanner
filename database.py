import sqlite3

DB_NAME = "railway.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_number TEXT NOT NULL,
    train_name TEXT NOT NULL,
    section TEXT NOT NULL,
    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,
    priority INTEGER DEFAULT 1
)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_name TEXT NOT NULL,
            section TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Users table for login
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    # Add source column...
    # Add source column to an older database if necessary
    columns = [
        row["name"]
        for row in cursor.execute(
            "PRAGMA table_info(trains)"
        ).fetchall()
    ]

    if "source" not in columns:
        cursor.execute("""
            ALTER TABLE trains
            ADD COLUMN source TEXT DEFAULT 'demo'
        """)

    # Demo data — temporary
    trains = [
        ("12001", "Shatabdi Express", "Bhopal-Itarsi",
         "06:00", "08:00"),
        ("12141", "Patliputra Express", "Bhopal-Itarsi",
         "09:00", "11:00"),
        ("12616", "Grand Trunk Express", "Bhopal-Itarsi",
         "13:00", "15:00"),
        ("11072", "Kamayani Express", "Bhopal-Itarsi",
         "17:00", "19:00"),
        ("12724", "Telangana Express", "Bhopal-Itarsi",
         "21:00", "23:00")
    ]

    cursor.execute("SELECT COUNT(*) FROM trains")

    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO trains
            (train_number, train_name, section,
             start_time, end_time, source)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (*train, "demo")
            for train in trains
        ])

    assets = [
        ("Track 1", "Bhopal-Itarsi", "Available"),
        ("Track 2", "Bhopal-Itarsi", "Available"),
        ("Signal System", "Bhopal-Itarsi", "Available"),
        ("Railway Bridge", "Bhopal-Itarsi", "Available")
    ]

    cursor.execute("SELECT COUNT(*) FROM assets")

    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO assets
            (asset_name, section, status)
            VALUES (?, ?, ?)
        """, assets)

    conn.commit()
    conn.close()