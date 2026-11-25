"""Usernames and workout summaries for the social feed."""

import re
import secrets

from sqlmodel import Session, col, select

from app.models import CustomExercise, PlanDay, SetLog, User, WorkoutLog
from app.services.workouts import CUSTOM_PREFIX, DAY_TYPES, EXERCISES

USERNAME_RE = re.compile(r"^[a-z0-9_.]{3,20}$")
RESERVED = {"me", "search", "admin", "api"}


def valid_username(username: str) -> bool:
    return bool(USERNAME_RE.match(username)) and username not in RESERVED


def normalize_username(raw: str) -> str:
    return raw.strip().lstrip("@").lower()


def unique_username(session: Session, seed: str) -> str:
    """Make a valid, unused username from any text (e.g. the part of an email before @)."""
    base = re.sub(r"[^a-z0-9_.]", "", seed.lower())[:15] or "user"
    if len(base) < 3:
        base = f"{base}fit"
    if base in RESERVED:
        base = f"{base}fit"
    candidate = base
    while session.exec(select(User.id).where(User.username == candidate)).first() is not None:
        candidate = f"{base}{secrets.randbelow(10_000)}"
    return candidate


def exercise_names(session: Session, key: str) -> tuple[str, str]:
    """Arabic and English name of any exercise, including other users' custom ones."""
    if key in EXERCISES:
        return EXERCISES[key]["ar"], EXERCISES[key]["en"]
    if key.startswith(CUSTOM_PREFIX) and key[len(CUSTOM_PREFIX) :].isdigit():
        custom = session.get(CustomExercise, int(key[len(CUSTOM_PREFIX) :]))
        if custom:
            return custom.name_ar, custom.name_en
    return key, key


def workout_summary(session: Session, log: WorkoutLog) -> dict:
    sets = list(session.exec(select(SetLog).where(SetLog.workout_log_id == log.id).order_by(col(SetLog.id))))
    exercises: dict[str, dict] = {}
    for s in sets:
        ex = exercises.get(s.exercise_key)
        if ex is None:
            name_ar, name_en = exercise_names(session, s.exercise_key)
            ex = exercises[s.exercise_key] = {
                "key": s.exercise_key,
                "name_ar": name_ar,
                "name_en": name_en,
                "sets": 0,
                "best_weight_kg": 0.0,
                "best_reps": 0,
            }
        ex["sets"] += 1
        if (s.weight_kg, s.reps) > (ex["best_weight_kg"], ex["best_reps"]):
            ex["best_weight_kg"], ex["best_reps"] = s.weight_kg, s.reps

    title_ar = title_en = None
    if log.plan_day_id and (day := session.get(PlanDay, log.plan_day_id)):
        template = DAY_TYPES.get(day.day_type, DAY_TYPES["custom"])
        title_ar, title_en = day.title or template["ar"], day.title or template["en"]

    return {
        "title_ar": title_ar,
        "title_en": title_en,
        "sets_count": len(sets),
        "volume_kg": round(sum(s.weight_kg * s.reps for s in sets), 1),
        "exercises": list(exercises.values()),
    }
