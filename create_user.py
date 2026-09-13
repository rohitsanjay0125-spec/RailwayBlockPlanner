import sqlite3
from database import DB_NAME

conn = sqlite3.connect(DB_NAME)

conn.execute("""
    INSERT OR IGNORE INTO users
    (user_id, password_hash, department)
    VALUES (?, ?, ?)
""", (
    "admin001",
    "admin123",
    "Admin"
))

conn.commit()
conn.close()

print("Demo user created successfully.")