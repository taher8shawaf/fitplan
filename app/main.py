import hashlib
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session

from app.database import engine, init_db
from app.routers import auth, meal_planner, meals, profile, progress, social, tracking, workouts
from app.seed import seed_foods

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    with Session(engine) as session:
        seed_foods(session)
    yield


app = FastAPI(
    title="FitPlan API",
    description="Gym workout scheduling and meal tracking / تنظيم التمارين والأكل",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(workouts.router)
app.include_router(meals.router)
app.include_router(social.router)
app.include_router(tracking.router)
app.include_router(progress.router)
app.include_router(meal_planner.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def _versioned_index() -> str:
    """index.html with ?v=<content hash> on the CSS and JS links.

    Browsers (phones especially) can keep old copies of these files; a new hash on every
    change makes them fetch the new version, so everyone sees an update right away.
    """
    html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    for name in ("styles.css", "app.js"):
        digest = hashlib.sha256((STATIC_DIR / name).read_bytes()).hexdigest()[:10]
        html = html.replace(f"/static/{name}", f"/static/{name}?v={digest}")
    return html


INDEX_HTML = _versioned_index()


@app.get("/", include_in_schema=False)
def index():
    # no-cache: the page itself is always re-checked, so it always points at the newest files
    return HTMLResponse(INDEX_HTML, headers={"Cache-Control": "no-cache"})
