def find_best_block(trains, section, duration):
    section_trains = [
        train for train in trains
        if train["section"] == section
    ]

    best_start = None
    best_conflicts = float("inf")

    for start in range(0, 24 - duration + 1):
        end = start + duration
        conflicts = 0

        for train in section_trains:
            if start < train["end_time"] and end > train["start_time"]:
                conflicts += 1

        if conflicts < best_conflicts:
            best_conflicts = conflicts
            best_start = start

    return {
        "start": best_start,
        "end": best_start + duration,
        "conflicts": best_conflicts
    }


def format_time(hour):
    return f"{hour:02d}:00"