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
            end_time INTEGER NOT NULL
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

    trains = [
        ("12001", "Shatabdi Express", "Bhopal-Itarsi", 6, 8),
        ("12141", "Patliputra Express", "Bhopal-Itarsi", 9, 11),
        ("12616", "Grand Trunk Express", "Bhopal-Itarsi", 13, 15),
        ("11072", "Kamayani Express", "Bhopal-Itarsi", 17, 19),
        ("12724", "Telangana Express", "Bhopal-Itarsi", 21, 23)
    ]

    cursor.execute("SELECT COUNT(*) FROM trains")

    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO trains
            (train_number, train_name, section, start_time, end_time)
            VALUES (?, ?, ?, ?, ?)
        """, trains)

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