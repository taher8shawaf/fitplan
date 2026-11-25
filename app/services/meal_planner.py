"""Smart meal planner: builds a day of meals that fits the user's calories and protein.

Works on the built-in foods. Each one gets planning metadata here: what role it plays
in a meal, which meals it suits, a rough price tier, and sensible portion sizes.
Prices vary a lot by country, so the tier is only cheap / medium / pricier.
"""

import random
from collections.abc import Callable
from dataclasses import dataclass

# Share of the day's calories and protein for each meal.
MEAL_SPLIT = {
    "breakfast": (0.25, 0.25),
    "lunch": (0.35, 0.30),
    "dinner": (0.30, 0.30),
    "snack": (0.10, 0.15),
}

# Which roles make up each meal, in the order they're filled. Carbs go last: they fill
# whatever calories are left after protein, vegetables and fat.
MEAL_SHAPE = {
    "breakfast": ("protein", "fruit", "carb"),
    "lunch": ("protein", "veg", "fat", "carb"),
    "dinner": ("protein", "veg", "fat", "carb"),
    "snack": ("protein", "fruit"),
}


@dataclass(frozen=True)
class Meta:
    role: str  # protein, carb, veg, fat, fruit
    meals: frozenset[str]
    tier: int  # 1 cheap, 2 medium, 3 pricier
    min_g: float
    max_g: float
    step_g: float  # portions are rounded to this (e.g. one egg, one pita)


def _m(role: str, meals: str, tier: int, min_g: float, max_g: float, step_g: float) -> Meta:
    names = {"b": "breakfast", "l": "lunch", "d": "dinner", "s": "snack"}
    return Meta(role, frozenset(names[c] for c in meals), tier, min_g, max_g, step_g)


# Keyed by the built-in food's English name (see app/seed.py). Mixed dishes are left out.
FOOD_META: dict[str, Meta] = {
    # protein
    "Grilled chicken breast": _m("protein", "ld", 1, 100, 350, 25),
    "Canned tuna in water": _m("protein", "ld", 1, 60, 240, 60),
    "Whole egg": _m("protein", "bs", 1, 100, 200, 50),
    "Egg white": _m("protein", "b", 1, 99, 198, 33),
    "Foul medames": _m("protein", "b", 1, 150, 300, 50),
    "Lentils, cooked": _m("protein", "ld", 1, 150, 350, 50),
    "Lean ground beef, cooked": _m("protein", "ld", 2, 100, 300, 25),
    "Greek yogurt, low fat": _m("protein", "bs", 2, 170, 510, 85),
    "Cottage cheese": _m("protein", "bs", 2, 100, 300, 50),
    "Whey protein": _m("protein", "bs", 2, 30, 60, 15),
    "Low-fat milk": _m("protein", "bs", 1, 240, 480, 120),
    "Salmon": _m("protein", "ld", 3, 100, 300, 25),
    "Lamb, cooked": _m("protein", "ld", 3, 100, 200, 25),
    # carbs
    "White rice, cooked": _m("carb", "ld", 1, 100, 500, 25),
    "Pasta, cooked": _m("carb", "ld", 1, 100, 500, 25),
    "Potato, boiled": _m("carb", "ld", 1, 150, 600, 50),
    "White pita bread": _m("carb", "bld", 1, 60, 240, 30),
    "Whole wheat pita": _m("carb", "bld", 1, 60, 240, 30),
    "Oats": _m("carb", "b", 1, 30, 150, 10),
    "Sweet potato, boiled": _m("carb", "ld", 2, 150, 600, 50),
    # vegetables
    "Mixed salad (cucumber, tomato)": _m("veg", "ld", 1, 150, 300, 50),
    "Broccoli, cooked": _m("veg", "ld", 2, 100, 200, 50),
    # fat
    "Olive oil": _m("fat", "ld", 2, 5, 20, 5),
    "Hummus": _m("fat", "ld", 1, 50, 100, 25),
    "Avocado": _m("fat", "ld", 3, 50, 100, 50),
    "Peanut butter": _m("fat", "bs", 2, 16, 48, 16),
    "Labneh": _m("fat", "b", 2, 30, 90, 30),
    "Almonds": _m("fat", "s", 3, 14, 42, 14),
    # fruit
    "Banana": _m("fruit", "bs", 1, 118, 118, 118),
    "Apple": _m("fruit", "bs", 1, 182, 182, 182),
    "Dates": _m("fruit", "bs", 2, 48, 96, 24),
}


@dataclass
class PlanFood:
    """The parts of a Food the planner needs (values per 100 g)."""

    id: int
    name_en: str
    calories: float
    protein: float


@dataclass
class Item:
    food: PlanFood
    grams: float
    role: str

    @property
    def kcal(self) -> float:
        return self.food.calories * self.grams / 100

    @property
    def protein(self) -> float:
        return self.food.protein * self.grams / 100


def portion(meta: Meta, grams: float) -> float:
    """Round to the food's natural step and keep it in a sensible range."""
    stepped = round(grams / meta.step_g) * meta.step_g
    return round(min(max(stepped, meta.min_g), meta.max_g), 1)


def candidates(foods: list[PlanFood], role: str, meal: str, budget: int, disliked: set[int]) -> list[PlanFood]:
    """Foods for a role in a meal within budget. If nothing fits the budget, allow any price."""
    fitting = [
        f
        for f in foods
        if f.name_en in FOOD_META
        and FOOD_META[f.name_en].role == role
        and meal in FOOD_META[f.name_en].meals
        and f.id not in disliked
    ]
    within = [f for f in fitting if FOOD_META[f.name_en].tier <= budget]
    return within or fitting


def pick(options: list[PlanFood], liked: set[int], rng: random.Random, avoid: set[int]) -> PlanFood | None:
    fresh = [f for f in options if f.id not in avoid] or options
    if not fresh:
        return None
    # Liked foods win most of the time; the random part gives variety between plans.
    return max(fresh, key=lambda f: (2 if f.id in liked else 0) + rng.random())


def build_meal(
    foods: list[PlanFood],
    meal: str,
    kcal: float,
    protein: float,
    budget: int,
    liked: set[int],
    disliked: set[int],
    rng: random.Random,
    used_proteins: set[int],
) -> list[Item]:
    items: list[Item] = []
    for role in MEAL_SHAPE[meal]:
        food = pick(
            candidates(foods, role, meal, budget, disliked),
            liked,
            rng,
            used_proteins if role == "protein" else set(),
        )
        if food is None:
            continue
        meta = FOOD_META[food.name_en]
        if role == "protein":
            used_proteins.add(food.id)
            grams = protein * 0.85 / food.protein * 100 if food.protein else meta.min_g
        elif role == "carb":
            left = kcal - sum(i.kcal for i in items)
            if left < food.calories * meta.min_g / 100 * 0.6:
                continue  # not enough room for a sensible portion
            grams = left / food.calories * 100
        else:
            grams = meta.min_g
        items.append(Item(food, portion(meta, grams), role))
    return items


def rebalance(
    meals: dict[str, list[Item]],
    kcal_target: float,
    protein_target: float,
    add: Callable[[str], bool],
) -> None:
    """Nudge portions so the day lands near the targets: protein first, then calories.

    When portions hit their limits (very small or very large targets), side items are
    dropped or extra ones added through `add(role)`.
    """

    def all_items() -> list[Item]:
        return [i for items in meals.values() for i in items]

    def of(role: str) -> list[Item]:
        return [i for i in all_items() if i.role == role]

    for _ in range(80):
        items = all_items()
        kcal, protein = sum(i.kcal for i in items), sum(i.protein for i in items)
        protein_dense = lambda i: i.food.protein / max(i.food.calories, 1)  # noqa: E731
        if protein < protein_target * 0.97 and (_step(of("protein"), +1, key=protein_dense) or add("protein")):
            continue
        if kcal > kcal_target * 1.04:
            if _step(of("carb"), -1, key=lambda i: i.kcal):
                continue
            if _step(of("fat"), -1, key=lambda i: i.kcal):
                continue
            if _step(of("protein"), -1, key=lambda i: i.kcal, keep=protein_target):
                continue
            if _drop_extra(meals, kcal - kcal_target * 0.94):
                continue
        elif kcal < kcal_target * 0.96:
            if _step(of("carb"), +1, key=lambda i: -i.kcal) or _step(of("fat"), +1, key=lambda i: -i.kcal):
                continue
            if add("fat") or add("carb") or add("fruit"):
                continue
        break


def _drop_extra(meals: dict[str, list[Item]], room: float) -> bool:
    """When portions can't shrink any more (small calorie targets), leave out one side item."""
    for role in ("fat", "fruit", "carb"):
        options = [(meal, i) for meal, items in meals.items() for i in items if i.role == role and i.kcal <= room]
        if options:
            meal, item = max(options, key=lambda x: x[1].kcal)
            meals[meal].remove(item)
            return True
    return False


def _step(items: list[Item], direction: int, key, keep: float | None = None) -> bool:
    """Move the best-suited item one portion step up or down. Returns False if none can move."""
    for item in sorted(items, key=key, reverse=True):
        meta = FOOD_META[item.food.name_en]
        new = item.grams + direction * meta.step_g
        if not meta.min_g <= new <= meta.max_g:
            continue
        if keep is not None:  # don't cut protein below the target
            others = sum(i.protein for i in items) - item.protein
            if others + item.food.protein * new / 100 < keep:
                continue
        item.grams = round(new, 1)
        return True
    return False


def plan_day(
    foods: list[PlanFood],
    kcal_target: float,
    protein_target: float,
    budget: int = 2,
    liked: set[int] | None = None,
    disliked: set[int] | None = None,
    seed: int = 0,
) -> dict[str, list[Item]]:
    liked, disliked = liked or set(), disliked or set()
    rng = random.Random(seed)
    used: set[int] = set()
    meals = {
        meal: build_meal(
            foods, meal, kcal_target * k_share, protein_target * p_share, budget, liked, disliked, rng, used
        )
        for meal, (k_share, p_share) in MEAL_SPLIT.items()
    }

    def add(role: str) -> bool:
        """Add one more item of `role` to the first meal that can take it."""
        in_plan = {i.food.id for items in meals.values() for i in items}
        for meal in ("snack", "breakfast", "dinner", "lunch"):
            if any(i.role == role for i in meals[meal]) and role != "protein":
                continue
            options = [f for f in candidates(foods, role, meal, budget, disliked) if f.id not in in_plan]
            food = pick(options, liked, rng, set())
            if food:
                meta = FOOD_META[food.name_en]
                meals[meal].append(Item(food, meta.min_g, role))
                return True
        return False

    rebalance(meals, kcal_target, protein_target, add)
    return meals


def alternatives(
    foods: list[PlanFood],
    current: Item,
    meal: str,
    budget: int,
    liked: set[int],
    disliked: set[int],
    limit: int = 4,
) -> list[Item]:
    """Swaps for one item: same role, sized to give the same protein (protein foods) or calories."""
    options = [f for f in candidates(foods, current.role, meal, budget, disliked) if f.id != current.food.id]
    out = []
    for food in options:
        meta = FOOD_META[food.name_en]
        if current.role == "protein" and food.protein:
            grams = current.protein / food.protein * 100
        elif food.calories:
            grams = current.kcal / food.calories * 100
        else:
            continue
        out.append(Item(food, portion(meta, grams), current.role))
    out.sort(key=lambda i: (i.food.id not in liked, abs(i.kcal - current.kcal)))
    return out[:limit]
