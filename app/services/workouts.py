"""Exercise library, split templates, and progression logic."""

import re

# key -> (Arabic name, English name, muscle group)
EXERCISES: dict[str, dict[str, str]] = {
    # chest
    "bench_press": {"ar": "ضغط صدر بالبار", "en": "Barbell Bench Press", "muscle": "chest"},
    "incline_db_press": {"ar": "ضغط صدر علوي بالدمبل", "en": "Incline Dumbbell Press", "muscle": "chest"},
    "cable_fly": {"ar": "تفتيح صدر بالكيبل", "en": "Cable Fly", "muscle": "chest"},
    "push_up": {"ar": "ضغط", "en": "Push-up", "muscle": "chest"},
    # back
    "deadlift": {"ar": "رفعة ميتة", "en": "Deadlift", "muscle": "back"},
    "barbell_row": {"ar": "تجديف بالبار", "en": "Barbell Row", "muscle": "back"},
    "lat_pulldown": {"ar": "سحب أمامي", "en": "Lat Pulldown", "muscle": "back"},
    "pull_up": {"ar": "عقلة", "en": "Pull-up", "muscle": "back"},
    "seated_cable_row": {"ar": "تجديف جالس بالكيبل", "en": "Seated Cable Row", "muscle": "back"},
    # shoulders
    "overhead_press": {"ar": "ضغط أكتاف بالبار", "en": "Overhead Press", "muscle": "shoulders"},
    "lateral_raise": {"ar": "رفرفة جانبية", "en": "Lateral Raise", "muscle": "shoulders"},
    "face_pull": {"ar": "سحب للوجه", "en": "Face Pull", "muscle": "shoulders"},
    # legs
    "squat": {"ar": "سكوات", "en": "Back Squat", "muscle": "legs"},
    "romanian_deadlift": {"ar": "رفعة رومانية", "en": "Romanian Deadlift", "muscle": "legs"},
    "leg_press": {"ar": "دفع أرجل", "en": "Leg Press", "muscle": "legs"},
    "leg_curl": {"ar": "ثني أرجل", "en": "Leg Curl", "muscle": "legs"},
    "leg_extension": {"ar": "مد أرجل", "en": "Leg Extension", "muscle": "legs"},
    "walking_lunge": {"ar": "طعنات مشي", "en": "Walking Lunge", "muscle": "legs"},
    "calf_raise": {"ar": "سمانة", "en": "Calf Raise", "muscle": "legs"},
    # arms
    "barbell_curl": {"ar": "بايسبس بالبار", "en": "Barbell Curl", "muscle": "arms"},
    "hammer_curl": {"ar": "بايسبس مطرقة", "en": "Hammer Curl", "muscle": "arms"},
    "triceps_pushdown": {"ar": "ترايسبس بالكيبل", "en": "Triceps Pushdown", "muscle": "arms"},
    "overhead_triceps": {"ar": "ترايسبس خلف الرأس", "en": "Overhead Triceps Extension", "muscle": "arms"},
    # core
    "plank": {"ar": "بلانك", "en": "Plank", "muscle": "core"},
    "hanging_leg_raise": {"ar": "رفع أرجل معلّق", "en": "Hanging Leg Raise", "muscle": "core"},
}

DAY_TYPES: dict[str, dict[str, str]] = {
    "full_a": {"ar": "جسم كامل (أ)", "en": "Full Body A"},
    "full_b": {"ar": "جسم كامل (ب)", "en": "Full Body B"},
    "upper_a": {"ar": "علوي (أ)", "en": "Upper A"},
    "upper_b": {"ar": "علوي (ب)", "en": "Upper B"},
    "lower_a": {"ar": "سفلي (أ)", "en": "Lower A"},
    "lower_b": {"ar": "سفلي (ب)", "en": "Lower B"},
    "push": {"ar": "دفع", "en": "Push"},
    "pull": {"ar": "سحب", "en": "Pull"},
    "legs": {"ar": "أرجل", "en": "Legs"},
}

# day type -> list of (exercise_key, sets, reps)
TEMPLATES: dict[str, list[tuple[str, int, str]]] = {
    "full_a": [
        ("squat", 3, "6-8"),
        ("bench_press", 3, "6-8"),
        ("barbell_row", 3, "8-10"),
        ("overhead_press", 2, "8-10"),
        ("leg_curl", 2, "10-12"),
        ("plank", 3, "30-45s"),
    ],
    "full_b": [
        ("deadlift", 3, "5"),
        ("incline_db_press", 3, "8-10"),
        ("lat_pulldown", 3, "8-12"),
        ("walking_lunge", 2, "10-12"),
        ("lateral_raise", 3, "12-15"),
        ("hammer_curl", 2, "10-12"),
    ],
    "upper_a": [
        ("bench_press", 4, "6-8"),
        ("barbell_row", 4, "6-8"),
        ("overhead_press", 3, "8-10"),
        ("lat_pulldown", 3, "8-12"),
        ("barbell_curl", 2, "10-12"),
        ("triceps_pushdown", 2, "10-12"),
    ],
    "upper_b": [
        ("incline_db_press", 4, "8-10"),
        ("pull_up", 4, "6-10"),
        ("seated_cable_row", 3, "10-12"),
        ("lateral_raise", 3, "12-15"),
        ("hammer_curl", 2, "10-12"),
        ("overhead_triceps", 2, "10-12"),
    ],
    "lower_a": [
        ("squat", 4, "6-8"),
        ("romanian_deadlift", 3, "8-10"),
        ("leg_extension", 3, "10-12"),
        ("calf_raise", 4, "12-15"),
        ("plank", 3, "30-45s"),
    ],
    "lower_b": [
        ("deadlift", 3, "5"),
        ("leg_press", 4, "10-12"),
        ("leg_curl", 3, "10-12"),
        ("walking_lunge", 2, "10-12"),
        ("hanging_leg_raise", 3, "10-15"),
    ],
    "push": [
        ("bench_press", 4, "6-8"),
        ("overhead_press", 3, "8-10"),
        ("incline_db_press", 3, "8-12"),
        ("lateral_raise", 3, "12-15"),
        ("triceps_pushdown", 3, "10-12"),
    ],
    "pull": [
        ("deadlift", 3, "5"),
        ("pull_up", 3, "6-10"),
        ("barbell_row", 3, "8-10"),
        ("face_pull", 3, "12-15"),
        ("barbell_curl", 3, "10-12"),
    ],
    "legs": [
        ("squat", 4, "6-8"),
        ("romanian_deadlift", 3, "8-10"),
        ("leg_press", 3, "10-12"),
        ("leg_curl", 3, "10-12"),
        ("calf_raise", 4, "12-15"),
    ],
}

SPLIT_NAMES: dict[str, dict[str, str]] = {
    "full_body": {"ar": "جسم كامل", "en": "Full Body"},
    "upper_lower": {"ar": "علوي / سفلي", "en": "Upper / Lower"},
    "hybrid": {"ar": "علوي / سفلي + دفع / سحب / أرجل", "en": "Upper / Lower + PPL"},
    "ppl": {"ar": "دفع / سحب / أرجل", "en": "Push / Pull / Legs"},
}

WEIGHT_STEP_KG = 2.5


def choose_split(days_per_week: int) -> tuple[str, list[str]]:
    """Pick a split and the ordered day types for the given training frequency."""
    if days_per_week <= 3:
        cycle = ["full_a", "full_b"]
        return "full_body", [cycle[i % 2] for i in range(days_per_week)]
    if days_per_week == 4:
        return "upper_lower", ["upper_a", "lower_a", "upper_b", "lower_b"]
    if days_per_week == 5:
        return "hybrid", ["upper_a", "lower_a", "push", "pull", "legs"]
    return "ppl", ["push", "pull", "legs", "push", "pull", "legs"]


def rep_range_top(reps: str) -> int | None:
    """'8-12' -> 12, '5' -> 5, '30-45s' -> None (timed sets don't progress by weight)."""
    match = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*", reps)
    if not match:
        return None
    return int(match.group(2) or match.group(1))


def suggest_next_weight(reps_target: str, last_sets: list[tuple[float, int]]) -> float | None:
    """Double progression: if every set last time reached the top of the rep range,
    add weight; otherwise keep the same weight and aim for more reps."""
    if not last_sets:
        return None
    top = rep_range_top(reps_target)
    working_weight = max(w for w, _ in last_sets)
    if top is None:
        return working_weight
    working_sets = [r for w, r in last_sets if w == working_weight]
    if all(r >= top for r in working_sets):
        return working_weight + WEIGHT_STEP_KG
    return working_weight
