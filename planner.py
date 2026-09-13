def time_to_minutes(time_string):
    """Convert HH:MM into minutes from midnight."""
    hours, minutes = map(int, time_string.split(":"))
    return hours * 60 + minutes


def minutes_to_time(total_minutes):
    """Convert minutes into HH:MM."""
    total_minutes = total_minutes % (24 * 60)

    hours = total_minutes // 60
    minutes = total_minutes % 60

    return f"{hours:02d}:{minutes:02d}"


def get_train_interval(start_time, end_time):
    """
    Convert train timing into a continuous interval.

    Example:
    22:15 -> 00:10 becomes 22:15 -> 24:10
    """

    start = time_to_minutes(start_time)
    end = time_to_minutes(end_time)

    # Train crosses midnight
    if end <= start:
        end += 24 * 60

    return start, end


def find_best_block(trains, section, duration):
    """
    Find the best maintenance block.

    duration is given in hours.

    The planner checks every 15 minutes and
    selects the slot with minimum train conflicts.
    """

    section_trains = [
        train for train in trains
        if train["section"] == section
    ]

    duration_minutes = int(duration) * 60

    best_start = None
    best_conflicts = float("inf")

    # Check every 15-minute slot in 24 hours
    for start in range(
        0,
        24 * 60 - duration_minutes + 1,
        15
    ):

        end = start + duration_minutes

        conflicts = 0

        for train in section_trains:

            train_start, train_end = get_train_interval(
                train["start_time"],
                train["end_time"]
            )

            # Check normal same-day overlap
            if start < train_end and end > train_start:
                conflicts += 1

            # Check midnight-crossing representation
            elif train_end > 24 * 60:

                second_start = train_start - 24 * 60
                second_end = train_end - 24 * 60

                if start < second_end and end > second_start:
                    conflicts += 1

        # Select minimum-conflict block
        if conflicts < best_conflicts:
            best_conflicts = conflicts
            best_start = start

    return {
        "start": best_start,
        "end": best_start + duration_minutes,
        "conflicts": best_conflicts
    }


def format_time(value):
    """Convert planner minutes into HH:MM."""
    return minutes_to_time(value)