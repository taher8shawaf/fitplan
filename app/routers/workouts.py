from datetime import date

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session, col, select

from app.deps import CurrentUser, SessionDep
from app.models import PlanDay, PlanExercise, SetLog, User, WorkoutLog, WorkoutPlan
from app.schemas import (
    ExerciseAddIn,
    ExerciseOut,
    ExerciseUpdateIn,
    GeneratePlanIn,
    PlanDayOut,
    PlanOut,
    ProgressPoint,
    SetIn,
    TodayOut,
    WorkoutLogIn,
    WorkoutLogOut,
)
from app.services.workouts import (
    DAY_TYPES,
    EXERCISES,
    SPLIT_NAMES,
    TEMPLATES,
    choose_split,
    suggest_next_weight,
)

router = APIRouter(tags=["workouts"])
NOT_FOUND = HTTPException(status.HTTP_404_NOT_FOUND, "Not found")


# ---------- helpers ----------
def active_plan(session: Session, user: User) -> WorkoutPlan | None:
    return session.exec(
        select(WorkoutPlan)
        .where(WorkoutPlan.user_id == user.id, WorkoutPlan.is_active == True)  # noqa: E712
        .order_by(col(WorkoutPlan.id).desc())
    ).first()


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
    info = EXERCISES.get(ex.exercise_key, {"ar": ex.exercise_key, "en": ex.exercise_key, "muscle": "other"})
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
    exercises = session.exec(
        select(PlanExercise)
        .where(PlanExercise.plan_day_id == day.id)
        .order_by(col(PlanExercise.position), col(PlanExercise.id))
    )
    titles = DAY_TYPES[day.day_type]
    return PlanDayOut(
        id=day.id,
        weekday=day.weekday,
        day_type=day.day_type,
        title_ar=titles["ar"],
        title_en=titles["en"],
        exercises=[exercise_out(session, user, e, with_history) for e in exercises],
    )


def plan_out(session: Session, user: User, plan: WorkoutPlan) -> PlanOut:
    days = session.exec(select(PlanDay).where(PlanDay.plan_id == plan.id).order_by(col(PlanDay.weekday)))
    return PlanOut(
        id=plan.id,
        split=plan.split,
        split_ar=SPLIT_NAMES[plan.split]["ar"],
        split_en=SPLIT_NAMES[plan.split]["en"],
        days=[day_out(session, user, d) for d in days],
    )


# ---------- exercise library ----------
@router.get("/api/exercises")
def list_exercises():
    return [{"key": k, **v} for k, v in EXERCISES.items()]


# ---------- plan ----------
@router.post("/api/workouts/plan", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
def generate_plan(data: GeneratePlanIn, user: CurrentUser, session: SessionDep):
    # Keep old plans for history, but only one is active.
    for old in session.exec(
        select(WorkoutPlan).where(WorkoutPlan.user_id == user.id, WorkoutPlan.is_active == True)  # noqa: E712
    ):
        old.is_active = False
        session.add(old)

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


@router.get("/api/workouts/plan", response_model=PlanOut)
def get_plan(user: CurrentUser, session: SessionDep):
    plan = active_plan(session, user)
    if not plan:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No active plan")
    return plan_out(session, user, plan)


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
    if data.exercise_key not in EXERCISES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Unknown exercise")
    count = len(list(session.exec(select(PlanExercise.id).where(PlanExercise.plan_day_id == day_id))))
    ex = PlanExercise(plan_day_id=day_id, position=count, **data.model_dump())
    session.add(ex)
    session.commit()
    session.refresh(ex)
    return exercise_out(session, user, ex, with_history=False)


@router.patch("/api/workouts/plan/exercises/{exercise_id}", response_model=ExerciseOut)
def update_exercise(exercise_id: int, data: ExerciseUpdateIn, user: CurrentUser, session: SessionDep):
    ex = owned_exercise(session, user, exercise_id)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(ex, key, value)
    session.add(ex)
    session.commit()
    session.refresh(ex)
    return exercise_out(session, user, ex, with_history=False)


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
    unknown = {s.exercise_key for s in data.sets} - EXERCISES.keys()
    if unknown:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"Unknown exercises: {sorted(unknown)}")

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
    session.delete(log)
    session.commit()


@router.get("/api/workouts/progress/{exercise_key}", response_model=list[ProgressPoint])
def progress(exercise_key: str, user: CurrentUser, session: SessionDep):
    if exercise_key not in EXERCISES:
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
