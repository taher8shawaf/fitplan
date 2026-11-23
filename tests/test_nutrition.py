from app.models import ActivityLevel, Goal, Profile, Sex
from app.services.nutrition import bmr, calculate_targets

PROFILE = {"sex": "male", "age": 25, "height_cm": 178, "weight_kg": 80, "activity_level": "moderate", "goal": "cut"}


def test_bmr_mifflin_st_jeor():
    assert bmr(Sex.male, 80, 178, 25) == 10 * 80 + 6.25 * 178 - 5 * 25 + 5
    assert bmr(Sex.female, 60, 165, 30) == 10 * 60 + 6.25 * 165 - 5 * 30 - 161


def test_targets_add_up():
    p = Profile(
        user_id=1,
        sex=Sex.male,
        age=25,
        height_cm=178,
        weight_kg=80,
        activity_level=ActivityLevel.moderate,
        goal=Goal.maintain,
    )
    t = calculate_targets(p)
    assert t.calories == t.tdee
    assert abs(t.protein_g * 4 + t.carbs_g * 4 + t.fat_g * 9 - t.calories) < 15


def test_cut_never_goes_below_floor():
    p = Profile(
        user_id=1,
        sex=Sex.female,
        age=70,
        height_cm=145,
        weight_kg=40,
        activity_level=ActivityLevel.sedentary,
        goal=Goal.cut,
    )
    assert calculate_targets(p).calories >= 1200


def test_profile_endpoint(client, auth):
    assert client.get("/api/profile", headers=auth).status_code == 404
    res = client.put("/api/profile", json=PROFILE, headers=auth)
    assert res.status_code == 200
    body = res.json()
    assert body["targets"]["calories"] < body["targets"]["tdee"]  # deficit for "cut"
    assert body["targets"]["protein_g"] == 160  # 2 g/kg


def test_profile_validation(client, auth):
    assert client.put("/api/profile", json={**PROFILE, "age": 5}, headers=auth).status_code == 422


def test_meal_logging_and_totals(client, auth):
    client.put("/api/profile", json=PROFILE, headers=auth)
    chicken = client.get("/api/foods", params={"q": "chicken breast"}, headers=auth).json()[0]
    res = client.post(
        "/api/meals",
        json={"day": "2026-01-10", "meal_type": "lunch", "food_id": chicken["id"], "grams": 200},
        headers=auth,
    )
    assert res.status_code == 201
    assert res.json()["macros"]["protein"] == 62.0  # 31 g per 100 g

    day = client.get("/api/meals", params={"day": "2026-01-10"}, headers=auth).json()
    assert day["totals"]["calories"] == 330.0
    assert day["remaining"]["calories"] == day["targets"]["calories"] - 330.0
    # other days are unaffected
    assert client.get("/api/meals", params={"day": "2026-01-11"}, headers=auth).json()["entries"] == []


def test_arabic_food_search(client, auth):
    names = [f["name_ar"] for f in client.get("/api/foods", params={"q": "دجاج"}, headers=auth).json()]
    assert "صدر دجاج مشوي" in names


def test_custom_food_is_private(client, auth, other_auth):
    food = {"name_ar": "مندي", "name_en": "Mandi", "calories": 180, "protein": 10, "carbs": 20, "fat": 6}
    created = client.post("/api/foods", json=food, headers=auth).json()
    assert created["is_custom"] is True
    assert client.get("/api/foods", params={"q": "Mandi"}, headers=other_auth).json() == []
    meal = {"day": "2026-01-10", "meal_type": "dinner", "food_id": created["id"], "grams": 100}
    assert client.post("/api/meals", json=meal, headers=other_auth).status_code == 404


def test_custom_food_macros_cannot_exceed_100g(client, auth):
    food = {"name_ar": "x", "name_en": "x", "calories": 500, "protein": 60, "carbs": 60, "fat": 10}
    assert client.post("/api/foods", json=food, headers=auth).status_code == 422


def test_cannot_delete_someone_elses_meal(client, auth, other_auth):
    food_id = client.get("/api/foods", headers=auth).json()[0]["id"]
    entry = client.post(
        "/api/meals", json={"day": "2026-01-10", "meal_type": "snack", "food_id": food_id, "grams": 50}, headers=auth
    ).json()
    assert client.delete(f"/api/meals/{entry['id']}", headers=other_auth).status_code == 404
    assert client.delete(f"/api/meals/{entry['id']}", headers=auth).status_code == 204
