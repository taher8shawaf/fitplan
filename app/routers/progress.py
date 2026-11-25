"""Progress dashboard: one request that gathers weight, lifts, adherence and nutrition."""

from datetime import date, timedelta

from fastapi import APIRouter, Query
from sqlmodel import func, select

from app.deps import CurrentUser, SessionDep
from app.models import CustomExercise, Food, MealEntry, PlanDay, Profile, SetLog, WeightLog, WorkoutLog, WorkoutPlan
from app.services import progress
from app.services.exercise_guides import GUIDES
from app.services.nutrition import calculate_targets
from app.services.workouts import CUSTOM_PREFIX, EXERCISES

router = APIRouter(tags=["progress"])


@router.get("/api/progress")
def get_progress(
    user: CurrentUser,
    session: SessionDep,
    today: date | None = Query(None, description="The user's local date (defaults to the server's)."),
):
    today = today or date.today()

    weights = session.exec(
        select(WeightLog.day, WeightLog.weight_kg).where(
            WeightLog.user_id == user.id, WeightLog.day >= today - timedelta(weeks=9)
        )
    ).all()

    sets = session.exec(
        select(WorkoutLog.day, SetLog.exercise_key, SetLog.weight_kg, SetLog.reps)
        .join(SetLog, SetLog.workout_log_id == WorkoutLog.id)
        .where(WorkoutLog.user_id == user.id, WorkoutLog.day >= today - timedelta(days=90))
    ).all()
    lifts = progress.lift_summary(list(sets))
    for row in lifts:
        info = EXERCISES.get(row["exercise_key"])
        row["name_ar"] = info["ar"] if info else row["exercise_key"]
        row["name_en"] = info["en"] if info else row["exercise_key"]

    plan = session.exec(
        select(WorkoutPlan).where(WorkoutPlan.user_id == user.id, WorkoutPlan.is_active == True)  # noqa: E712
    ).first()
    planned = (
        session.exec(select(func.count()).select_from(PlanDay).where(PlanDay.plan_id == plan.id)).one() if plan else 0
    )
    workout_days = session.exec(
        select(WorkoutLog.day).where(WorkoutLog.user_id == user.id, WorkoutLog.day >= today - timedelta(weeks=5))
    ).all()

    daily_rows = session.exec(
        select(
            MealEntry.day,
            func.sum(Food.calories * MealEntry.grams / 100),
            func.sum(Food.protein * MealEntry.grams / 100),
        )
        .join(Food, Food.id == MealEntry.food_id)
        .where(MealEntry.user_id == user.id, MealEntry.day > today - timedelta(days=7), MealEntry.day <= today)
        .group_by(MealEntry.day)
    ).all()
    daily = {d: (float(kcal or 0), float(protein or 0)) for d, kcal, protein in daily_rows}

    profile = session.get(Profile, user.id)
    targets = calculate_targets(profile) if profile else None

    return {
        "today": today,
        "goal": profile.goal if profile else None,
        "weight": progress.weight_summary(list(weights), today),
        "lifts": lifts,
        "adherence": progress.adherence(list(workout_days), planned, today),
        "nutrition": {
            "target_calories": targets.calories if targets else None,
            "target_protein": targets.protein_g if targets else None,
            "protein_min": targets.protein_min_g if targets else None,
            **progress.nutrition_summary(
                daily, today, targets.calories if targets else 0, targets.protein_min_g if targets else 0
            ),
        },
    }


@router.get("/api/progress/muscles")
def muscle_progress(
    user: CurrentUser,
    session: SessionDep,
    today: date | None = Query(None, description="The user's local date."),
    weeks_ago: int = Query(0, ge=0, le=26, description="0 = this week, 1 = last week, ..."),
):
    """Sets per muscle for one week (for the body map) and strength trend per muscle group."""
    from app.routers.workouts import GROUP_TO_MUSCLES

    today = today or date.today()
    muscles_for = {k: (g["primary"], g["secondary"]) for k, g in GUIDES.items()}
    group_of = {k: v["muscle"] for k, v in EXERCISES.items() if v["muscle"] != "cardio"}
    for c in session.exec(select(CustomExercise).where(CustomExercise.user_id == user.id)):
        key = f"{CUSTOM_PREFIX}{c.id}"
        muscles_for[key] = (GROUP_TO_MUSCLES.get(c.muscle, []), [])
        if c.muscle not in ("cardio", "other"):
            group_of[key] = c.muscle

    rows = session.exec(
        select(WorkoutLog.day, SetLog.exercise_key, SetLog.weight_kg, SetLog.reps)
        .join(SetLog, SetLog.workout_log_id == WorkoutLog.id)
        .where(WorkoutLog.user_id == user.id, WorkoutLog.day >= today - timedelta(weeks=max(9, weeks_ago + 1)))
    ).all()
    week = progress.week_start(today) - timedelta(weeks=weeks_ago)
    return {
        "map": progress.muscle_map([(d, k) for d, k, _, _ in rows], muscles_for, week, today),
        "groups": progress.strength_by_group(list(rows), group_of, today),
    }
