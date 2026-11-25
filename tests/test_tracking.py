from datetime import date, timedelta

from app.services.adaptive import estimate, slope_per_day

PROFILE = {"sex": "male", "age": 25, "height_cm": 178, "weight_kg": 80, "activity_level": "moderate", "goal": "cut"}
DAY = "2026-03-10"


def food_id(client, auth, q):
    return client.get("/api/foods", params={"q": q}, headers=auth).json()[0]["id"]


def day_totals(client, auth, day=DAY):
    return client.get("/api/meals", params={"day": day}, headers=auth).json()


# ---------- quick add ----------
def test_quick_add_logs_exact_numbers_and_stays_out_of_search(client, auth):
    body = {"day": DAY, "meal_type": "dinner", "name": "Burger", "calories": 750, "protein": 35, "fat": 40}
    res = client.post("/api/meals/quick", json=body, headers=auth)
    assert res.status_code == 201
    assert res.json()["macros"] == {"calories": 750.0, "protein": 35.0, "carbs": 0.0, "fat": 40.0}
    assert day_totals(client, auth)["totals"]["calories"] == 750
    assert client.get("/api/foods", params={"q": "Burger"}, headers=auth).json() == []
    assert client.get("/api/foods/recent", headers=auth).json() == []


def test_quick_add_needs_calories(client, auth):
    assert (
        client.post(
            "/api/meals/quick", json={"day": DAY, "meal_type": "lunch", "calories": 0}, headers=auth
        ).status_code
        == 422
    )


# ---------- copy ----------
def test_copy_whole_day_or_one_meal(client, auth):
    rice, eggs = food_id(client, auth, "White rice"), food_id(client, auth, "Whole egg")
    client.post("/api/meals", json={"day": DAY, "meal_type": "breakfast", "food_id": eggs, "grams": 100}, headers=auth)
    client.post("/api/meals", json={"day": DAY, "meal_type": "lunch", "food_id": rice, "grams": 200}, headers=auth)

    res = client.post("/api/meals/copy", json={"from_day": DAY, "to_day": "2026-03-11"}, headers=auth)
    assert res.status_code == 201 and len(res.json()) == 2
    assert day_totals(client, auth, "2026-03-11")["totals"] == day_totals(client, auth)["totals"]

    one = client.post(
        "/api/meals/copy", json={"from_day": DAY, "to_day": "2026-03-12", "meal_type": "lunch"}, headers=auth
    ).json()
    assert [e["meal_type"] for e in one] == ["lunch"]
    assert client.post("/api/meals/copy", json={"from_day": DAY, "to_day": DAY}, headers=auth).status_code == 422


def test_copy_only_copies_my_meals(client, auth, other_auth):
    rice = food_id(client, auth, "White rice")
    client.post(
        "/api/meals", json={"day": DAY, "meal_type": "lunch", "food_id": rice, "grams": 200}, headers=other_auth
    )
    assert client.post("/api/meals/copy", json={"from_day": DAY, "to_day": "2026-03-11"}, headers=auth).json() == []


# ---------- saved meals ----------
def test_saved_meal_roundtrip(client, auth, other_auth):
    oats, banana = food_id(client, auth, "Oats"), food_id(client, auth, "Banana")
    body = {"name": "فطوري", "items": [{"food_id": oats, "grams": 40}, {"food_id": banana, "grams": 118}]}
    meal = client.post("/api/saved-meals", json=body, headers=auth).json()
    assert meal["totals"]["calories"] == round(389 * 0.4 + 89 * 1.18, 1)
    assert [m["name"] for m in client.get("/api/saved-meals", headers=auth).json()] == ["فطوري"]

    logged = client.post(
        f"/api/saved-meals/{meal['id']}/log", json={"day": DAY, "meal_type": "breakfast"}, headers=auth
    )
    assert logged.status_code == 201 and len(logged.json()) == 2
    assert day_totals(client, auth)["totals"]["calories"] == meal["totals"]["calories"]

    # private to the owner
    assert client.get("/api/saved-meals", headers=other_auth).json() == []
    assert (
        client.post(
            f"/api/saved-meals/{meal['id']}/log", json={"day": DAY, "meal_type": "lunch"}, headers=other_auth
        ).status_code
        == 404
    )
    assert client.delete(f"/api/saved-meals/{meal['id']}", headers=auth).status_code == 204
    assert client.get("/api/saved-meals", headers=auth).json() == []


def test_saved_meal_cannot_use_someone_elses_food(client, auth, other_auth):
    secret = client.post(
        "/api/foods",
        json={"name_ar": "س", "name_en": "Secret", "calories": 100, "protein": 1, "carbs": 1, "fat": 1},
        headers=other_auth,
    ).json()["id"]
    body = {"name": "x", "items": [{"food_id": secret, "grams": 100}]}
    assert client.post("/api/saved-meals", json=body, headers=auth).status_code == 404


# ---------- recipes ----------
def test_recipe_is_calculated_per_100g_of_cooked_dish(client, auth):
    rice, chicken = food_id(client, auth, "White rice"), food_id(client, auth, "Grilled chicken breast")
    body = {
        "name_ar": "كبسة البيت",
        "name_en": "Home kabsa",
        "servings": 4,
        "ingredients": [{"food_id": rice, "grams": 600}, {"food_id": chicken, "grams": 400}],
        "cooked_weight_g": 1000,
    }
    recipe = client.post("/api/recipes", json=body, headers=auth).json()
    total_kcal = 130 * 6 + 165 * 4  # 1440 kcal in 1000 g
    assert recipe["food"]["calories"] == 144.0
    assert recipe["food"]["kind"] == "recipe" and recipe["food"]["serving_g"] == 250
    assert recipe["per_serving"]["calories"] == total_kcal / 4
    assert len(recipe["ingredients"]) == 2
    # shows up in food search and can be logged like any food
    assert client.get("/api/foods", params={"q": "كبسة البيت"}, headers=auth).json()[0]["kind"] == "recipe"
    meal = {"day": DAY, "meal_type": "lunch", "food_id": recipe["food"]["id"], "grams": 250}
    assert client.post("/api/meals", json=meal, headers=auth).json()["macros"]["calories"] == 360.0


def test_recipe_without_cooked_weight_uses_raw_weight(client, auth):
    rice = food_id(client, auth, "White rice")
    body = {"name_ar": "ر", "name_en": "r", "servings": 2, "ingredients": [{"food_id": rice, "grams": 300}]}
    recipe = client.post("/api/recipes", json=body, headers=auth).json()
    assert recipe["food"]["calories"] == 130 and recipe["total_weight_g"] == 300


def test_deleting_a_used_recipe_keeps_the_logged_food(client, auth):
    rice = food_id(client, auth, "White rice")
    body = {"name_ar": "ر", "name_en": "Rice bowl", "servings": 1, "ingredients": [{"food_id": rice, "grams": 300}]}
    recipe = client.post("/api/recipes", json=body, headers=auth).json()
    client.post(
        "/api/meals",
        json={"day": DAY, "meal_type": "lunch", "food_id": recipe["food"]["id"], "grams": 100},
        headers=auth,
    )
    assert client.delete(f"/api/recipes/{recipe['id']}", headers=auth).status_code == 204
    assert client.get("/api/recipes", headers=auth).json() == []
    assert day_totals(client, auth)["entries"][0]["food_en"] == "Rice bowl"


# ---------- water ----------
def test_water(client, auth):
    assert client.get("/api/water", params={"day": DAY}, headers=auth).json() == {"day": DAY, "ml": 0, "goal_ml": 2500}
    client.put("/api/profile", json=PROFILE, headers=auth)  # 80 kg -> 2750 ml
    client.post("/api/water", json={"day": DAY, "ml": 250}, headers=auth)
    res = client.post("/api/water", json={"day": DAY, "ml": 500}, headers=auth).json()
    assert res == {"day": DAY, "ml": 750, "goal_ml": 2750}
    assert client.post("/api/water", json={"day": DAY, "ml": -5000}, headers=auth).json()["ml"] == 0


# ---------- weight ----------
def test_weight_one_per_day_and_updates_profile(client, auth):
    client.put("/api/profile", json=PROFILE, headers=auth)
    today = date.today()
    client.put("/api/weights", json={"day": str(today), "weight_kg": 81}, headers=auth)
    client.put("/api/weights", json={"day": str(today), "weight_kg": 80.6}, headers=auth)  # replaces
    client.put("/api/weights", json={"day": str(today - timedelta(days=3)), "weight_kg": 82}, headers=auth)
    weights = client.get("/api/weights", headers=auth).json()
    assert [w["weight_kg"] for w in weights] == [82, 80.6]
    # the older entry didn't overwrite the profile's current weight
    assert client.get("/api/profile", headers=auth).json()["weight_kg"] == 80.6


# ---------- adaptive TDEE ----------
def test_slope():
    d0 = date(2026, 1, 1)
    assert slope_per_day([(d0, 80), (d0 + timedelta(days=10), 79)]) == -0.1


def test_estimate_needs_enough_data():
    today = date(2026, 3, 21)
    r = estimate([(today, 80)], {today: 2000}, 2500, today)
    assert r["status"] == "collecting" and r["weigh_ins"] == 1


def test_estimate_finds_real_burn():
    today = date(2026, 3, 21)
    days = [today - timedelta(days=i) for i in range(21)]
    # eating 2000 kcal while losing 0.5 kg/week => burn ≈ 2000 + 0.5 * 7700 / 7 = 2550
    weights = [(d, 80 - 0.5 / 7 * i) for i, d in enumerate(reversed(days)) if i % 2 == 0]  # oldest first
    intake = {d: 2000 for d in days}
    r = estimate(weights, intake, 2400, today)
    assert r["status"] == "ready"
    assert r["estimated_tdee"] == 2550 and r["weekly_change_kg"] == -0.5


def test_estimate_ignores_incomplete_days_and_clamps():
    today = date(2026, 3, 21)
    days = [today - timedelta(days=i) for i in range(21)]
    weights = [(d, 80 - 0.5 * i) for i, d in enumerate(reversed(days))]  # absurd 3.5 kg/week loss
    intake = {d: (300 if i < 5 else 2000) for i, d in enumerate(days)}
    r = estimate(weights, intake, 2400, today)
    assert r["logged_days"] == 16  # the 300 kcal days are ignored
    assert r["estimated_tdee"] == round(2400 * 1.3)  # clamped


def test_adaptive_endpoint_and_apply(client, auth):
    client.put("/api/profile", json=PROFILE, headers=auth)
    assert client.get("/api/adaptive", headers=auth).json()["status"] == "collecting"
    assert client.post("/api/adaptive/apply", headers=auth).status_code == 409

    rice = food_id(client, auth, "White rice")
    today = date.today()
    for i in range(21):
        d = today - timedelta(days=i)
        # 1540 g rice = 2002 kcal per day
        client.post(
            "/api/meals", json={"day": str(d), "meal_type": "lunch", "food_id": rice, "grams": 1540}, headers=auth
        )
        if i % 2 == 0:
            client.put("/api/weights", json={"day": str(d), "weight_kg": round(80 + 0.5 / 7 * i, 2)}, headers=auth)

    result = client.get("/api/adaptive", headers=auth).json()
    assert result["status"] == "ready" and result["weekly_change_kg"] == -0.5
    assert 2500 <= result["estimated_tdee"] <= 2600
    assert result["suggested_calories"] == round(result["estimated_tdee"] * 0.8)

    applied = client.post("/api/adaptive/apply", headers=auth).json()
    assert applied["applied"] is True
    targets = client.get("/api/profile", headers=auth).json()["targets"]
    assert targets["tdee_source"] == "measured" and targets["tdee"] == result["estimated_tdee"]

    assert client.delete("/api/adaptive/apply", headers=auth).status_code == 204
    assert client.get("/api/profile", headers=auth).json()["targets"]["tdee_source"] == "formula"
