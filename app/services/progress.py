"""Progress dashboard: weekly weight, lifts, workout adherence and nutrition.

Every function takes plain data (no database), so it is easy to test.
"""

from collections import defaultdict
from datetime import date, timedelta


def week_start(d: date) -> date:
    """Monday of the week that contains `d`."""
    return d - timedelta(days=d.weekday())


def e1rm(weight_kg: float, reps: int) -> float:
    """Estimated one-rep max (Epley)."""
    return weight_kg * (1 + reps / 30)


def weekly_weights(weights: list[tuple[date, float]], today: date, weeks: int = 8) -> list[dict]:
    """Average weigh-in per week, oldest first. Weeks with no weigh-in are left out."""
    first = week_start(today) - timedelta(weeks=weeks - 1)
    buckets: dict[date, list[float]] = defaultdict(list)
    for day, kg in weights:
        if first <= day <= today:
            buckets[week_start(day)].append(kg)
    return [
        {"week_start": ws, "avg_kg": round(sum(v) / len(v), 1), "count": len(v)} for ws, v in sorted(buckets.items())
    ]


def weight_summary(weights: list[tuple[date, float]], today: date) -> dict:
    weeks = weekly_weights(weights, today)
    latest = max(weights, default=None)
    change = round(weeks[-1]["avg_kg"] - weeks[0]["avg_kg"], 1) if len(weeks) >= 2 else None
    return {
        "weeks": weeks,
        "latest_kg": latest[1] if latest else None,
        "latest_day": latest[0] if latest else None,
        "change_kg": change,  # from the first to the latest week shown
        "per_week_kg": round(change / (len(weeks) - 1), 2) if change is not None else None,
    }


def lift_summary(sets: list[tuple[date, str, float, int]], limit: int = 4) -> list[dict]:
    """Best estimated 1RM per exercise: first session vs latest, for the most-trained lifts.

    `sets` holds (day, exercise_key, weight_kg, reps). Sets without weight are ignored.
    """
    best: dict[str, dict[date, float]] = defaultdict(dict)
    for day, key, weight, reps in sets:
        if weight <= 0 or reps <= 0:
            continue
        value = e1rm(weight, reps)
        if value > best[key].get(day, 0):
            best[key][day] = value
    rows = []
    for key, by_day in best.items():
        if len(by_day) < 2:
            continue
        days = sorted(by_day)
        first, latest = by_day[days[0]], by_day[days[-1]]
        rows.append(
            {
                "exercise_key": key,
                "sessions": len(days),
                "first_e1rm": round(first, 1),
                "latest_e1rm": round(latest, 1),
                "change_pct": round((latest - first) / first * 100, 1),
                "since": days[0],
            }
        )
    rows.sort(key=lambda r: (-r["sessions"], r["exercise_key"]))
    return rows[:limit]


def adherence(workout_days: list[date], planned_per_week: int, today: date, weeks: int = 4) -> dict:
    """Workouts done vs planned, per week (this week last). Extra workouts don't count twice."""
    done_by_week: dict[date, set[date]] = defaultdict(set)
    for d in workout_days:
        done_by_week[week_start(d)].add(d)
    this_week = week_start(today)
    rows = []
    for i in range(weeks - 1, -1, -1):
        ws = this_week - timedelta(weeks=i)
        rows.append({"week_start": ws, "done": len(done_by_week.get(ws, ())), "planned": planned_per_week})
    # This week isn't over, so the percentage uses finished weeks only (when there are any).
    finished = rows[:-1]
    planned = sum(r["planned"] for r in finished)
    done = sum(min(r["done"], r["planned"]) for r in finished)
    return {
        "weeks": rows,
        "this_week_done": rows[-1]["done"],
        "planned_per_week": planned_per_week,
        "percent": round(done / planned * 100) if planned else None,
    }


def nutrition_summary(daily: dict[date, tuple[float, float]], today: date, calories: int, protein_min: int) -> dict:
    """Last 7 days of calories and protein against the targets. Only days with food logged count."""
    days = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        kcal, protein = daily.get(d, (0.0, 0.0))
        days.append({"day": d, "calories": round(kcal), "protein": round(protein), "logged": d in daily})
    logged = [x for x in days if x["logged"]]
    n = len(logged)
    return {
        "days": days,
        "logged_days": n,
        "avg_calories": round(sum(x["calories"] for x in logged) / n) if n else None,
        "avg_protein": round(sum(x["protein"] for x in logged) / n) if n else None,
        "calorie_days_on_target": sum(1 for x in logged if abs(x["calories"] - calories) <= calories * 0.1),
        "protein_days_on_target": sum(1 for x in logged if x["protein"] >= protein_min),
    }
