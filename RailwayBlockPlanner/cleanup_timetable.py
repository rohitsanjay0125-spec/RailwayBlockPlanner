import sqlite3
from database import DB_NAME

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Keep only verified timetable records
cursor.execute("""
    DELETE FROM trains
    WHERE source != 'verified_schedule'
       OR source IS NULL
""")

deleted = cursor.rowcount

conn.commit()

# Show remaining trains
trains = cursor.execute("""
    SELECT train_number, train_name, start_time, end_time, source
    FROM trains
    ORDER BY start_time
""").fetchall()

conn.close()

print(f"Removed {deleted} old manual/demo train records.")
print(f"Verified trains remaining: {len(trains)}")

for train in trains:
    print(train)