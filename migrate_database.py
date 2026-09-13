import sqlite3
from database import DB_NAME


def convert_time(value):
    """
    Convert old integer hour values into HH:MM format.
    Example: 6 -> 06:00, 13 -> 13:00
    """
    value = int(value)
    return f"{value:02d}:00"


conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


# -------------------------------------------------
# 1. Add priority column if it does not exist
# -------------------------------------------------

columns = cursor.execute("""
    PRAGMA table_info(trains)
""").fetchall()

column_names = [column[1] for column in columns]

if "priority" not in column_names:
    cursor.execute("""
        ALTER TABLE trains
        ADD COLUMN priority INTEGER DEFAULT 1
    """)

    print("Priority column added successfully.")
else:
    print("Priority column already exists.")


# -------------------------------------------------
# 2. Read existing trains
# -------------------------------------------------

trains = cursor.execute("""
    SELECT id, start_time, end_time
    FROM trains
""").fetchall()


# -------------------------------------------------
# 3. Convert old time values
# -------------------------------------------------

for train_id, start_time, end_time in trains:

    if str(start_time).isdigit():
        new_start = convert_time(start_time)
    else:
        new_start = start_time

    if str(end_time).isdigit():
        new_end = convert_time(end_time)
    else:
        new_end = end_time

    cursor.execute("""
        UPDATE trains
        SET start_time = ?, end_time = ?
        WHERE id = ?
    """, (
        new_start,
        new_end,
        train_id
    ))


# -------------------------------------------------
# 4. Save changes
# -------------------------------------------------

conn.commit()
conn.close()

print("Database migration completed successfully.")