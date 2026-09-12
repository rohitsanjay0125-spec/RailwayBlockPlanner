def find_best_block(trains, section, duration):
    """
    Find the best time slot for a train/block
    while minimizing conflicts with existing trains.
    """

    section_trains = [
        train for train in trains
        if train["section"] == section
    ]

    best_start = None
    best_conflicts = float("inf")

    # Check every possible starting hour
    for start in range(0, 24 - duration + 1):

        end = start + duration
        conflicts = 0

        # Check overlap with existing trains
        for train in section_trains:

            train_start = int(train["start_time"])
            train_end = int(train["end_time"])

            if start < train_end and end > train_start:
                conflicts += 1

        # Select slot having minimum conflicts
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