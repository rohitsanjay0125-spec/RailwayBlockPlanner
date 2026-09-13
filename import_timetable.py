from database import get_connection


trains = [
    ("12616", "Grand Trunk Express", "Bhopal-Itarsi", "03:20", "05:15", "public timetable"),
    ("11072", "Kamayani Express", "Bhopal-Itarsi", "07:30", "09:40", "public timetable"),
]


conn = get_connection()

for train in trains:
    existing = conn.execute(
        "SELECT id FROM trains WHERE train_number = ?",
        (train[0],)
    ).fetchone()

    if existing:
        print(f"Skipping {train[0]} - already exists")
        continue

    conn.execute("""
        INSERT INTO trains
        (train_number, train_name, section, start_time, end_time, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """, train)

conn.commit()
conn.close()

print("Public timetable import completed successfully.")