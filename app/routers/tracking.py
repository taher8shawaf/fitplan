"""Quick add, copying days, saved meals, recipes, water and body weight."""

from datetime import date, timedelta

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session, col, func, select

from app.deps import CurrentUser, SessionDep
from app.models import (
    Food,
    MealEntry,
    Profile,
    Recipe,
    RecipeIngredient,
    SavedMeal,
    SavedMealItem,
    User,
    WaterLog,
    WeightLog,
)
from app.routers.meals import entry_out, food_out, visible_food
from app.schemas import (
    AdaptiveOut,
    CopyMealsIn,
    FoodAmount,
    LogSavedMealIn,
    Macros,
    MealEntryOut,
    QuickAddIn,
    RecipeIn,
    RecipeOut,
    SavedMealIn,
    SavedMealItemOut,
    SavedMealOut,
    WaterIn,
    WaterOut,
    WeightIn,
    WeightOut,
)
from app.services import adaptive
from app.services.nutrition import calculate_targets, calories_for_goal, macros_for

router = APIRouter(tags=["tracking"])
NOT_FOUND = HTTPException(status.HTTP_404_NOT_FOUND, "Not found")


def sum_macros(rows: list[tuple[Food, float]]) -> Macros:
    totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for food, grams in rows:
        for k, v in macros_for(food, grams).items():
            totals[k] += v
    return Macros(**{k: round(v, 1) for k, v in totals.items()})


def item_out(food: Food, grams: float) -> SavedMealItemOut:
    return SavedMealItemOut(food_id=food.id, food_ar=food.name_ar, food_en=food.name_en, grams=grams)


def resolve_items(session: Session, user: User, items: list[FoodAmount]) -> list[tuple[Food, float]]:
    return [(visible_food(session, user, i.food_id), i.grams) for i in items]


# ---------- quick add ----------
@router.post("/api/meals/quick", response_model=MealEntryOut, status_code=status.HTTP_201_CREATED)
def quick_add(data: QuickAddIn, user: CurrentUser, session: SessionDep):
    """Log calories (and optionally macros) directly, e.g. for a restaurant meal.

    Stored as a hidden one-off food of exactly 100 g, so the entry's macros equal the numbers given.
    """
    name = data.name.strip() or None
    food = Food(
        name_ar=name or "إضافة سريعة",
        name_en=name or "Quick add",
        calories=data.calories,
        protein=data.protein,
        carbs=data.carbs,
        fat=data.fat,
        serving_g=100,
        serving_ar="حصة",
        serving_en="portion",
        owner_id=user.id,
        kind="quick",
    )
    session.add(food)
    session.flush()
    entry = MealEntry(user_id=user.id, food_id=food.id, day=data.day, meal_type=data.meal_type, grams=100)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry_out(entry, food)


# ---------- copy a previous day ----------
@router.post("/api/meals/copy", response_model=list[MealEntryOut], status_code=status.HTTP_201_CREATED)
def copy_meals(data: CopyMealsIn, user: CurrentUser, session: SessionDep):
    if data.from_day == data.to_day:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Pick a different day to copy from")
    stmt = select(MealEntry, Food).join(Food, col(Food.id) == col(MealEntry.food_id))
    stmt = stmt.where(MealEntry.user_id == user.id, MealEntry.day == data.from_day)
    if data.meal_type:
        stmt = stmt.where(MealEntry.meal_type == data.meal_type)
    copied = []
    for entry, food in session.exec(stmt.order_by(col(MealEntry.id))).all():
        new = MealEntry(user_id=user.id, food_id=food.id, day=data.to_day, meal_type=entry.meal_type, grams=entry.grams)
        session.add(new)
        copied.append((new, food))
    session.commit()
    for new, _ in copied:
        session.refresh(new)
    return [entry_out(e, f) for e, f in copied]


# ---------- saved meals ----------
def saved_meal_out(session: Session, meal: SavedMeal) -> SavedMealOut:
    rows = session.exec(
        select(SavedMealItem, Food)
        .join(Food, col(Food.id) == col(SavedMealItem.food_id))
        .where(SavedMealItem.saved_meal_id == meal.id)
        .order_by(col(SavedMealItem.id))
    ).all()
    return SavedMealOut(
        id=meal.id,
        name=meal.name,
        items=[item_out(f, i.grams) for i, f in rows],
        totals=sum_macros([(f, i.grams) for i, f in rows]),
    )


def owned_saved_meal(session: Session, user: User, meal_id: int) -> SavedMeal:
    meal = session.get(SavedMeal, meal_id)
    if not meal or meal.user_id != user.id:
        raise NOT_FOUND
    return meal


@router.get("/api/saved-meals", response_model=list[SavedMealOut])
def list_saved_meals(user: CurrentUser, session: SessionDep):
    meals = session.exec(select(SavedMeal).where(SavedMeal.user_id == user.id).order_by(col(SavedMeal.id).desc()))
    return [saved_meal_out(session, m) for m in meals]


@router.post("/api/saved-meals", response_model=SavedMealOut, status_code=status.HTTP_201_CREATED)
def create_saved_meal(data: SavedMealIn, user: CurrentUser, session: SessionDep):
    resolve_items(session, user, data.items)  # checks every food is visible to the user
    meal = SavedMeal(user_id=user.id, name=data.name.strip())
    session.add(meal)
    session.flush()
    for item in data.items:
        session.add(SavedMealItem(saved_meal_id=meal.id, food_id=item.food_id, grams=item.grams))
    session.commit()
    session.refresh(meal)
    return saved_meal_out(session, meal)


@router.post("/api/saved-meals/{meal_id}/log", response_model=list[MealEntryOut], status_code=status.HTTP_201_CREATED)
def log_saved_meal(meal_id: int, data: LogSavedMealIn, user: CurrentUser, session: SessionDep):
    meal = owned_saved_meal(session, user, meal_id)
    items = session.exec(select(SavedMealItem).where(SavedMealItem.saved_meal_id == meal.id)).all()
    created = []
    for item in items:
        food = session.get(Food, item.food_id)
        entry = MealEntry(user_id=user.id, food_id=food.id, day=data.day, meal_type=data.meal_type, grams=item.grams)
        session.add(entry)
        created.append((entry, food))
    session.commit()
    for entry, _ in created:
        session.refresh(entry)
    return [entry_out(e, f) for e, f in created]


@router.delete("/api/saved-meals/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_meal(meal_id: int, user: CurrentUser, session: SessionDep):
    meal = owned_saved_meal(session, user, meal_id)
    for item in session.exec(select(SavedMealItem).where(SavedMealItem.saved_meal_id == meal.id)):
        session.delete(item)
    session.flush()  # children first, so the foreign key is never broken
    session.delete(meal)
    session.commit()


# ---------- recipes ----------
def recipe_out(session: Session, recipe: Recipe) -> RecipeOut:
    food = session.get(Food, recipe.food_id)
    rows = session.exec(
        select(RecipeIngredient, Food)
        .join(Food, col(Food.id) == col(RecipeIngredient.food_id))
        .where(RecipeIngredient.recipe_id == recipe.id)
        .order_by(col(RecipeIngredient.id))
    ).all()
    return RecipeOut(
        id=recipe.id,
        food=food_out(food),
        servings=recipe.servings,
        total_weight_g=recipe.total_weight_g,
        per_serving=Macros(**macros_for(food, recipe.total_weight_g / recipe.servings)),
        ingredients=[
            SavedMealItemOut(food_id=f.id, food_ar=f.name_ar, food_en=f.name_en, grams=i.grams) for i, f in rows
        ],
    )


@router.get("/api/recipes", response_model=list[RecipeOut])
def list_recipes(user: CurrentUser, session: SessionDep):
    recipes = session.exec(select(Recipe).where(Recipe.user_id == user.id).order_by(col(Recipe.id).desc()))
    return [recipe_out(session, r) for r in recipes]


@router.post("/api/recipes", response_model=RecipeOut, status_code=status.HTTP_201_CREATED)
def create_recipe(data: RecipeIn, user: CurrentUser, session: SessionDep):
    """Turn a list of ingredients into one food (per 100 g of the finished dish)."""
    rows = resolve_items(session, user, data.ingredients)
    totals = sum_macros(rows)
    raw_weight = sum(g for _, g in rows)
    # Cooking changes weight (rice absorbs water, meat loses it), so the cooked weight is more accurate if known.
    total_weight = data.cooked_weight_g or raw_weight
    per100 = 100 / total_weight
    serving_g = round(total_weight / data.servings, 1)
    food = Food(
        name_ar=data.name_ar.strip(),
        name_en=data.name_en.strip(),
        calories=round(totals.calories * per100, 1),
        protein=round(totals.protein * per100, 1),
        carbs=round(totals.carbs * per100, 1),
        fat=round(totals.fat * per100, 1),
        serving_g=serving_g,
        serving_ar="حصة",
        serving_en="serving",
        owner_id=user.id,
        kind="recipe",
    )
    session.add(food)
    session.flush()
    recipe = Recipe(user_id=user.id, food_id=food.id, servings=data.servings, total_weight_g=total_weight)
    session.add(recipe)
    session.flush()
    for item in data.ingredients:
        session.add(RecipeIngredient(recipe_id=recipe.id, food_id=item.food_id, grams=item.grams))
    session.commit()
    session.refresh(recipe)
    return recipe_out(session, recipe)


@router.delete("/api/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, user: CurrentUser, session: SessionDep):
    recipe = session.get(Recipe, recipe_id)
    if not recipe or recipe.user_id != user.id:
        raise NOT_FOUND
    for ing in session.exec(select(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe.id)):
        session.delete(ing)
    session.flush()
    food = session.get(Food, recipe.food_id)
    session.delete(recipe)
    session.flush()
    used = session.exec(select(MealEntry.id).where(MealEntry.food_id == food.id)).first() is not None
    saved = session.exec(select(SavedMealItem.id).where(SavedMealItem.food_id == food.id)).first() is not None
    if used or saved:
        food.kind = "food"  # keep it so past logs still show; it becomes a normal custom food
        session.add(food)
    else:
        session.delete(food)
    session.commit()


# ---------- water ----------
def water_goal_ml(profile: Profile | None) -> int:
    """About 35 ml per kg of body weight, rounded to a glass (250 ml)."""
    if not profile:
        return 2500
    goal = round(profile.weight_kg * 35 / 250) * 250
    return int(min(max(goal, 1500), 4500))


@router.get("/api/water", response_model=WaterOut)
def get_water(user: CurrentUser, session: SessionDep, day: date = Query(default_factory=date.today)):
    log = session.get(WaterLog, (user.id, day))
    return WaterOut(day=day, ml=log.ml if log else 0, goal_ml=water_goal_ml(session.get(Profile, user.id)))


@router.post("/api/water", response_model=WaterOut)
def add_water(data: WaterIn, user: CurrentUser, session: SessionDep):
    log = session.get(WaterLog, (user.id, data.day)) or WaterLog(user_id=user.id, day=data.day, ml=0)
    log.ml = max(0, min(log.ml + data.ml, 15000))
    session.add(log)
    session.commit()
    return WaterOut(day=data.day, ml=log.ml, goal_ml=water_goal_ml(session.get(Profile, user.id)))


# ---------- body weight ----------
@router.put("/api/weights", response_model=WeightOut)
def log_weight(data: WeightIn, user: CurrentUser, session: SessionDep):
    """One weigh-in per day (logging again replaces it). The latest weigh-in also updates the profile."""
    entry = session.get(WeightLog, (user.id, data.day)) or WeightLog(user_id=user.id, day=data.day, weight_kg=0)
    entry.weight_kg = round(data.weight_kg, 1)
    session.add(entry)
    latest = session.exec(select(func.max(WeightLog.day)).where(WeightLog.user_id == user.id)).one()
    profile = session.get(Profile, user.id)
    if profile and (latest is None or data.day >= latest):
        profile.weight_kg = entry.weight_kg
        session.add(profile)
    session.commit()
    return WeightOut(day=entry.day, weight_kg=entry.weight_kg)


@router.get("/api/weights", response_model=list[WeightOut])
def list_weights(user: CurrentUser, session: SessionDep, days: int = Query(30, ge=1, le=365)):
    since = date.today() - timedelta(days=days)
    rows = session.exec(
        select(WeightLog).where(WeightLog.user_id == user.id, WeightLog.day >= since).order_by(col(WeightLog.day))
    )
    return [WeightOut(day=w.day, weight_kg=w.weight_kg) for w in rows]


@router.delete("/api/weights/{day}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weight(day: date, user: CurrentUser, session: SessionDep):
    entry = session.get(WeightLog, (user.id, day))
    if entry:
        session.delete(entry)
        session.commit()


# ---------- adaptive TDEE ----------
def require_profile(session: Session, user: User) -> Profile:
    profile = session.get(Profile, user.id)
    if not profile:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profile not set up yet")
    return profile


def daily_intake(session: Session, user: User, since: date) -> dict[date, float]:
    rows = session.exec(
        select(MealEntry, Food)
        .join(Food, col(Food.id) == col(MealEntry.food_id))
        .where(MealEntry.user_id == user.id, MealEntry.day >= since)
    ).all()
    totals: dict[date, float] = {}
    for entry, food in rows:
        totals[entry.day] = totals.get(entry.day, 0) + food.calories * entry.grams / 100
    return totals


@router.get("/api/adaptive", response_model=AdaptiveOut)
def adaptive_tdee(user: CurrentUser, session: SessionDep, today: date = Query(default_factory=date.today)):
    profile = require_profile(session, user)
    since = today - timedelta(days=adaptive.WINDOW_DAYS)
    weights = [(w.day, w.weight_kg) for w in session.exec(select(WeightLog).where(WeightLog.user_id == user.id))]
    formula = calculate_targets(profile).formula_tdee
    result = adaptive.estimate(weights, daily_intake(session, user, since), formula, today)
    if result["status"] == "ready":
        result["suggested_calories"] = round(calories_for_goal(result["estimated_tdee"], profile.goal, profile.sex)[0])
    return AdaptiveOut(**result, applied=profile.tdee_override is not None)


@router.post("/api/adaptive/apply", response_model=AdaptiveOut)
def apply_adaptive(user: CurrentUser, session: SessionDep, today: date = Query(default_factory=date.today)):
    result = adaptive_tdee(user, session, today)
    if result.status != "ready":
        raise HTTPException(status.HTTP_409_CONFLICT, "Not enough data yet")
    profile = require_profile(session, user)
    profile.tdee_override = result.estimated_tdee
    session.add(profile)
    session.commit()
    result.applied = True
    return result


@router.delete("/api/adaptive/apply", status_code=status.HTTP_204_NO_CONTENT)
def reset_adaptive(user: CurrentUser, session: SessionDep):
    profile = require_profile(session, user)
    profile.tdee_override = None
    session.add(profile)
    session.commit()
