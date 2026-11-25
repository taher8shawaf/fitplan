from datetime import UTC, date, datetime
from enum import StrEnum

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(UTC)


class Sex(StrEnum):
    male = "male"
    female = "female"


class ActivityLevel(StrEnum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    active = "active"
    very_active = "very_active"


class Goal(StrEnum):
    cut = "cut"
    maintain = "maintain"
    bulk = "bulk"


class MealType(StrEnum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"


# ---------- Users ----------
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: str
    hashed_password: str
    username: str | None = Field(default=None, index=True, unique=True)  # public @handle
    is_private: bool = False  # hide workouts from everyone else
    created_at: datetime = Field(default_factory=utcnow)


class Follow(SQLModel, table=True):
    follower_id: int = Field(foreign_key="user.id", primary_key=True)
    followee_id: int = Field(foreign_key="user.id", primary_key=True, index=True)
    created_at: datetime = Field(default_factory=utcnow)


class Profile(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    sex: Sex
    age: int
    height_cm: float
    weight_kg: float
    activity_level: ActivityLevel = ActivityLevel.moderate
    goal: Goal = Goal.maintain
    # Real daily burn measured from the user's own weight + food logs (adaptive TDEE).
    # When set, it replaces the formula estimate.
    tdee_override: int | None = None
    updated_at: datetime = Field(default_factory=utcnow)


# ---------- Workouts ----------
class WorkoutPlan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    split: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=utcnow)


class PlanDay(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="workoutplan.id", index=True, ondelete="CASCADE")
    weekday: int  # 0 = Monday ... 6 = Sunday (ISO, like Python's date.weekday())
    day_type: str  # e.g. "push", "upper_a", or "custom"
    title: str | None = None  # user-defined name; overrides the template title


class PlanExercise(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plan_day_id: int = Field(foreign_key="planday.id", index=True, ondelete="CASCADE")
    exercise_key: str
    sets: int
    reps: str  # "8-12", "5", "30-45s"
    position: int = 0


class CustomExercise(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    name_ar: str
    name_en: str
    muscle: str = "other"


class WorkoutLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    plan_day_id: int | None = Field(default=None, foreign_key="planday.id", index=True)
    day: date = Field(index=True)
    notes: str | None = None
    created_at: datetime = Field(default_factory=utcnow)


class SetLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    workout_log_id: int = Field(foreign_key="workoutlog.id", index=True, ondelete="CASCADE")
    exercise_key: str = Field(index=True)
    set_number: int
    weight_kg: float
    reps: int


# ---------- Nutrition ----------
class Food(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name_ar: str
    name_en: str
    # values per 100 g
    calories: float
    protein: float
    carbs: float
    fat: float
    serving_g: float = 100
    serving_ar: str = "100 غ"
    serving_en: str = "100 g"
    owner_id: int | None = Field(default=None, foreign_key="user.id", index=True)  # None = built-in
    kind: str = "food"  # "food", "recipe" (built from ingredients) or "quick" (quick-add, hidden from search)


class MealEntry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    food_id: int = Field(foreign_key="food.id", index=True)
    day: date = Field(index=True)
    meal_type: MealType
    grams: float
    created_at: datetime = Field(default_factory=utcnow)


class WorkoutLike(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    workout_log_id: int = Field(foreign_key="workoutlog.id", primary_key=True, index=True)
    created_at: datetime = Field(default_factory=utcnow)


# ---------- Saved meals & recipes ----------
class SavedMeal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    name: str
    created_at: datetime = Field(default_factory=utcnow)


class SavedMealItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    saved_meal_id: int = Field(foreign_key="savedmeal.id", index=True)
    food_id: int = Field(foreign_key="food.id", index=True)
    grams: float


class Recipe(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    food_id: int = Field(foreign_key="food.id", index=True)  # the food that gets logged
    servings: int
    total_weight_g: float


class RecipeIngredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    recipe_id: int = Field(foreign_key="recipe.id", index=True)
    food_id: int = Field(foreign_key="food.id", index=True)
    grams: float


# ---------- Body weight & water ----------
class WeightLog(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    day: date = Field(primary_key=True)
    weight_kg: float


class WaterLog(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    day: date = Field(primary_key=True)
    ml: int = 0
