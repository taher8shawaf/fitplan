from datetime import date

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models import ActivityLevel, Goal, MealType, Sex


# ---------- Auth ----------
class RegisterIn(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=8, max_length=128)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    name: str


# ---------- Profile ----------
class ProfileIn(BaseModel):
    sex: Sex
    age: int = Field(ge=14, le=100)
    height_cm: float = Field(ge=120, le=230)
    weight_kg: float = Field(ge=35, le=300)
    activity_level: ActivityLevel = ActivityLevel.moderate
    goal: Goal = Goal.maintain


class TargetsOut(BaseModel):
    bmr: int
    tdee: int
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int


class ProfileOut(ProfileIn):
    targets: TargetsOut


# ---------- Workouts ----------
class GeneratePlanIn(BaseModel):
    weekdays: list[int] = Field(description="Training days, 0=Monday ... 6=Sunday", min_length=2, max_length=6)

    @field_validator("weekdays")
    @classmethod
    def valid_days(cls, v: list[int]) -> list[int]:
        if any(d < 0 or d > 6 for d in v):
            raise ValueError("weekdays must be between 0 (Monday) and 6 (Sunday)")
        if len(set(v)) != len(v):
            raise ValueError("weekdays must be unique")
        return sorted(v)


class ExerciseOut(BaseModel):
    id: int
    exercise_key: str
    name_ar: str
    name_en: str
    muscle: str
    sets: int
    reps: str
    last_sets: list[dict] = []
    suggested_weight_kg: float | None = None


class PlanDayOut(BaseModel):
    id: int
    weekday: int
    day_type: str
    title_ar: str
    title_en: str
    exercises: list[ExerciseOut]


class PlanOut(BaseModel):
    id: int
    split: str
    split_ar: str
    split_en: str
    days: list[PlanDayOut]


class TodayOut(BaseModel):
    date: date
    has_plan: bool
    is_rest_day: bool
    day: PlanDayOut | None = None
    logged: bool = False


class ExerciseAddIn(BaseModel):
    exercise_key: str
    sets: int = Field(default=3, ge=1, le=10)
    reps: str = Field(default="8-12", max_length=20)


class ExerciseUpdateIn(BaseModel):
    sets: int | None = Field(default=None, ge=1, le=10)
    reps: str | None = Field(default=None, max_length=20)


class SetIn(BaseModel):
    exercise_key: str
    set_number: int = Field(ge=1, le=20)
    weight_kg: float = Field(ge=0, le=600)
    reps: int = Field(ge=0, le=100)


class WorkoutLogIn(BaseModel):
    day: date
    plan_day_id: int | None = None
    notes: str | None = Field(default=None, max_length=500)
    sets: list[SetIn] = Field(min_length=1)


class WorkoutLogOut(BaseModel):
    id: int
    day: date
    plan_day_id: int | None
    notes: str | None
    sets: list[SetIn]


class ProgressPoint(BaseModel):
    day: date
    max_weight_kg: float
    best_set_reps: int
    estimated_1rm: float


# ---------- Nutrition ----------
class FoodIn(BaseModel):
    name_ar: str = Field(min_length=1, max_length=100)
    name_en: str = Field(min_length=1, max_length=100)
    calories: float = Field(ge=0, le=900)
    protein: float = Field(ge=0, le=100)
    carbs: float = Field(ge=0, le=100)
    fat: float = Field(ge=0, le=100)
    serving_g: float = Field(default=100, gt=0, le=2000)
    serving_ar: str = "١٠٠ غ"
    serving_en: str = "100 g"


class FoodOut(FoodIn):
    id: int
    is_custom: bool


class MealIn(BaseModel):
    day: date
    meal_type: MealType
    food_id: int
    grams: float = Field(gt=0, le=3000)


class Macros(BaseModel):
    calories: float
    protein: float
    carbs: float
    fat: float


class MealEntryOut(BaseModel):
    id: int
    day: date
    meal_type: MealType
    food_id: int
    food_ar: str
    food_en: str
    grams: float
    macros: Macros


class DayNutritionOut(BaseModel):
    day: date
    entries: list[MealEntryOut]
    totals: Macros
    targets: TargetsOut | None
    remaining: Macros | None
