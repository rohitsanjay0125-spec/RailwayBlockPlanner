import sqlite3
from database import DB_NAME


def import_verified_train(
    train_number,
    train_name,
    section,
    start_time,
    end_time,
    source="Indian Railways"
):
    if end_time <= start_time:
        raise ValueError("End time must be greater than start time.")

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO trains
        (train_number, train_name, section,
         start_time, end_time, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        train_number,
        train_name,
        section,
        start_time,
        end_time,
        source
    ))

    conn.commit()
    conn.close()

    print(
        f"Imported: {train_number} | "
        f"{train_name} | {start_time}:00-{end_time}:00"
    )


def get_trains_from_database():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    trains = conn.execute("""
        SELECT *
        FROM trains
        ORDER BY start_time
    """).fetchall()

    conn.close()
    return trains


if __name__ == "__main__":
    trains = get_trains_from_database()

    print("\nRailway Train Data")
    print("-" * 60)

    for train in trains:
        print(
            train["train_number"],
            "|",
            train["train_name"],
            "|",
            train["section"],
            "|",
            train["start_time"],
            "-",
            train["end_time"],
            "| Source:",
            train["source"]
        )