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

PROTEIN_PER_KG: dict[Goal, float] = {
    Goal.cut: 2.0,
    Goal.maintain: 1.8,
    Goal.bulk: 1.8,
}

FAT_SHARE = 0.25  # 25% of calories from fat

# Never recommend intakes below these floors, whatever the inputs.
MIN_CALORIES: dict[Sex, int] = {Sex.male: 1500, Sex.female: 1200}


@dataclass
class Targets:
    bmr: int
    tdee: int
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int

    def to_dict(self) -> dict:
        return asdict(self)


def bmr(sex: Sex, weight_kg: float, height_cm: float, age: int) -> float:
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if sex == Sex.male else base - 161


def calculate_targets(profile: Profile) -> Targets:
    b = bmr(profile.sex, profile.weight_kg, profile.height_cm, profile.age)
    tdee = b * ACTIVITY_FACTORS[profile.activity_level]
    calories = tdee * (1 + GOAL_ADJUSTMENT[profile.goal])
    calories = max(calories, MIN_CALORIES[profile.sex])

    protein_g = profile.weight_kg * PROTEIN_PER_KG[profile.goal]
    fat_g = calories * FAT_SHARE / 9
    carbs_g = max((calories - protein_g * 4 - fat_g * 9) / 4, 0)

    return Targets(
        bmr=round(b),
        tdee=round(tdee),
        calories=round(calories),
        protein_g=round(protein_g),
        carbs_g=round(carbs_g),
        fat_g=round(fat_g),
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
