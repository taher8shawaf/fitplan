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


# ---------- building a plan by hand ----------
def test_build_custom_plan_from_scratch(client, auth):
    plan = client.post("/api/workouts/plan/custom", json={"days": [{"weekday": 0, "title": "صدر وتراي"}]}, headers=auth)
    assert plan.status_code == 201
    assert plan.json()["split"] == "custom"
    day = plan.json()["days"][0]
    assert day["title_ar"] == day["title_en"] == "صدر وتراي"
    assert day["exercises"] == []

    new_day = client.post("/api/workouts/plan/days", json={"weekday": 2, "title": "Back"}, headers=auth)
    assert new_day.status_code == 201
    # one workout per weekday
    assert client.post("/api/workouts/plan/days", json={"weekday": 2}, headers=auth).status_code == 409

    client.post(f"/api/workouts/plan/days/{day['id']}/exercises", json={"exercise_key": "bench_press"}, headers=auth)
    today = client.get("/api/workouts/today", params={"day": MONDAY}, headers=auth).json()
    assert today["day"]["title_en"] == "صدر وتراي"
    assert [e["exercise_key"] for e in today["day"]["exercises"]] == ["bench_press"]


def test_update_and_delete_day(client, auth):
    plan = client.post("/api/workouts/plan", json={"weekdays": [0, 3]}, headers=auth).json()
    monday, thursday = plan["days"]
    # rename and move Monday to Tuesday
    res = client.patch(
        f"/api/workouts/plan/days/{monday['id']}", json={"weekday": 1, "title": "Heavy upper"}, headers=auth
    )
    assert res.status_code == 200
    assert res.json()["weekday"] == 1 and res.json()["title_en"] == "Heavy upper"
    # can't move onto a weekday that's taken
    assert client.patch(f"/api/workouts/plan/days/{monday['id']}", json={"weekday": 3}, headers=auth).status_code == 409
    # clearing the title falls back to the template name
    res = client.patch(f"/api/workouts/plan/days/{monday['id']}", json={"title": ""}, headers=auth).json()
    assert res["title_en"] == "Full Body A"

    assert client.delete(f"/api/workouts/plan/days/{thursday['id']}", headers=auth).status_code == 204
    assert len(client.get("/api/workouts/plan", headers=auth).json()["days"]) == 1


def test_deleting_day_keeps_workout_history(client, auth):
    plan = client.post("/api/workouts/plan", json={"weekdays": [0, 3]}, headers=auth).json()
    day_id = plan["days"][0]["id"]
    sets = [{"exercise_key": "squat", "set_number": 1, "weight_kg": 80, "reps": 5}]
    client.post("/api/workouts/logs", json={"day": MONDAY, "plan_day_id": day_id, "sets": sets}, headers=auth)
    client.delete(f"/api/workouts/plan/days/{day_id}", headers=auth)
    logs = client.get("/api/workouts/logs", headers=auth).json()
    assert len(logs) == 1 and logs[0]["plan_day_id"] is None


def test_reorder_exercises(client, auth):
    plan = client.post("/api/workouts/plan", json={"weekdays": [0, 3]}, headers=auth).json()
    first, second = plan["days"][0]["exercises"][:2]
    res = client.post(f"/api/workouts/plan/exercises/{second['id']}/move", json={"direction": "up"}, headers=auth)
    order = [e["id"] for e in res.json()["exercises"]]
    assert order[:2] == [second["id"], first["id"]]
    # moving the first one up does nothing
    res = client.post(f"/api/workouts/plan/exercises/{second['id']}/move", json={"direction": "up"}, headers=auth)
    assert [e["id"] for e in res.json()["exercises"]] == order


def test_custom_exercise(client, auth, other_auth):
    created = client.post(
        "/api/exercises", json={"name_ar": "هيب ثرست", "name_en": "Hip Thrust", "muscle": "legs"}, headers=auth
    )
    assert created.status_code == 201
    key = created.json()["key"]
    assert key.startswith("custom_")
    assert any(e["key"] == key for e in client.get("/api/exercises", headers=auth).json())
    assert not any(e["key"] == key for e in client.get("/api/exercises", headers=other_auth).json())

    plan = client.post("/api/workouts/plan/custom", json={"days": [{"weekday": 0}]}, headers=auth).json()
    day_id = plan["days"][0]["id"]
    added = client.post(
        f"/api/workouts/plan/days/{day_id}/exercises", json={"exercise_key": key, "sets": 4, "reps": "10"}, headers=auth
    )
    assert added.status_code == 201 and added.json()["name_en"] == "Hip Thrust"

    sets = [{"exercise_key": key, "set_number": 1, "weight_kg": 100, "reps": 10}]
    assert client.post("/api/workouts/logs", json={"day": MONDAY, "sets": sets}, headers=auth).status_code == 201
    # another user can't use it
    assert client.post("/api/workouts/logs", json={"day": MONDAY, "sets": sets}, headers=other_auth).status_code == 422


def test_custom_exercise_rejects_unknown_muscle(client, auth):
    body = {"name_ar": "س", "name_en": "x", "muscle": "elbows"}
    assert client.post("/api/exercises", json=body, headers=auth).status_code == 422


def test_every_builtin_exercise_has_a_guide():
    from app.services.exercise_guides import GUIDES
    from app.services.workouts import EXERCISES

    body_map = {
        "chest",
        "shoulders",
        "rear_delts",
        "traps",
        "biceps",
        "triceps",
        "forearms",
        "lats",
        "lower_back",
        "abs",
        "glutes",
        "quads",
        "hamstrings",
        "calves",
    }
    assert set(GUIDES) == set(EXERCISES)
    for key, g in GUIDES.items():
        assert len(g["steps_ar"]) == len(g["steps_en"]) >= 3, key
        assert g["tip_ar"] and g["tip_en"], key
        assert set(g["primary"]) | set(g["secondary"]) <= body_map, key


def test_guide_endpoint(client, auth):
    g = client.get("/api/exercises/squat/guide", headers=auth).json()
    assert g["primary"] == ["quads", "glutes"]
    assert g["video_url"].startswith("https://www.youtube.com/results?search_query=Back+Squat")
    assert client.get("/api/exercises/nope/guide", headers=auth).status_code == 404

    key = client.post(
        "/api/exercises", json={"name_ar": "س", "name_en": "Sissy Squat", "muscle": "legs"}, headers=auth
    ).json()["key"]
    custom = client.get(f"/api/exercises/{key}/guide", headers=auth).json()
    assert custom["steps_en"] == [] and custom["primary"] == ["quads", "hamstrings", "glutes"]


def test_every_exercise_group_is_known_and_labelled():
    from pathlib import Path

    from app.services.workouts import EXERCISES, MUSCLES

    js = (Path(__file__).parent.parent / "app/static/app.js").read_text()
    assert {e["muscle"] for e in EXERCISES.values()} <= set(MUSCLES)
    for m in MUSCLES:
        assert js.count(f"m_{m}:") == 2, m  # Arabic and English labels


def test_library_has_the_common_lifts():
    from app.services.workouts import EXERCISES

    for key in (
        "incline_bench_press",
        "db_bench_press",
        "pec_deck",
        "chest_dip",
        "preacher_curl",
        "skull_crusher",
        "rope_pushdown",
        "hip_thrust",
        "hack_squat",
        "t_bar_row",
        "arnold_press",
        "rear_delt_fly",
    ):
        assert key in EXERCISES, key
