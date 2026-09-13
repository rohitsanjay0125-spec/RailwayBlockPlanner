import sqlite3
from database import DB_NAME


trains = [
    ("11078", "Jhelum Express", "Bhopal-Itarsi",
     "00:05", "01:50"),

    ("12191", "Shridham SF Express", "Bhopal-Itarsi",
     "02:00", "03:50"),

    ("12780", "Goa Express", "Bhopal-Itarsi",
     "02:45", "04:25"),

    ("12616", "Grand Trunk Express", "Bhopal-Itarsi",
     "03:20", "05:15"),

    ("22692", "Bangalore Rajdhani", "Bhopal-Itarsi",
     "03:55", "05:23"),

    ("12626", "Kerala Express", "Bhopal-Itarsi",
     "05:25", "07:05"),

    ("12628", "Karnataka Express", "Bhopal-Itarsi",
     "06:30", "08:20"),

    ("12622", "Tamilnadu SF Express", "Bhopal-Itarsi",
     "06:50", "08:35"),

    ("12533", "Pushpak Express", "Bhopal-Itarsi",
     "07:10", "08:55"),

    ("11072", "Kamayani Express", "Bhopal-Itarsi",
     "07:30", "09:40"),

    ("11058", "ASR CSMT Express", "Bhopal-Itarsi",
     "09:20", "11:15"),

    ("12722", "Dakshin Express", "Bhopal-Itarsi",
     "09:40", "11:50"),

    ("22537", "Kushinagar SF Express", "Bhopal-Itarsi",
     "10:00", "11:50"),

    ("20104", "GKP LTT SF Express", "Bhopal-Itarsi",
     "14:45", "16:20"),

    ("12854", "Amarkantak Express", "Bhopal-Itarsi",
     "16:00", "17:40"),

    ("12618", "Mangladweep Express", "Bhopal-Itarsi",
     "16:25", "18:20"),

    ("12138", "Punjab Mail", "Bhopal-Itarsi",
     "16:40", "18:35"),

    ("18238", "Chhattisgarh Express", "Bhopal-Itarsi",
     "18:00", "20:20"),

    ("19343", "Panchvalley Express", "Bhopal-Itarsi",
     "18:10", "21:05"),

    ("20424", "Patalkot Express", "Bhopal-Itarsi",
     "21:55", "23:45"),

    ("18233", "INDB BSP Express", "Bhopal-Itarsi",
     "22:15", "00:10"),

    ("12716", "Sachkhand Express", "Bhopal-Itarsi",
     "22:40", "00:10"),

    ("22191", "INDB JBP SF Express", "Bhopal-Itarsi",
     "23:35", "01:35")
]


conn = sqlite3.connect(DB_NAME)

# Remove current demo timetable
conn.execute("""
    DELETE FROM trains
    WHERE source = 'demo'
""")

# Insert verified timetable records
conn.executemany("""
    INSERT INTO trains
    (train_number, train_name, section,
     start_time, end_time, source)
    VALUES (?, ?, ?, ?, ?, ?)
""", [
    (*train, "verified_schedule")
    for train in trains
])

conn.commit()
conn.close()

print(f"Imported {len(trains)} Bhopal-Itarsi trains successfully.")