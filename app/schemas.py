from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from app.models import ActivityLevel, Goal, MealType, Sex


# ---------- Auth ----------
class RegisterIn(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=8, max_length=128)
    username: str | None = Field(default=None, max_length=21)


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
    username: str | None = None
    is_private: bool = False


class SocialSettingsIn(BaseModel):
    username: str | None = Field(default=None, max_length=21)
    is_private: bool | None = None


class PublicUser(BaseModel):
    username: str
    name: str
    is_following: bool = False
    follows_you: bool = False
    followers: int = 0
    following: int = 0


class FeedExercise(BaseModel):
    key: str
    name_ar: str
    name_en: str
    sets: int
    best_weight_kg: float
    best_reps: int


class FeedItem(BaseModel):
    id: int
    user: PublicUser
    day: date
    created_at: datetime
    title_ar: str | None
    title_en: str | None
    sets_count: int
    volume_kg: float
    exercises: list[FeedExercise]
    likes: int
    liked_by_me: bool
    is_mine: bool


class ProfileView(BaseModel):
    user: PublicUser
    is_me: bool
    is_private: bool
    workouts_count: int | None  # None when hidden
    workouts: list[FeedItem]


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
    formula_tdee: int
    tdee_source: str
    activity_factor: float
    calories: int
    calorie_change: int
    weekly_change_kg: float
    goal_calories: dict[str, int]
    protein_g: int
    protein_min_g: int
    protein_max_g: int
    carbs_g: int
    fat_g: int
    fat_min_g: int
    fat_max_g: int
    floor_applied: bool


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


class PlanDayIn(BaseModel):
    weekday: int = Field(ge=0, le=6)
    title: str | None = Field(default=None, max_length=40)


class PlanDayUpdateIn(BaseModel):
    weekday: int | None = Field(default=None, ge=0, le=6)
    title: str | None = Field(default=None, max_length=40)


class CustomPlanIn(BaseModel):
    days: list[PlanDayIn] = Field(default_factory=list, max_length=7)

    @field_validator("days")
    @classmethod
    def unique_weekdays(cls, v: list[PlanDayIn]) -> list[PlanDayIn]:
        if len({d.weekday for d in v}) != len(v):
            raise ValueError("weekdays must be unique")
        return v


class MoveIn(BaseModel):
    direction: Literal["up", "down"]


class CustomExerciseIn(BaseModel):
    name_ar: str = Field(min_length=1, max_length=60)
    name_en: str = Field(min_length=1, max_length=60)
    muscle: str = Field(default="other", max_length=20)


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
    title: str | None = None
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
    sets: int = Field(default=3, ge=1, le=15)
    reps: str = Field(default="8-12", min_length=1, max_length=20)


class ExerciseUpdateIn(BaseModel):
    sets: int | None = Field(default=None, ge=1, le=15)
    reps: str | None = Field(default=None, min_length=1, max_length=20)


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
    serving_ar: str = "100 غ"
    serving_en: str = "100 g"


class FoodOut(FoodIn):
    id: int
    is_custom: bool
    kind: str = "food"


class BatchItemIn(BaseModel):
    food_id: int | None = None
    food: FoodIn | None = None  # a new food to create on the fly
    grams: float = Field(gt=0, le=3000)

    @model_validator(mode="after")
    def one_source(self):
        if (self.food_id is None) == (self.food is None):
            raise ValueError("give exactly one of food_id or food")
        return self


class BatchMealIn(BaseModel):
    day: date
    meal_type: MealType
    items: list[BatchItemIn] = Field(min_length=1, max_length=20)


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


# ---------- Quick add, copy, saved meals, recipes ----------
class QuickAddIn(BaseModel):
    day: date
    meal_type: MealType
    name: str = Field(default="", max_length=60)
    calories: float = Field(gt=0, le=5000)
    protein: float = Field(default=0, ge=0, le=400)
    carbs: float = Field(default=0, ge=0, le=800)
    fat: float = Field(default=0, ge=0, le=400)


class CopyMealsIn(BaseModel):
    from_day: date
    to_day: date
    meal_type: MealType | None = None  # None = the whole day


class FoodAmount(BaseModel):
    food_id: int
    grams: float = Field(gt=0, le=3000)


class SavedMealIn(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    items: list[FoodAmount] = Field(min_length=1, max_length=30)


class SavedMealItemOut(BaseModel):
    food_id: int
    food_ar: str
    food_en: str
    grams: float


class SavedMealOut(BaseModel):
    id: int
    name: str
    items: list[SavedMealItemOut]
    totals: Macros


class LogSavedMealIn(BaseModel):
    day: date
    meal_type: MealType


class RecipeIn(BaseModel):
    name_ar: str = Field(min_length=1, max_length=100)
    name_en: str = Field(min_length=1, max_length=100)
    servings: int = Field(ge=1, le=50)
    ingredients: list[FoodAmount] = Field(min_length=1, max_length=40)
    cooked_weight_g: float | None = Field(default=None, gt=0, le=50000)


class RecipeOut(BaseModel):
    id: int
    food: FoodOut
    servings: int
    total_weight_g: float
    per_serving: Macros
    ingredients: list[SavedMealItemOut]


# ---------- Water & weight ----------
class WaterIn(BaseModel):
    day: date
    ml: int = Field(ge=-5000, le=5000, description="amount to add (negative to remove)")


class WaterOut(BaseModel):
    day: date
    ml: int
    goal_ml: int


class WeightIn(BaseModel):
    day: date
    weight_kg: float = Field(ge=30, le=300)


class WeightOut(BaseModel):
    day: date
    weight_kg: float


class AdaptiveOut(BaseModel):
    status: str  # "collecting" or "ready"
    window_days: int
    weigh_ins: int
    weigh_ins_needed: int
    logged_days: int
    logged_days_needed: int
    span_days: int
    span_days_needed: int
    estimated_tdee: int | None = None
    formula_tdee: int | None = None
    avg_intake: int | None = None
    weekly_change_kg: float | None = None
    suggested_calories: int | None = None
    applied: bool = False
