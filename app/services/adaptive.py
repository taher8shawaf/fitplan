"""Adaptive TDEE: measure the user's real daily burn from their own data.

Idea: if you ate on average X kcal/day and your weight trend changed by S kg/day,
then your burn is about X - S * 7700 (7700 kcal ≈ 1 kg of body weight).

The weight trend is a least-squares line through the weigh-ins, so single noisy
days (water, salt) matter much less than with a simple first-vs-last comparison.
"""

from datetime import date, timedelta

from app.services.nutrition import KCAL_PER_KG_BODY_WEIGHT

WINDOW_DAYS = 21
MIN_WEIGH_INS = 8
MIN_SPAN_DAYS = 14  # first to last weigh-in
MIN_LOGGED_DAYS = 10
MIN_DAY_KCAL = 800  # days below this look incompletely logged, so they're ignored
MAX_DEVIATION = 0.30  # results more than ±30% from the formula are clamped


def slope_per_day(points: list[tuple[date, float]]) -> float:
    """Least-squares slope (kg per day) of weight over time."""
    origin = points[0][0]
    xs = [(d - origin).days for d, _ in points]
    ys = [w for _, w in points]
    n = len(points)
    mean_x, mean_y = sum(xs) / n, sum(ys) / n
    var_x = sum((x - mean_x) ** 2 for x in xs)
    if var_x == 0:
        return 0.0
    return sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys, strict=True)) / var_x


def estimate(
    weights: list[tuple[date, float]],
    intake_by_day: dict[date, float],
    formula_tdee: float,
    today: date,
) -> dict:
    start = today - timedelta(days=WINDOW_DAYS - 1)
    w = sorted((d, kg) for d, kg in weights if start <= d <= today)
    logged = {d: kcal for d, kcal in intake_by_day.items() if start <= d <= today and kcal >= MIN_DAY_KCAL}
    span = (w[-1][0] - w[0][0]).days if len(w) >= 2 else 0

    result = {
        "window_days": WINDOW_DAYS,
        "weigh_ins": len(w),
        "weigh_ins_needed": MIN_WEIGH_INS,
        "logged_days": len(logged),
        "logged_days_needed": MIN_LOGGED_DAYS,
        "span_days": span,
        "span_days_needed": MIN_SPAN_DAYS,
        "formula_tdee": round(formula_tdee),
    }
    if len(w) < MIN_WEIGH_INS or span < MIN_SPAN_DAYS or len(logged) < MIN_LOGGED_DAYS:
        return {**result, "status": "collecting"}

    slope = slope_per_day(w)
    avg_intake = sum(logged.values()) / len(logged)
    tdee = avg_intake - slope * KCAL_PER_KG_BODY_WEIGHT
    low, high = formula_tdee * (1 - MAX_DEVIATION), formula_tdee * (1 + MAX_DEVIATION)
    tdee = min(max(tdee, low), high)

    return {
        **result,
        "status": "ready",
        "estimated_tdee": round(tdee),
        "avg_intake": round(avg_intake),
        "weekly_change_kg": round(slope * 7, 2),
    }
