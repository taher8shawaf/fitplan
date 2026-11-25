"""Static checks on the frontend, so a missing translation or deleted style can't slip through."""

import re
from pathlib import Path

STATIC = Path(__file__).resolve().parent.parent / "app" / "static"
JS = (STATIC / "app.js").read_text(encoding="utf-8")
CSS = (STATIC / "styles.css").read_text(encoding="utf-8")

# Classes that only act as JS hooks or state flags and have no style of their own.
NO_STYLE_NEEDED = {
    "water",
    "hero",
    "plan-day",
    "meal",
    "sel",
    "on",
    "done",
    "armed",
    "finished",
    "small",
    "lg",
    "block",
    "ghost",
    "ok",
    "reps",
    "mini",
    "x",
    "n",
    "m",
    "info",
    "best",
    "post",
    "card",
    "rest",
    "chart",
    "grid",
    "line",
    "dot",
    "ex",
    "day-weekday",
    "pi-main",
}


def i18n_block(lang: str) -> str:
    start = JS.index(f"  {lang}: {{") + len(f"  {lang}: {{")
    return JS[start : JS.index("\n  },", start)]


def keys(block: str) -> set[str]:
    # a key starts a line or follows ", " and is followed by a string or list value
    return set(re.findall(r'(?:^\s+|,\s+)([A-Za-z_]\w*):\s*["\[]', block, flags=re.M))


def test_arabic_and_english_have_the_same_keys():
    ar, en = keys(i18n_block("ar")), keys(i18n_block("en"))
    assert ar - en == set(), f"missing in English: {sorted(ar - en)}"
    assert en - ar == set(), f"missing in Arabic: {sorted(en - ar)}"


def test_every_translation_key_used_exists():
    defined = keys(i18n_block("ar"))
    used = set(re.findall(r"\bt\(\"([A-Za-z_][A-Za-z0-9_]*)\"\)", JS)) | set(
        re.findall(r"\btf\(\"([A-Za-z_]\w*)\"", JS)
    )
    assert used - defined == set(), f"undefined keys: {sorted(used - defined)}"


def test_no_arabic_indic_digits_in_the_ui():
    assert not re.search(r"[٠-٩]", JS), "use Western digits (0-9) everywhere"


def test_every_static_class_has_a_style():
    used = set()
    for attr in re.findall(r'class="([^"$]*)"', JS):
        used |= set(attr.split())
    missing = {c for c in used - NO_STYLE_NEEDED if not re.search(rf"\.{re.escape(c)}\b", CSS)}
    assert missing == set(), f"classes with no CSS: {sorted(missing)}"


def test_index_links_versioned_assets():
    from fastapi.testclient import TestClient

    from app.main import app

    res = TestClient(app).get("/")
    assert res.status_code == 200
    assert res.headers["cache-control"] == "no-cache"
    assert "/static/app.js?v=" in res.text and "/static/styles.css?v=" in res.text
