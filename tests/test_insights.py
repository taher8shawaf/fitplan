"""Progress dashboard and meal planner."""

from datetime import date, timedelta

from app.seed import FOODS
from app.services import meal_planner as mp
from app.services import progress

PROFILE = {"sex": "male", "age": 25, "height_cm": 178, "weight_kg": 80, "activity_level": "moderate", "goal": "cut"}
TODAY = date(2026, 11, 25)  # a Wednesday


# ---------------------------------------------------------------- progress (pure)
def test_weekly_weights_average_each_week():
    weights = [(TODAY - timedelta(days=d), 80 - d * 0.05) for d in range(0, 30, 2)]
    weeks = progress.weekly_weights(weights, TODAY)
    assert all(w["week_start"].weekday() == 0 for w in weeks)
    assert weeks[-1]["week_start"] == date(2026, 11, 23)
    summary = progress.weight_summary(weights, TODAY)
    assert summary["latest_kg"] == 80
    assert summary["change_kg"] > 0  # weights were lower in the past


def test_lift_summary_compares_first_and_latest_session():
    sets = [
        (date(2026, 10, 1), "squat", 100, 5),
        (date(2026, 10, 1), "squat", 90, 8),
        (date(2026, 11, 1), "squat", 110, 5),
        (date(2026, 11, 1), "bench_press", 80, 5),  # only one session: left out
    ]
    rows = progress.lift_summary(sets)
    assert [r["exercise_key"] for r in rows] == ["squat"]
    assert rows[0]["first_e1rm"] == round(100 * (1 + 5 / 30), 1)
    assert rows[0]["change_pct"] == 10.0


def test_adherence_counts_finished_weeks_and_caps_extra_workouts():
    monday = date(2026, 11, 23)
    days = [monday - timedelta(weeks=1) + timedelta(days=i) for i in range(5)]  # 5 workouts, 3 planned
    days += [monday - timedelta(weeks=2)]  # 1 of 3
    days += [monday]  # this week so far
    result = progress.adherence(days, 3, TODAY)
    assert [w["done"] for w in result["weeks"]] == [0, 1, 5, 1]
    assert result["this_week_done"] == 1
    assert result["percent"] == round((0 + 1 + 3) / 9 * 100)


def test_nutrition_summary_only_counts_logged_days():
    daily = {TODAY: (2000, 150), TODAY - timedelta(days=1): (2600, 100)}
    s = progress.nutrition_summary(daily, TODAY, calories=2100, protein_min=130)
    assert len(s["days"]) == 7 and s["logged_days"] == 2
    assert s["avg_calories"] == 2300
    assert s["calorie_days_on_target"] == 1
    assert s["protein_days_on_target"] == 1


# ---------------------------------------------------------------- progress (API)
def test_progress_endpoint(client, auth):
    client.put("/api/profile", json=PROFILE, headers=auth)
    client.post("/api/workouts/plan", json={"weekdays": [0, 2, 4]}, headers=auth)
    for d, kg in [(TODAY - timedelta(days=14), 81), (TODAY, 80)]:
        client.put("/api/weights", json={"day": str(d), "weight_kg": kg}, headers=auth)
    plan = client.get("/api/workouts/plan", headers=auth).json()
    day = plan["days"][0]
    key = day["exercises"][0]["exercise_key"]
    for d, w in [(TODAY - timedelta(days=7), 60), (TODAY, 65)]:
        body = {
            "day": str(d),
            "plan_day_id": day["id"],
            "sets": [{"exercise_key": key, "set_number": 1, "weight_kg": w, "reps": 8}],
        }
        assert client.post("/api/workouts/logs", json=body, headers=auth).status_code == 201
    food = client.get("/api/foods", headers=auth).json()[0]
    client.post(
        "/api/meals", json={"day": str(TODAY), "meal_type": "lunch", "food_id": food["id"], "grams": 200}, headers=auth
    )

    res = client.get(f"/api/progress?today={TODAY}", headers=auth)
    assert res.status_code == 200
    p = res.json()
    assert p["weight"]["latest_kg"] == 80 and p["weight"]["change_kg"] == -1
    assert p["lifts"][0]["exercise_key"] == key and p["lifts"][0]["change_pct"] > 0
    assert p["adherence"]["planned_per_week"] == 3 and p["adherence"]["this_week_done"] == 1
    assert p["nutrition"]["logged_days"] == 1 and p["nutrition"]["target_calories"] > 0


def test_progress_works_for_a_brand_new_user(client, auth):
    p = client.get("/api/progress", headers=auth).json()
    assert p["weight"]["weeks"] == [] and p["lifts"] == []
    assert p["adherence"]["percent"] is None and p["nutrition"]["avg_calories"] is None


# ---------------------------------------------------------------- meal planner (pure)
FOODS_FOR_PLAN = [mp.PlanFood(i, f[1], f[2], f[3]) for i, f in enumerate(FOODS)]


def _totals(meals):
    items = [i for its in meals.values() for i in its]
    return sum(i.kcal for i in items), sum(i.protein for i in items)


def test_every_planner_food_exists_in_the_seed():
    names = {f[1] for f in FOODS}
    assert set(mp.FOOD_META) <= names


def test_plan_lands_near_targets_for_different_people():
    for kcal, protein, budget in [(2400, 170, 2), (1800, 140, 1), (3000, 150, 3), (1500, 120, 1)]:
        for seed in range(5):
            meals = mp.plan_day(FOODS_FOR_PLAN, kcal, protein, budget=budget, seed=seed)
            total_kcal, total_protein = _totals(meals)
            assert abs(total_kcal - kcal) <= kcal * 0.08, (kcal, seed, total_kcal)
            assert total_protein >= protein * 0.95, (protein, seed, total_protein)
            assert all(meals[m] for m in mp.MEAL_SPLIT)


def test_plan_respects_budget_and_dislikes():
    chicken = next(f.id for f in FOODS_FOR_PLAN if f.name_en == "Grilled chicken breast")
    for seed in range(8):
        meals = mp.plan_day(FOODS_FOR_PLAN, 2200, 150, budget=1, disliked={chicken}, seed=seed)
        for items in meals.values():
            for i in items:
                assert mp.FOOD_META[i.food.name_en].tier == 1
                assert i.food.id != chicken


def test_liked_foods_show_up():
    salmon = next(f.id for f in FOODS_FOR_PLAN if f.name_en == "Salmon")
    meals = mp.plan_day(FOODS_FOR_PLAN, 2400, 160, budget=3, liked={salmon}, seed=1)
    assert salmon in {i.food.id for its in meals.values() for i in its}


def test_portions_follow_natural_steps():
    meals = mp.plan_day(FOODS_FOR_PLAN, 2400, 170, seed=2)
    for items in meals.values():
        for i in items:
            meta = mp.FOOD_META[i.food.name_en]
            assert meta.min_g <= i.grams <= meta.max_g
            assert abs(i.grams / meta.step_g - round(i.grams / meta.step_g)) < 1e-6


def test_alternatives_keep_the_role_and_protein():
    chicken = next(f for f in FOODS_FOR_PLAN if f.name_en == "Grilled chicken breast")
    item = mp.Item(chicken, 200, "protein")
    swaps = mp.alternatives(FOODS_FOR_PLAN, item, "lunch", 3, set(), set())
    assert swaps and all(s.role == "protein" and s.food.id != chicken.id for s in swaps)
    assert all(mp.FOOD_META[s.food.name_en].role == "protein" for s in swaps)


# ---------------------------------------------------------------- meal planner (API)
def test_meal_plan_needs_a_profile(client, auth):
    assert client.post("/api/meal-plan", json={}, headers=auth).status_code == 400


def test_meal_plan_endpoints(client, auth):
    client.put("/api/profile", json=PROFILE, headers=auth)
    foods = client.get("/api/meal-plan/foods", headers=auth).json()
    assert len(foods) == len(mp.FOOD_META)
    tuna = next(f["food"]["id"] for f in foods if f["food"]["name_en"] == "Canned tuna in water")

    prefs = client.put(
        "/api/meal-plan/prefs", json={"budget": 1, "liked": [tuna], "disliked": [tuna, 999999]}, headers=auth
    )
    assert prefs.json() == {"budget": 1, "liked": [tuna], "disliked": []}  # liked wins, unknown ids dropped

    plan = client.post("/api/meal-plan", json={"seed": 3}, headers=auth).json()
    assert [m["meal_type"] for m in plan["meals"]] == ["breakfast", "lunch", "dinner", "snack"]
    assert abs(plan["calories"] - plan["target_calories"]) <= plan["target_calories"] * 0.08
    assert all(m["protein"] > 0 for m in plan["meals"])

    item = plan["meals"][1]["items"][0]
    swaps = client.post(
        "/api/meal-plan/alternatives",
        json={"food_id": item["food"]["id"], "grams": item["grams"], "meal_type": "lunch"},
        headers=auth,
    ).json()
    assert swaps and all(s["role"] == item["role"] for s in swaps)

    # the plan can be logged with the existing batch endpoint
    meal = plan["meals"][0]
    body = {
        "day": str(TODAY),
        "meal_type": "breakfast",
        "items": [{"food_id": i["food"]["id"], "grams": i["grams"]} for i in meal["items"]],
    }
    assert client.post("/api/meals/batch", json=body, headers=auth).status_code == 201


def test_prefs_are_per_user(client, auth, other_auth):
    client.put("/api/meal-plan/prefs", json={"budget": 3}, headers=auth)
    assert client.get("/api/meal-plan/prefs", headers=other_auth).json()["budget"] == 2
