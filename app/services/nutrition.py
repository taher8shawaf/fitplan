"""Daily calorie and macro targets.

BMR uses the Mifflin-St Jeor equation, multiplied by an activity factor (TDEE),
then adjusted for the user's goal. Targets are estimates, not medical advice.
"""

from dataclasses import asdict, dataclass

from app.models import ActivityLevel, Goal, Profile, Sex

ACTIVITY_FACTORS: dict[ActivityLevel, float] = {
    ActivityLevel.sedentary: 1.2,
    ActivityLevel.light: 1.375,
    ActivityLevel.moderate: 1.55,
    ActivityLevel.active: 1.725,
    ActivityLevel.very_active: 1.9,
}

GOAL_ADJUSTMENT: dict[Goal, float] = {
    Goal.cut: -0.20,  # moderate 20% deficit
    Goal.maintain: 0.0,
    Goal.bulk: 0.10,  # lean 10% surplus
}

# Protein in g per kg of body weight.
# 1.6 g/kg is about where muscle-building benefits level off for most people;
# up to 2.2 g/kg (higher end) helps keep muscle when eating in a deficit.
PROTEIN_MIN_PER_KG = 1.6
PROTEIN_MAX_PER_KG = 2.2
PROTEIN_PER_KG: dict[Goal, float] = {  # recommended point inside the range
    Goal.cut: 2.0,
    Goal.maintain: 1.8,
    Goal.bulk: 1.8,
}
# Above BMI 30, protein is based on the weight at BMI 30,
# otherwise g/kg targets get unrealistically high. Below that it has no effect.
PROTEIN_REFERENCE_BMI = 30

FAT_SHARE = 0.25  # recommended: 25% of calories from fat
FAT_MIN_SHARE = 0.20
FAT_MAX_SHARE = 0.35

KCAL_PER_KG_BODY_WEIGHT = 7700  # rough energy content of 1 kg of body weight

# Never recommend intakes below these floors, whatever the inputs.
MIN_CALORIES: dict[Sex, int] = {Sex.male: 1500, Sex.female: 1200}


@dataclass
class Targets:
    bmr: int
    tdee: int  # the burn used for the targets (measured if available, otherwise formula)
    formula_tdee: int
    tdee_source: str  # "formula" or "measured"
    activity_factor: float
    calories: int  # for the user's current goal
    calorie_change: int  # calories - tdee (negative = deficit)
    weekly_change_kg: float  # expected body-weight change per week
    goal_calories: dict[str, int]  # calories for every goal, to compare
    protein_g: int  # recommended
    protein_min_g: int
    protein_max_g: int
    carbs_g: int
    fat_g: int
    fat_min_g: int
    fat_max_g: int
    floor_applied: bool  # true if the safety minimum raised the calories

    def to_dict(self) -> dict:
        return asdict(self)


def bmr(sex: Sex, weight_kg: float, height_cm: float, age: int) -> float:
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if sex == Sex.male else base - 161


def calories_for_goal(tdee: float, goal: Goal, sex: Sex) -> tuple[float, bool]:
    raw = tdee * (1 + GOAL_ADJUSTMENT[goal])
    floor = MIN_CALORIES[sex]
    return max(raw, floor), raw < floor


def protein_weight(weight_kg: float, height_cm: float) -> float:
    reference = PROTEIN_REFERENCE_BMI * (height_cm / 100) ** 2
    return min(weight_kg, reference)


def calculate_targets(profile: Profile) -> Targets:
    b = bmr(profile.sex, profile.weight_kg, profile.height_cm, profile.age)
    factor = ACTIVITY_FACTORS[profile.activity_level]
    formula_tdee = b * factor
    tdee = profile.tdee_override or formula_tdee
    calories, floor_applied = calories_for_goal(tdee, profile.goal, profile.sex)
    goal_calories = {g.value: round(calories_for_goal(tdee, g, profile.sex)[0]) for g in Goal}

    pw = protein_weight(profile.weight_kg, profile.height_cm)
    protein_g = pw * PROTEIN_PER_KG[profile.goal]
    fat_g = calories * FAT_SHARE / 9
    carbs_g = max((calories - protein_g * 4 - fat_g * 9) / 4, 0)

    change = round(calories) - round(tdee)
    return Targets(
        bmr=round(b),
        tdee=round(tdee),
        formula_tdee=round(formula_tdee),
        tdee_source="measured" if profile.tdee_override else "formula",
        activity_factor=factor,
        calories=round(calories),
        calorie_change=change,
        weekly_change_kg=round(change * 7 / KCAL_PER_KG_BODY_WEIGHT, 2),
        goal_calories=goal_calories,
        protein_g=round(protein_g),
        protein_min_g=round(pw * PROTEIN_MIN_PER_KG),
        protein_max_g=round(pw * PROTEIN_MAX_PER_KG),
        carbs_g=round(carbs_g),
        fat_g=round(fat_g),
        fat_min_g=round(calories * FAT_MIN_SHARE / 9),
        fat_max_g=round(calories * FAT_MAX_SHARE / 9),
        floor_applied=floor_applied,
    )


def macros_for(food, grams: float) -> dict[str, float]:
    """Nutrition for `grams` of a food whose values are stored per 100 g."""
    factor = grams / 100
    return {
        "calories": round(food.calories * factor, 1),
        "protein": round(food.protein * factor, 1),
        "carbs": round(food.carbs * factor, 1),
        "fat": round(food.fat * factor, 1),
    }
