def time_to_minutes(time_string):
    hours, minutes = map(int, time_string.split(":"))
    return hours * 60 + minutes


def minutes_to_time(total_minutes):
    total_minutes = total_minutes % (24 * 60)

    hours = total_minutes // 60
    minutes = total_minutes % 60

    return f"{hours:02d}:{minutes:02d}"


def get_train_interval(start_time, end_time):
    start = time_to_minutes(start_time)
    end = time_to_minutes(end_time)

    if end <= start:
        end += 24 * 60

    return start, end


def time_to_minutes(value):
    """Convert HH:MM time into minutes."""
    value = str(value)

    if ":" in value:
        hour, minute = map(int, value.split(":"))
        return hour * 60 + minute

    return int(value) * 60


def minutes_to_time(minutes):
    """Convert minutes into HH:MM."""
    minutes = minutes % (24 * 60)
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"


def ai_recommendation(trains, assets, section, duration):

    available_assets = [
        asset for asset in assets
        if str(asset["status"]).lower() == "available"
    ]

    duration_minutes = duration * 60
    recommendations = []

    # Check every possible 1-hour starting point
    for start in range(0, 24 * 60 - duration_minutes + 1, 60):

        end = start + duration_minutes

        conflicts = 0
        conflict_weight = 0

        for train in trains:

            train_start = time_to_minutes(train["start_time"])
            train_end = time_to_minutes(train["end_time"])

            # Handle trains crossing midnight
            if train_end <= train_start:
                train_end += 24 * 60

            # Check block/train overlap
            if start < train_end and end > train_start:

                conflicts += 1

                # Train priority
                try:
                    priority = int(train["priority"])
                except:
                    priority = 1

                conflict_weight += priority

        # Start with maximum score
        score = 100

        # Heavy penalty for train conflicts
        score -= conflict_weight * 30

        # Slight penalty for longer maintenance
        score -= duration * 3

        # Asset availability bonus
        asset_bonus = min(len(available_assets) * 2, 10)
        score += asset_bonus

        # Keep score between 0 and 100
        score = max(0, min(100, score))

        recommendations.append({
            "start": start,
            "end": end,
            "conflicts": conflicts,
            "score": score
        })

    # Prefer fewer conflicts, then higher AI score
    best = min(
        recommendations,
        key=lambda x: (x["conflicts"], -x["score"])
    )

    return {
        "start": minutes_to_time(best["start"]),
        "end": minutes_to_time(best["end"]),
        "conflicts": best["conflicts"],
        "score": best["score"]
    }