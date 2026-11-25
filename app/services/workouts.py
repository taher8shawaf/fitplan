"""Exercise library, split templates, and progression logic."""

import re


# key -> Arabic name, English name, muscle group, and (for exercises without a
# written guide) the muscles to highlight on the body map.
def _ex(ar: str, en: str, muscle: str, primary: tuple[str, ...] = (), secondary: tuple[str, ...] = ()) -> dict:
    entry: dict = {"ar": ar, "en": en, "muscle": muscle}
    if primary:
        entry["primary"] = list(primary)
        entry["secondary"] = list(secondary)
    return entry


EXERCISES: dict[str, dict] = {
    # chest
    "bench_press": _ex("ضغط صدر بالبار", "Barbell Bench Press", "chest"),
    "incline_bench_press": _ex(
        "ضغط صدر علوي بالبار", "Incline Barbell Bench Press", "chest", ("chest", "shoulders"), ("triceps",)
    ),
    "decline_bench_press": _ex("ضغط صدر سفلي بالبار", "Decline Bench Press", "chest", ("chest",), ("triceps",)),
    "db_bench_press": _ex("ضغط صدر بالدمبل", "Dumbbell Bench Press", "chest", ("chest",), ("triceps", "shoulders")),
    "incline_db_press": _ex("ضغط صدر علوي بالدمبل", "Incline Dumbbell Press", "chest"),
    "chest_press_machine": _ex("ضغط صدر بالجهاز", "Machine Chest Press", "chest", ("chest",), ("triceps", "shoulders")),
    "incline_machine_press": _ex(
        "ضغط صدر علوي بالجهاز", "Incline Machine Press", "chest", ("chest", "shoulders"), ("triceps",)
    ),
    "smith_incline_press": _ex(
        "ضغط صدر علوي بالسميث", "Smith Machine Incline Press", "chest", ("chest", "shoulders"), ("triceps",)
    ),
    "db_fly": _ex("تفتيح صدر بالدمبل", "Dumbbell Fly", "chest", ("chest",), ("shoulders",)),
    "incline_db_fly": _ex("تفتيح صدر علوي بالدمبل", "Incline Dumbbell Fly", "chest", ("chest",), ("shoulders",)),
    "pec_deck": _ex("فراشة صدر بالجهاز", "Pec Deck (Machine Fly)", "chest", ("chest",)),
    "cable_fly": _ex("تفتيح صدر بالكيبل", "Cable Fly", "chest"),
    "low_cable_fly": _ex("تفتيح كيبل من تحت لفوق", "Low-to-High Cable Fly", "chest", ("chest",), ("shoulders",)),
    "chest_dip": _ex("متوازي للصدر", "Chest Dip", "chest", ("chest", "triceps"), ("shoulders",)),
    "push_up": _ex("ضغط", "Push-up", "chest"),
    "db_pullover": _ex("بول أوفر بالدمبل", "Dumbbell Pullover", "chest", ("chest", "lats"), ("triceps",)),
    # back
    "deadlift": _ex("رفعة ميتة", "Deadlift", "back"),
    "rack_pull": _ex(
        "رفعة ميتة جزئية (راك بول)", "Rack Pull", "back", ("lower_back", "traps", "glutes"), ("hamstrings", "forearms")
    ),
    "barbell_row": _ex("تجديف بالبار", "Barbell Row", "back"),
    "t_bar_row": _ex("تجديف تي بار", "T-Bar Row", "back", ("lats", "traps"), ("rear_delts", "biceps")),
    "one_arm_db_row": _ex(
        "تجديف دمبل بيد واحدة", "One-Arm Dumbbell Row", "back", ("lats", "traps"), ("rear_delts", "biceps")
    ),
    "chest_supported_row": _ex(
        "تجديف مسنود على الصدر", "Chest-Supported Row", "back", ("traps", "lats"), ("rear_delts", "biceps")
    ),
    "machine_row": _ex("تجديف بالجهاز", "Machine Row", "back", ("traps", "lats"), ("biceps",)),
    "seated_cable_row": _ex("تجديف جالس بالكيبل", "Seated Cable Row", "back"),
    "lat_pulldown": _ex("سحب أمامي", "Lat Pulldown", "back"),
    "close_grip_pulldown": _ex("سحب أمامي قبضة ضيقة", "Close-Grip Lat Pulldown", "back", ("lats",), ("biceps",)),
    "straight_arm_pulldown": _ex("سحب بذراع مستقيمة", "Straight-Arm Pulldown", "back", ("lats",), ("triceps",)),
    "pull_up": _ex("عقلة", "Pull-up", "back"),
    "chin_up": _ex("عقلة قبضة معكوسة", "Chin-up", "back", ("lats", "biceps"), ("traps",)),
    "assisted_pull_up": _ex("عقلة بالمساعدة", "Assisted Pull-up", "back", ("lats",), ("biceps",)),
    "back_extension": _ex(
        "ظهر سفلي (باك إكستنشن)", "Back Extension", "back", ("lower_back",), ("glutes", "hamstrings")
    ),
    "barbell_shrug": _ex("ترابيس بالبار", "Barbell Shrug", "back", ("traps",), ("forearms",)),
    "db_shrug": _ex("ترابيس بالدمبل", "Dumbbell Shrug", "back", ("traps",), ("forearms",)),
    # shoulders
    "overhead_press": _ex("ضغط أكتاف بالبار", "Overhead Press", "shoulders"),
    "db_shoulder_press": _ex("ضغط أكتاف بالدمبل", "Dumbbell Shoulder Press", "shoulders", ("shoulders",), ("triceps",)),
    "arnold_press": _ex("ضغط أرنولد", "Arnold Press", "shoulders", ("shoulders",), ("triceps",)),
    "machine_shoulder_press": _ex(
        "ضغط أكتاف بالجهاز", "Machine Shoulder Press", "shoulders", ("shoulders",), ("triceps",)
    ),
    "lateral_raise": _ex("رفرفة جانبية", "Lateral Raise", "shoulders"),
    "cable_lateral_raise": _ex("رفرفة جانبية بالكيبل", "Cable Lateral Raise", "shoulders", ("shoulders",)),
    "front_raise": _ex("رفرفة أمامية", "Front Raise", "shoulders", ("shoulders",)),
    "rear_delt_fly": _ex("رفرفة خلفية بالدمبل", "Rear Delt Fly", "shoulders", ("rear_delts",), ("traps",)),
    "reverse_pec_deck": _ex("فراشة عكسية", "Reverse Pec Deck", "shoulders", ("rear_delts",), ("traps",)),
    "face_pull": _ex("سحب للوجه", "Face Pull", "shoulders"),
    "upright_row": _ex("سحب عمودي", "Upright Row", "shoulders", ("shoulders", "traps"), ("biceps",)),
    # biceps
    "barbell_curl": _ex("بايسبس بالبار", "Barbell Curl", "biceps"),
    "ez_bar_curl": _ex("بايسبس بالبار المتعرج", "EZ-Bar Curl", "biceps", ("biceps",), ("forearms",)),
    "db_curl": _ex("بايسبس بالدمبل", "Dumbbell Curl", "biceps", ("biceps",), ("forearms",)),
    "hammer_curl": _ex("بايسبس مطرقة", "Hammer Curl", "biceps"),
    "incline_db_curl": _ex("بايسبس على بنش مائل", "Incline Dumbbell Curl", "biceps", ("biceps",)),
    "preacher_curl": _ex("بايسبس سكوت (على الكرسي)", "Preacher Curl", "biceps", ("biceps",)),
    "cable_curl": _ex("بايسبس بالكيبل", "Cable Curl", "biceps", ("biceps",), ("forearms",)),
    "concentration_curl": _ex("بايسبس تركيز", "Concentration Curl", "biceps", ("biceps",)),
    # triceps
    "triceps_pushdown": _ex("ترايسبس بالكيبل", "Triceps Pushdown", "triceps"),
    "rope_pushdown": _ex("ترايسبس بالحبل", "Rope Pushdown", "triceps", ("triceps",)),
    "overhead_triceps": _ex("ترايسبس خلف الرأس", "Overhead Triceps Extension", "triceps"),
    "cable_overhead_ext": _ex("ترايسبس خلف الرأس بالكيبل", "Overhead Cable Extension", "triceps", ("triceps",)),
    "skull_crusher": _ex("ترايسبس فرنسي (سكل كراشر)", "Skull Crusher", "triceps", ("triceps",)),
    "close_grip_bench": _ex(
        "ضغط صدر بقبضة ضيقة", "Close-Grip Bench Press", "triceps", ("triceps", "chest"), ("shoulders",)
    ),
    "triceps_dip": _ex("متوازي للترايسبس", "Triceps Dip", "triceps", ("triceps",), ("chest", "shoulders")),
    "db_kickback": _ex("ترايسبس كيك باك", "Dumbbell Kickback", "triceps", ("triceps",)),
    # forearms
    "wrist_curl": _ex("ساعد (ثني الرسغ)", "Wrist Curl", "forearms", ("forearms",)),
    "reverse_curl": _ex("بايسبس قبضة معكوسة", "Reverse Curl", "forearms", ("forearms", "biceps")),
    "farmers_walk": _ex("مشية المزارع", "Farmer's Walk", "forearms", ("forearms", "traps"), ("abs", "glutes")),
    # legs
    "squat": _ex("سكوات", "Back Squat", "legs"),
    "front_squat": _ex("سكوات أمامي", "Front Squat", "legs", ("quads",), ("glutes", "abs")),
    "smith_squat": _ex("سكوات بالسميث", "Smith Machine Squat", "legs", ("quads", "glutes"), ("hamstrings",)),
    "hack_squat": _ex("هاك سكوات", "Hack Squat", "legs", ("quads",), ("glutes",)),
    "goblet_squat": _ex("سكوات كأس (جوبلت)", "Goblet Squat", "legs", ("quads", "glutes"), ("abs",)),
    "bulgarian_split_squat": _ex("سكوات بلغاري", "Bulgarian Split Squat", "legs", ("quads", "glutes"), ("hamstrings",)),
    "leg_press": _ex("دفع أرجل", "Leg Press", "legs"),
    "walking_lunge": _ex("طعنات مشي", "Walking Lunge", "legs"),
    "step_up": _ex("صعود على بوكس", "Step-up", "legs", ("quads", "glutes")),
    "leg_extension": _ex("مد أرجل", "Leg Extension", "legs"),
    "romanian_deadlift": _ex("رفعة رومانية", "Romanian Deadlift", "legs"),
    "sumo_deadlift": _ex(
        "رفعة ميتة سومو", "Sumo Deadlift", "legs", ("glutes", "quads", "hamstrings"), ("lower_back", "traps")
    ),
    "good_morning": _ex("جود مورنينج", "Good Morning", "legs", ("hamstrings", "lower_back"), ("glutes",)),
    "leg_curl": _ex("ثني أرجل", "Leg Curl", "legs"),
    "seated_leg_curl": _ex("ثني أرجل جالس", "Seated Leg Curl", "legs", ("hamstrings",)),
    "hip_thrust": _ex("دفع الحوض بالبار (هيب ثرست)", "Barbell Hip Thrust", "legs", ("glutes",), ("hamstrings",)),
    "glute_bridge": _ex("جسر الأرداف", "Glute Bridge", "legs", ("glutes",), ("hamstrings",)),
    "cable_kickback": _ex("ركلة خلفية بالكيبل", "Cable Glute Kickback", "legs", ("glutes",)),
    "hip_abduction": _ex("فتح الأرجل بالجهاز", "Hip Abduction Machine", "legs", ("glutes",)),
    "hip_adduction": _ex("ضم الأرجل بالجهاز", "Hip Adduction Machine", "legs", ("quads",)),
    "calf_raise": _ex("سمانة", "Calf Raise", "legs"),
    "seated_calf_raise": _ex("سمانة جالس", "Seated Calf Raise", "legs", ("calves",)),
    # core
    "plank": _ex("بلانك", "Plank", "core"),
    "side_plank": _ex("بلانك جانبي", "Side Plank", "core", ("abs",)),
    "hanging_leg_raise": _ex("رفع أرجل معلّق", "Hanging Leg Raise", "core"),
    "lying_leg_raise": _ex("رفع أرجل على الأرض", "Lying Leg Raise", "core", ("abs",)),
    "crunch": _ex("كرنش", "Crunch", "core", ("abs",)),
    "cable_crunch": _ex("كرنش بالكيبل", "Cable Crunch", "core", ("abs",)),
    "ab_wheel": _ex("عجلة البطن", "Ab Wheel Rollout", "core", ("abs",), ("lats", "shoulders")),
    "russian_twist": _ex("لف روسي", "Russian Twist", "core", ("abs",)),
    "mountain_climber": _ex("متسلق الجبل", "Mountain Climbers", "core", ("abs",), ("shoulders", "quads")),
    # cardio
    "treadmill_run": _ex("جري على السير", "Treadmill Run", "cardio", ("quads", "calves"), ("hamstrings", "glutes")),
    "incline_walk": _ex(
        "مشي مائل على السير", "Incline Treadmill Walk", "cardio", ("glutes", "calves"), ("hamstrings",)
    ),
    "stationary_bike": _ex("دراجة ثابتة", "Stationary Bike", "cardio", ("quads",), ("calves", "hamstrings")),
    "elliptical": _ex("جهاز الإليبتيكال", "Elliptical", "cardio", ("quads", "glutes"), ("calves",)),
    "rowing_machine": _ex("جهاز التجديف", "Rowing Machine", "cardio", ("lats", "quads"), ("biceps", "hamstrings")),
    "stair_climber": _ex("جهاز الدرج", "Stair Climber", "cardio", ("glutes", "quads"), ("calves",)),
    "jump_rope": _ex("نط الحبل", "Jump Rope", "cardio", ("calves",), ("shoulders",)),
    "burpee": _ex("بيربي", "Burpees", "cardio", ("quads", "chest"), ("shoulders", "abs")),
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
    "custom": {"ar": "تمرين", "en": "Workout"},
}

# "arms" is kept so custom exercises saved before biceps/triceps were split stay valid.
MUSCLES = ["chest", "back", "shoulders", "biceps", "triceps", "forearms", "legs", "core", "cardio", "arms", "other"]
CUSTOM_PREFIX = "custom_"

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
    "custom": {"ar": "جدولي الخاص", "en": "My custom plan"},
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
