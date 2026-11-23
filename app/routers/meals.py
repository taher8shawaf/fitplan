from datetime import date

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import col, or_, select

from app.deps import CurrentUser, SessionDep
from app.models import Food, MealEntry, Profile
from app.schemas import DayNutritionOut, FoodIn, FoodOut, Macros, MealEntryOut, MealIn
from app.services.nutrition import calculate_targets, macros_for

router = APIRouter(tags=["nutrition"])


def food_out(food: Food) -> FoodOut:
    return FoodOut(**food.model_dump(exclude={"owner_id"}), is_custom=food.owner_id is not None)


def visible_food(session, user, food_id: int) -> Food:
    food = session.get(Food, food_id)
    if not food or (food.owner_id is not None and food.owner_id != user.id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Food not found")
    return food


# ---------- foods ----------
@router.get("/api/foods", response_model=list[FoodOut])
def search_foods(user: CurrentUser, session: SessionDep, q: str = Query("", max_length=50)):
    stmt = select(Food).where(or_(Food.owner_id == None, Food.owner_id == user.id))  # noqa: E711
    if q.strip():
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(or_(col(Food.name_ar).ilike(pattern), col(Food.name_en).ilike(pattern)))
    return [food_out(f) for f in session.exec(stmt.order_by(col(Food.id)).limit(50))]


@router.post("/api/foods", response_model=FoodOut, status_code=status.HTTP_201_CREATED)
def create_food(data: FoodIn, user: CurrentUser, session: SessionDep):
    if data.protein + data.carbs + data.fat > 100:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Macros exceed 100 g per 100 g")
    food = Food(**data.model_dump(), owner_id=user.id)
    session.add(food)
    session.commit()
    session.refresh(food)
    return food_out(food)


# ---------- meals ----------
def entry_out(entry: MealEntry, food: Food) -> MealEntryOut:
    return MealEntryOut(
        id=entry.id,
        day=entry.day,
        meal_type=entry.meal_type,
        food_id=food.id,
        food_ar=food.name_ar,
        food_en=food.name_en,
        grams=entry.grams,
        macros=Macros(**macros_for(food, entry.grams)),
    )


@router.post("/api/meals", response_model=MealEntryOut, status_code=status.HTTP_201_CREATED)
def add_meal(data: MealIn, user: CurrentUser, session: SessionDep):
    food = visible_food(session, user, data.food_id)
    entry = MealEntry(user_id=user.id, **data.model_dump())
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry_out(entry, food)


@router.get("/api/meals", response_model=DayNutritionOut)
def day_nutrition(user: CurrentUser, session: SessionDep, day: date = Query(default_factory=date.today)):
    rows = session.exec(
        select(MealEntry, Food)
        .join(Food, col(Food.id) == col(MealEntry.food_id))
        .where(MealEntry.user_id == user.id, MealEntry.day == day)
        .order_by(col(MealEntry.id))
    ).all()
    entries = [entry_out(e, f) for e, f in rows]

    totals = Macros(
        calories=round(sum(e.macros.calories for e in entries), 1),
        protein=round(sum(e.macros.protein for e in entries), 1),
        carbs=round(sum(e.macros.carbs for e in entries), 1),
        fat=round(sum(e.macros.fat for e in entries), 1),
    )

    targets = remaining = None
    profile = session.get(Profile, user.id)
    if profile:
        t = calculate_targets(profile)
        targets = t.to_dict()
        remaining = Macros(
            calories=round(t.calories - totals.calories, 1),
            protein=round(t.protein_g - totals.protein, 1),
            carbs=round(t.carbs_g - totals.carbs, 1),
            fat=round(t.fat_g - totals.fat, 1),
        )
    return DayNutritionOut(day=day, entries=entries, totals=totals, targets=targets, remaining=remaining)


@router.delete("/api/meals/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(entry_id: int, user: CurrentUser, session: SessionDep):
    entry = session.get(MealEntry, entry_id)
    if not entry or entry.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    session.delete(entry)
    session.commit()
