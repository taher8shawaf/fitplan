"""Smart meal planner endpoints: preferences, a generated day of meals, and swaps."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import select

from app.deps import CurrentUser, SessionDep
from app.models import Food, MealPlanPrefs, MealType, Profile
from app.routers.meals import food_out
from app.services import meal_planner as mp
from app.services.nutrition import calculate_targets

router = APIRouter(prefix="/api/meal-plan", tags=["meal planner"])


class PrefsIn(BaseModel):
    budget: int = Field(2, ge=1, le=3)
    liked: list[int] = Field(default_factory=list, max_length=60)
    disliked: list[int] = Field(default_factory=list, max_length=60)


class PlanIn(BaseModel):
    seed: int = Field(0, ge=0, le=1_000_000)


class SwapIn(BaseModel):
    food_id: int
    grams: float = Field(gt=0, le=3000)
    meal_type: MealType


def _ids(text: str) -> set[int]:
    return {int(x) for x in text.split(",") if x.isdigit()}


def _prefs(session, user) -> MealPlanPrefs:
    return session.get(MealPlanPrefs, user.id) or MealPlanPrefs(user_id=user.id)


def _prefs_out(p: MealPlanPrefs) -> dict:
    return {"budget": p.budget, "liked": sorted(_ids(p.liked)), "disliked": sorted(_ids(p.disliked))}


def _planner_foods(session) -> dict[int, Food]:
    rows = session.exec(
        select(Food).where(Food.owner_id == None, Food.name_en.in_(list(mp.FOOD_META)))  # noqa: E711
    ).all()
    return {f.id: f for f in rows}


def _plan_food(f: Food) -> mp.PlanFood:
    return mp.PlanFood(id=f.id, name_en=f.name_en, calories=f.calories, protein=f.protein)


def _item_out(item: mp.Item, foods: dict[int, Food]) -> dict:
    return {
        "food": food_out(foods[item.food.id]),
        "grams": item.grams,
        "role": item.role,
        "calories": round(item.kcal),
        "protein": round(item.protein, 1),
    }


@router.get("/prefs")
def get_prefs(user: CurrentUser, session: SessionDep):
    return _prefs_out(_prefs(session, user))


@router.put("/prefs")
def put_prefs(data: PrefsIn, user: CurrentUser, session: SessionDep):
    valid = set(_planner_foods(session))
    liked = set(data.liked) & valid
    disliked = (set(data.disliked) & valid) - liked
    prefs = _prefs(session, user)
    prefs.budget = data.budget
    prefs.liked = ",".join(map(str, sorted(liked)))
    prefs.disliked = ",".join(map(str, sorted(disliked)))
    session.add(prefs)
    session.commit()
    return _prefs_out(prefs)


@router.get("/foods")
def planner_foods(user: CurrentUser, session: SessionDep):
    """Foods the planner can use, with their role and price tier (for the preferences screen)."""
    foods = _planner_foods(session)
    out = []
    for f in sorted(foods.values(), key=lambda f: list(mp.FOOD_META).index(f.name_en)):
        meta = mp.FOOD_META[f.name_en]
        out.append({"food": food_out(f), "role": meta.role, "tier": meta.tier})
    return out


@router.post("")
def generate(data: PlanIn, user: CurrentUser, session: SessionDep):
    profile = session.get(Profile, user.id)
    if not profile:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Set up your profile first")
    targets = calculate_targets(profile)
    prefs = _prefs(session, user)
    foods = _planner_foods(session)
    meals = mp.plan_day(
        [_plan_food(f) for f in foods.values()],
        targets.calories,
        targets.protein_g,
        budget=prefs.budget,
        liked=_ids(prefs.liked),
        disliked=_ids(prefs.disliked),
        seed=data.seed,
    )
    out_meals = []
    for meal, items in meals.items():
        k_share, p_share = mp.MEAL_SPLIT[meal]
        out_meals.append(
            {
                "meal_type": meal,
                "target_calories": round(targets.calories * k_share),
                "target_protein": round(targets.protein_g * p_share),
                "items": [_item_out(i, foods) for i in items],
                "calories": round(sum(i.kcal for i in items)),
                "protein": round(sum(i.protein for i in items)),
            }
        )
    return {
        "seed": data.seed,
        "target_calories": targets.calories,
        "target_protein": targets.protein_g,
        "calories": sum(m["calories"] for m in out_meals),
        "protein": sum(m["protein"] for m in out_meals),
        "meals": out_meals,
    }


@router.post("/alternatives")
def alternatives(data: SwapIn, user: CurrentUser, session: SessionDep):
    foods = _planner_foods(session)
    food = foods.get(data.food_id)
    if food is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not a planner food")
    prefs = _prefs(session, user)
    current = mp.Item(_plan_food(food), data.grams, mp.FOOD_META[food.name_en].role)
    swaps = mp.alternatives(
        [_plan_food(f) for f in foods.values()],
        current,
        data.meal_type.value,
        prefs.budget,
        _ids(prefs.liked),
        _ids(prefs.disliked),
    )
    return [_item_out(i, foods) for i in swaps]
