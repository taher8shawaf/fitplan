import pytest

from app.services.workouts import choose_split, rep_range_top, suggest_next_weight

MONDAY = "2026-01-05"
NEXT_MONDAY = "2026-01-12"
TUESDAY = "2026-01-06"


@pytest.mark.parametrize(
    ("days", "split"),
    [(2, "full_body"), (3, "full_body"), (4, "upper_lower"), (5, "hybrid"), (6, "ppl")],
)
def test_choose_split(days, split):
    name, day_types = choose_split(days)
    assert name == split
    assert len(day_types) == days


def test_rep_range_top():
    assert rep_range_top("8-12") == 12
    assert rep_range_top("5") == 5
    assert rep_range_top("30-45s") is None


def test_progression():
    assert suggest_next_weight("8-12", []) is None
    assert suggest_next_weight("8-12", [(60, 12), (60, 12), (60, 12)]) == 62.5  # hit the top: add weight
    assert suggest_next_weight("8-12", [(60, 12), (60, 10), (60, 9)]) == 60  # not yet: same weight
    assert suggest_next_weight("8-12", [(40, 12), (60, 12)]) == 62.5  # warm-up sets are ignored


def test_generate_plan_and_today(client, auth):
    res = client.post("/api/workouts/plan", json={"weekdays": [3, 0, 5]}, headers=auth)
    assert res.status_code == 201
    plan = res.json()
    assert plan["split"] == "full_body"
    assert [d["weekday"] for d in plan["days"]] == [0, 3, 5]

    today = client.get("/api/workouts/today", params={"day": MONDAY}, headers=auth).json()
    assert today["has_plan"] and not today["is_rest_day"]
    assert today["day"]["day_type"] == "full_a"

    rest = client.get("/api/workouts/today", params={"day": TUESDAY}, headers=auth).json()
    assert rest["has_plan"] and rest["is_rest_day"]


def test_today_without_plan(client, auth):
    res = client.get("/api/workouts/today", params={"day": MONDAY}, headers=auth).json()
    assert res["has_plan"] is False


@pytest.mark.parametrize("weekdays", [[0], [0, 0, 1], [0, 1, 2, 3, 4, 5, 6], [0, 9]])
def test_invalid_weekdays(client, auth, weekdays):
    assert client.post("/api/workouts/plan", json={"weekdays": weekdays}, headers=auth).status_code == 422


def test_new_plan_replaces_old(client, auth):
    client.post("/api/workouts/plan", json={"weekdays": [0, 2]}, headers=auth)
    client.post("/api/workouts/plan", json={"weekdays": [0, 1, 2, 3, 4, 5]}, headers=auth)
    assert client.get("/api/workouts/plan", headers=auth).json()["split"] == "ppl"


def test_log_workout_suggests_next_weight_and_tracks_progress(client, auth):
    plan = client.post("/api/workouts/plan", json={"weekdays": [0, 3]}, headers=auth).json()
    day = plan["days"][0]
    squat = next(e for e in day["exercises"] if e["exercise_key"] == "squat")  # 3 x 6-8

    sets = [{"exercise_key": "squat", "set_number": i, "weight_kg": 100, "reps": 8} for i in (1, 2, 3)]
    res = client.post("/api/workouts/logs", json={"day": MONDAY, "plan_day_id": day["id"], "sets": sets}, headers=auth)
    assert res.status_code == 201

    today = client.get("/api/workouts/today", params={"day": NEXT_MONDAY}, headers=auth).json()
    ex = next(e for e in today["day"]["exercises"] if e["id"] == squat["id"])
    assert ex["suggested_weight_kg"] == 102.5
    assert len(ex["last_sets"]) == 3

    progress = client.get("/api/workouts/progress/squat", headers=auth).json()
    assert progress == [{"day": MONDAY, "max_weight_kg": 100.0, "best_set_reps": 8, "estimated_1rm": 126.7}]


def test_log_rejects_unknown_exercise(client, auth):
    sets = [{"exercise_key": "made_up", "set_number": 1, "weight_kg": 10, "reps": 10}]
    assert client.post("/api/workouts/logs", json={"day": MONDAY, "sets": sets}, headers=auth).status_code == 422


def test_edit_plan_exercises(client, auth):
    plan = client.post("/api/workouts/plan", json={"weekdays": [0, 3]}, headers=auth).json()
    day_id = plan["days"][0]["id"]
    added = client.post(f"/api/workouts/plan/days/{day_id}/exercises", json={"exercise_key": "face_pull"}, headers=auth)
    assert added.status_code == 201
    ex_id = added.json()["id"]
    assert (
        client.patch(f"/api/workouts/plan/exercises/{ex_id}", json={"sets": 4, "reps": "15-20"}, headers=auth).json()[
            "sets"
        ]
        == 4
    )
    assert client.delete(f"/api/workouts/plan/exercises/{ex_id}", headers=auth).status_code == 204


def test_users_cannot_touch_each_others_plans(client, auth, other_auth):
    plan = client.post("/api/workouts/plan", json={"weekdays": [0, 3]}, headers=auth).json()
    day_id = plan["days"][0]["id"]
    ex_id = plan["days"][0]["exercises"][0]["id"]
    assert client.delete(f"/api/workouts/plan/exercises/{ex_id}", headers=other_auth).status_code == 404
    assert (
        client.post(
            f"/api/workouts/plan/days/{day_id}/exercises", json={"exercise_key": "plank"}, headers=other_auth
        ).status_code
        == 404
    )
    sets = [{"exercise_key": "squat", "set_number": 1, "weight_kg": 50, "reps": 5}]
    assert (
        client.post(
            "/api/workouts/logs", json={"day": MONDAY, "plan_day_id": day_id, "sets": sets}, headers=other_auth
        ).status_code
        == 404
    )
