from collections.abc import Generator

from sqlalchemy import event, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.pool import NullPool
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings


def enforce_sqlite_foreign_keys(engine) -> None:
    """SQLite ignores foreign keys unless asked; turn them on so it behaves like Postgres."""

    @event.listens_for(engine, "connect")
    def _on_connect(dbapi_connection, _):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")


def make_engine(url: str):
    if url.startswith("sqlite"):
        engine = create_engine(url, connect_args={"check_same_thread": False})
        enforce_sqlite_foreign_keys(engine)
        return engine
    if uses_transaction_pooler(url):
        # Supabase transaction pooler (port 6543), used from serverless hosts like Vercel:
        # the pooler already pools connections and doesn't support prepared statements.
        return create_engine(url, poolclass=NullPool, connect_args={"prepare_threshold": None})
    # Postgres on a long-running server (session pooler or direct): keep a small pool,
    # checking connections before use since poolers close idle ones.
    return create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=5)


def uses_transaction_pooler(url: str) -> bool:
    return url.startswith("postgresql") and make_url(url).port == 6543


engine = make_engine(settings.database_url)


def init_db() -> None:
    from app import models  # noqa: F401  (register tables)

    SQLModel.metadata.create_all(engine)
    _add_missing_columns()
    if engine.dialect.name == "postgresql":
        _lock_down_supabase_roles()


# Columns added after the first release. create_all() only creates missing tables,
# so older databases get these columns added here. (A bigger project would use Alembic.)
NEW_COLUMNS = {
    "planday": {"title": "VARCHAR"},
    "user": {"username": "VARCHAR", "is_private": "BOOLEAN NOT NULL DEFAULT FALSE"},
    "food": {"kind": "VARCHAR NOT NULL DEFAULT 'food'"},
    "profile": {"tdee_override": "INTEGER"},
}


# Foreign-key columns that got an index later (create_all() doesn't add indexes to existing tables).
NEW_FK_INDEXES = [
    ("mealentry", "food_id"),
    ("recipe", "food_id"),
    ("recipeingredient", "food_id"),
    ("savedmealitem", "food_id"),
    ("workoutlog", "plan_day_id"),
]


def _add_missing_columns() -> None:
    inspector = inspect(engine)
    with engine.begin() as conn:
        for table, columns in NEW_COLUMNS.items():
            existing = {c["name"] for c in inspector.get_columns(table)}
            for name, sql_type in columns.items():
                if name not in existing:
                    conn.execute(text(f'ALTER TABLE "{table}" ADD COLUMN {name} {sql_type}'))
        conn.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ix_user_username ON "user" (username)'))
        for table, column in NEW_FK_INDEXES:
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS ix_{table}_{column} ON {table} ({column})"))
    _backfill_usernames()
    with engine.begin() as conn:  # older versions saved this default with Arabic-Indic digits
        conn.execute(text("UPDATE food SET serving_ar = '100 غ' WHERE serving_ar = '١٠٠ غ'"))


def _backfill_usernames() -> None:
    from sqlmodel import select

    from app.models import User
    from app.services.social import unique_username

    with Session(engine) as session:
        for user in list(session.exec(select(User).where(User.username == None))):  # noqa: E711
            user.username = unique_username(session, user.email.split("@")[0])
            session.add(user)
            session.commit()


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def _lock_down_supabase_roles() -> None:
    """Defense in depth for Supabase.

    The app talks to Postgres directly as the table owner, so it isn't affected by RLS.
    Supabase's public API roles (anon, authenticated) must never read these tables
    (they hold password hashes), so RLS is enabled with no policies and their grants are revoked.
    """
    from app import models  # noqa: F401

    with engine.begin() as conn:
        api_roles = [
            r for (r,) in conn.execute(text("SELECT rolname FROM pg_roles WHERE rolname IN ('anon', 'authenticated')"))
        ]
        for table in SQLModel.metadata.sorted_tables:
            name = f'"{table.name}"'
            conn.execute(text(f"ALTER TABLE {name} ENABLE ROW LEVEL SECURITY"))
            for role in api_roles:
                conn.execute(text(f"REVOKE ALL ON TABLE {name} FROM {role}"))
