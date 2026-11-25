from datetime import date
from urllib.parse import quote_plus

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session, col, select

from app.deps import CurrentUser, SessionDep
from app.models import CustomExercise, PlanDay, PlanExercise, SetLog, User, WorkoutLike, WorkoutLog, WorkoutPlan
from app.schemas import (
    CustomExerciseIn,
    CustomPlanIn,
    ExerciseAddIn,
    ExerciseOut,
    ExerciseUpdateIn,
    GeneratePlanIn,
    MoveIn,
    PlanDayIn,
    PlanDayOut,
    PlanDayUpdateIn,
    PlanOut,
    ProgressPoint,
    SetIn,
    TodayOut,
    WorkoutLogIn,
    WorkoutLogOut,
)
from app.services.exercise_guides import GUIDES
from app.services.workouts import (
    CUSTOM_PREFIX,
    DAY_TYPES,
    EXERCISES,
    MUSCLES,
    SPLIT_NAMES,
    TEMPLATES,
    choose_split,
    suggest_next_weight,
)

router = APIRouter(tags=["workouts"])
NOT_FOUND = HTTPException(status.HTTP_404_NOT_FOUND, "Not found")


# ---------- helpers ----------
def exercise_info(session: Session, user: User, key: str) -> dict[str, str] | None:
    """Look up a built-in exercise, or one of the user's custom exercises (key 'custom_<id>')."""
    if key in EXERCISES:
        return EXERCISES[key]
    if key.startswith(CUSTOM_PREFIX) and key[len(CUSTOM_PREFIX) :].isdigit():
        custom = session.get(CustomExercise, int(key[len(CUSTOM_PREFIX) :]))
        if custom and custom.user_id == user.id:
            return {"ar": custom.name_ar, "en": custom.name_en, "muscle": custom.muscle}
    return None


def require_exercise(session: Session, user: User, key: str) -> dict[str, str]:
    info = exercise_info(session, user, key)
    if info is None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"Unknown exercise: {key}")
    return info


def active_plan(session: Session, user: User) -> WorkoutPlan | None:
    return session.exec(
        select(WorkoutPlan)
        .where(WorkoutPlan.user_id == user.id, WorkoutPlan.is_active == True)  # noqa: E712
        .order_by(col(WorkoutPlan.id).desc())
    ).first()


def require_active_plan(session: Session, user: User) -> WorkoutPlan:
    plan = active_plan(session, user)
    if not plan:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No active plan")
    return plan


def deactivate_plans(session: Session, user: User) -> None:
    # Old plans are kept (workout history points at their days), but only one is active.
    for old in session.exec(
        select(WorkoutPlan).where(WorkoutPlan.user_id == user.id, WorkoutPlan.is_active == True)  # noqa: E712
    ):
        old.is_active = False
        session.add(old)


def owned_plan_day(session: Session, user: User, day_id: int) -> PlanDay:
    day = session.get(PlanDay, day_id)
    if not day:
        raise NOT_FOUND
    plan = session.get(WorkoutPlan, day.plan_id)
    if not plan or plan.user_id != user.id:
        raise NOT_FOUND  # 404 not 403: don't reveal that other users' ids exist
    return day


def owned_exercise(session: Session, user: User, exercise_id: int) -> PlanExercise:
    ex = session.get(PlanExercise, exercise_id)
    if not ex:
        raise NOT_FOUND
    owned_plan_day(session, user, ex.plan_day_id)
    return ex


def ensure_weekday_free(session: Session, plan_id: int, weekday: int, except_day_id: int | None = None) -> None:
    clash = session.exec(select(PlanDay).where(PlanDay.plan_id == plan_id, PlanDay.weekday == weekday)).first()
    if clash and clash.id != except_day_id:
        raise HTTPException(status.HTTP_409_CONFLICT, "That weekday already has a workout")


def day_exercises(session: Session, day_id: int) -> list[PlanExercise]:
    return list(
        session.exec(
            select(PlanExercise)
            .where(PlanExercise.plan_day_id == day_id)
            .order_by(col(PlanExercise.position), col(PlanExercise.id))
        )
    )


def last_sets(session: Session, user: User, exercise_key: str) -> list[SetLog]:
    """Sets from the most recent workout in which this exercise was logged."""
    latest = session.exec(
        select(WorkoutLog.id)
        .join(SetLog, col(SetLog.workout_log_id) == col(WorkoutLog.id))
        .where(WorkoutLog.user_id == user.id, SetLog.exercise_key == exercise_key)
        .order_by(col(WorkoutLog.day).desc(), col(WorkoutLog.id).desc())
    ).first()
    if latest is None:
        return []
    return list(
        session.exec(
            select(SetLog)
            .where(SetLog.workout_log_id == latest, SetLog.exercise_key == exercise_key)
            .order_by(col(SetLog.set_number))
        )
    )


def exercise_out(session: Session, user: User, ex: PlanExercise, with_history: bool) -> ExerciseOut:
    info = exercise_info(session, user, ex.exercise_key) or {
        "ar": ex.exercise_key,
        "en": ex.exercise_key,
        "muscle": "other",
    }
    history: list[SetLog] = last_sets(session, user, ex.exercise_key) if with_history else []
    return ExerciseOut(
        id=ex.id,
        exercise_key=ex.exercise_key,
        name_ar=info["ar"],
        name_en=info["en"],
        muscle=info["muscle"],
        sets=ex.sets,
        reps=ex.reps,
        last_sets=[{"weight_kg": s.weight_kg, "reps": s.reps} for s in history],
        suggested_weight_kg=suggest_next_weight(ex.reps, [(s.weight_kg, s.reps) for s in history]),
    )


def day_out(session: Session, user: User, day: PlanDay, with_history: bool = False) -> PlanDayOut:
    template = DAY_TYPES.get(day.day_type, DAY_TYPES["custom"])
    return PlanDayOut(
        id=day.id,
        weekday=day.weekday,
        day_type=day.day_type,
        title=day.title,
        title_ar=day.title or template["ar"],
        title_en=day.title or template["en"],
        exercises=[exercise_out(session, user, e, with_history) for e in day_exercises(session, day.id)],
    )


def plan_out(session: Session, user: User, plan: WorkoutPlan) -> PlanOut:
    days = session.exec(select(PlanDay).where(PlanDay.plan_id == plan.id).order_by(col(PlanDay.weekday)))
    names = SPLIT_NAMES.get(plan.split, SPLIT_NAMES["custom"])
    return PlanOut(
        id=plan.id,
        split=plan.split,
        split_ar=names["ar"],
        split_en=names["en"],
        days=[day_out(session, user, d) for d in days],
    )


# ---------- exercise library ----------
@router.get("/api/exercises")
def list_exercises(user: CurrentUser, session: SessionDep):
    builtin = [{"key": k, **v, "custom": False} for k, v in EXERCISES.items()]
    custom = [
        {"key": f"{CUSTOM_PREFIX}{c.id}", "ar": c.name_ar, "en": c.name_en, "muscle": c.muscle, "custom": True}
        for c in session.exec(select(CustomExercise).where(CustomExercise.user_id == user.id))
    ]
    return custom + builtin


# muscle group -> body-map muscles, for custom exercises without a written guide
GROUP_TO_MUSCLES = {
    "chest": ["chest"],
    "back": ["lats"],
    "shoulders": ["shoulders"],
    "legs": ["quads", "hamstrings", "glutes"],
    "arms": ["biceps", "triceps"],
    "biceps": ["biceps"],
    "triceps": ["triceps"],
    "forearms": ["forearms"],
    "core": ["abs"],
}


@router.get("/api/exercises/{key}/guide")
def exercise_guide(key: str, user: CurrentUser, session: SessionDep):
    info = exercise_info(session, user, key)
    if info is None:
        raise NOT_FOUND
    guide = GUIDES.get(key)
    query = quote_plus(f"{info['en']} exercise proper form")
    return {
        "key": key,
        "ar": info["ar"],
        "en": info["en"],
        "muscle": info["muscle"],
        "primary": guide["primary"] if guide else info.get("primary") or GROUP_TO_MUSCLES.get(info["muscle"], []),
        "secondary": guide["secondary"] if guide else info.get("secondary", []),
        "steps_ar": guide["steps_ar"] if guide else [],
        "steps_en": guide["steps_en"] if guide else [],
        "tip_ar": guide["tip_ar"] if guide else None,
        "tip_en": guide["tip_en"] if guide else None,
        "video_url": f"https://www.youtube.com/results?search_query={query}",
    }


@router.post("/api/exercises", status_code=status.HTTP_201_CREATED)
def create_custom_exercise(data: CustomExerciseIn, user: CurrentUser, session: SessionDep):
    if data.muscle not in MUSCLES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"muscle must be one of {MUSCLES}")
    ex = CustomExercise(user_id=user.id, **data.model_dump())
    session.add(ex)
    session.commit()
    session.refresh(ex)
    return {"key": f"{CUSTOM_PREFIX}{ex.id}", "ar": ex.name_ar, "en": ex.name_en, "muscle": ex.muscle, "custom": True}


# ---------- plan ----------
@router.post("/api/workouts/plan", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
def generate_plan(data: GeneratePlanIn, user: CurrentUser, session: SessionDep):
    """Create a ready-made plan from a template, based on the chosen training days."""
    deactivate_plans(session, user)
    split, day_types = choose_split(len(data.weekdays))
    plan = WorkoutPlan(user_id=user.id, split=split)
    session.add(plan)
    session.flush()

    for weekday, day_type in zip(data.weekdays, day_types, strict=True):
        day = PlanDay(plan_id=plan.id, weekday=weekday, day_type=day_type)
        session.add(day)
        session.flush()
        for pos, (key, sets, reps) in enumerate(TEMPLATES[day_type]):
            session.add(PlanExercise(plan_day_id=day.id, exercise_key=key, sets=sets, reps=reps, position=pos))

    session.commit()
    session.refresh(plan)
    return plan_out(session, user, plan)


@router.post("/api/workouts/plan/custom", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
def create_custom_plan(data: CustomPlanIn, user: CurrentUser, session: SessionDep):
    """Start an empty plan that the user builds from scratch."""
    deactivate_plans(session, user)
    plan = WorkoutPlan(user_id=user.id, split="custom")
    session.add(plan)
    session.flush()
    for d in data.days:
        session.add(PlanDay(plan_id=plan.id, weekday=d.weekday, day_type="custom", title=_clean(d.title)))
    session.commit()
    session.refresh(plan)
    return plan_out(session, user, plan)


@router.get("/api/workouts/plan", response_model=PlanOut)
def get_plan(user: CurrentUser, session: SessionDep):
    return plan_out(session, user, require_active_plan(session, user))


def _clean(title: str | None) -> str | None:
    return title.strip() or None if title else None


@router.post("/api/workouts/plan/days", response_model=PlanDayOut, status_code=status.HTTP_201_CREATED)
def add_day(data: PlanDayIn, user: CurrentUser, session: SessionDep):
    plan = require_active_plan(session, user)
    ensure_weekday_free(session, plan.id, data.weekday)
    day = PlanDay(plan_id=plan.id, weekday=data.weekday, day_type="custom", title=_clean(data.title))
    session.add(day)
    session.commit()
    session.refresh(day)
    return day_out(session, user, day)


@router.patch("/api/workouts/plan/days/{day_id}", response_model=PlanDayOut)
def update_day(day_id: int, data: PlanDayUpdateIn, user: CurrentUser, session: SessionDep):
    day = owned_plan_day(session, user, day_id)
    fields = data.model_dump(exclude_unset=True)
    if fields.get("weekday") is not None:
        ensure_weekday_free(session, day.plan_id, data.weekday, except_day_id=day.id)
        day.weekday = data.weekday
    if "title" in fields:
        day.title = _clean(data.title)
    session.add(day)
    session.commit()
    session.refresh(day)
    return day_out(session, user, day)


@router.delete("/api/workouts/plan/days/{day_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_day(day_id: int, user: CurrentUser, session: SessionDep):
    day = owned_plan_day(session, user, day_id)
    for ex in day_exercises(session, day.id):
        session.delete(ex)
    # Keep logged workouts, just unlink them from the deleted day.
    for log in session.exec(select(WorkoutLog).where(WorkoutLog.plan_day_id == day.id)):
        log.plan_day_id = None
        session.add(log)
    session.flush()  # children first, so the foreign key is never broken
    session.delete(day)
    session.commit()


@router.get("/api/workouts/today", response_model=TodayOut)
def today(user: CurrentUser, session: SessionDep, day: date = Query(default_factory=date.today)):
    """`day` should be sent by the client in the user's local time zone."""
    logged = (
        session.exec(select(WorkoutLog.id).where(WorkoutLog.user_id == user.id, WorkoutLog.day == day)).first()
        is not None
    )
    plan = active_plan(session, user)
    if not plan:
        return TodayOut(date=day, has_plan=False, is_rest_day=True, logged=logged)
    plan_day = session.exec(select(PlanDay).where(PlanDay.plan_id == plan.id, PlanDay.weekday == day.weekday())).first()
    if not plan_day:
        return TodayOut(date=day, has_plan=True, is_rest_day=True, logged=logged)
    return TodayOut(
        date=day,
        has_plan=True,
        is_rest_day=False,
        day=day_out(session, user, plan_day, with_history=True),
        logged=logged,
    )


@router.post(
    "/api/workouts/plan/days/{day_id}/exercises",
    response_model=ExerciseOut,
    status_code=status.HTTP_201_CREATED,
)
def add_exercise(day_id: int, data: ExerciseAddIn, user: CurrentUser, session: SessionDep):
    owned_plan_day(session, user, day_id)
    require_exercise(session, user, data.exercise_key)
    existing = day_exercises(session, day_id)
    position = max((e.position for e in existing), default=-1) + 1
    ex = PlanExercise(plan_day_id=day_id, position=position, **data.model_dump())
    session.add(ex)
    session.commit()
    session.refresh(ex)
    return exercise_out(session, user, ex, with_history=False)


@router.patch("/api/workouts/plan/exercises/{exercise_id}", response_model=ExerciseOut)
def update_exercise(exercise_id: int, data: ExerciseUpdateIn, user: CurrentUser, session: SessionDep):
    ex = owned_exercise(session, user, exercise_id)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(ex, key, value.strip() if isinstance(value, str) else value)
    session.add(ex)
    session.commit()
    session.refresh(ex)
    return exercise_out(session, user, ex, with_history=False)


@router.post("/api/workouts/plan/exercises/{exercise_id}/move", response_model=PlanDayOut)
def move_exercise(exercise_id: int, data: MoveIn, user: CurrentUser, session: SessionDep):
    ex = owned_exercise(session, user, exercise_id)
    exercises = day_exercises(session, ex.plan_day_id)
    i = next(idx for idx, e in enumerate(exercises) if e.id == ex.id)
    j = i - 1 if data.direction == "up" else i + 1
    if 0 <= j < len(exercises):
        exercises[i], exercises[j] = exercises[j], exercises[i]
        for pos, e in enumerate(exercises):  # renumber so positions are always 0..n-1
            e.position = pos
            session.add(e)
        session.commit()
    return day_out(session, user, session.get(PlanDay, ex.plan_day_id))


@router.delete("/api/workouts/plan/exercises/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, user: CurrentUser, session: SessionDep):
    ex = owned_exercise(session, user, exercise_id)
    session.delete(ex)
    session.commit()


# ---------- logs ----------
def log_out(session: Session, log: WorkoutLog) -> WorkoutLogOut:
    sets = session.exec(select(SetLog).where(SetLog.workout_log_id == log.id).order_by(col(SetLog.id)))
    return WorkoutLogOut(
        id=log.id,
        day=log.day,
        plan_day_id=log.plan_day_id,
        notes=log.notes,
        sets=[
            SetIn(exercise_key=s.exercise_key, set_number=s.set_number, weight_kg=s.weight_kg, reps=s.reps)
            for s in sets
        ],
    )


@router.post("/api/workouts/logs", response_model=WorkoutLogOut, status_code=status.HTTP_201_CREATED)
def create_log(data: WorkoutLogIn, user: CurrentUser, session: SessionDep):
    if data.plan_day_id is not None:
        owned_plan_day(session, user, data.plan_day_id)
    for key in {s.exercise_key for s in data.sets}:
        require_exercise(session, user, key)

    log = WorkoutLog(user_id=user.id, day=data.day, plan_day_id=data.plan_day_id, notes=data.notes)
    session.add(log)
    session.flush()
    for s in data.sets:
        session.add(SetLog(workout_log_id=log.id, **s.model_dump()))
    session.commit()
    session.refresh(log)
    return log_out(session, log)


@router.get("/api/workouts/logs", response_model=list[WorkoutLogOut])
def list_logs(user: CurrentUser, session: SessionDep, limit: int = Query(20, ge=1, le=100)):
    logs = session.exec(
        select(WorkoutLog)
        .where(WorkoutLog.user_id == user.id)
        .order_by(col(WorkoutLog.day).desc(), col(WorkoutLog.id).desc())
        .limit(limit)
    )
    return [log_out(session, log) for log in logs]


@router.delete("/api/workouts/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(log_id: int, user: CurrentUser, session: SessionDep):
    log = session.get(WorkoutLog, log_id)
    if not log or log.user_id != user.id:
        raise NOT_FOUND
    for s in session.exec(select(SetLog).where(SetLog.workout_log_id == log.id)):
        session.delete(s)
    for like in session.exec(select(WorkoutLike).where(WorkoutLike.workout_log_id == log.id)):
        session.delete(like)
    session.flush()
    session.delete(log)
    session.commit()


@router.get("/api/workouts/progress/{exercise_key}", response_model=list[ProgressPoint])
def progress(exercise_key: str, user: CurrentUser, session: SessionDep):
    if exercise_info(session, user, exercise_key) is None:
        raise NOT_FOUND
    rows = session.exec(
        select(WorkoutLog.day, SetLog.weight_kg, SetLog.reps)
        .join(SetLog, col(SetLog.workout_log_id) == col(WorkoutLog.id))
        .where(WorkoutLog.user_id == user.id, SetLog.exercise_key == exercise_key)
        .order_by(col(WorkoutLog.day))
    )
    by_day: dict[date, ProgressPoint] = {}
    for day, weight, reps in rows:
        e1rm = round(weight * (1 + reps / 30), 1)  # Epley formula
        point = by_day.setdefault(
            day, ProgressPoint(day=day, max_weight_kg=weight, best_set_reps=reps, estimated_1rm=e1rm)
        )
        point.max_weight_kg = max(point.max_weight_kg, weight)
        if e1rm > point.estimated_1rm:
            point.estimated_1rm, point.best_set_reps = e1rm, reps
    return list(by_day.values())
