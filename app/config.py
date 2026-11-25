import os
import warnings

DEFAULT_SECRET = "dev-secret-change-me"


def normalize_database_url(url: str) -> str:
    """Accept the plain Postgres URL Supabase gives you and use the psycopg 3 driver for it."""
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix) :]
    return url


def default_database_url() -> str:
    # Vercel's filesystem is read-only except /tmp, so a database-less deploy still starts (demo only).
    if os.getenv("VERCEL"):
        return "sqlite:////tmp/fitplan.db"
    return "sqlite:///./fitplan.db"


class Settings:
    database_url: str = normalize_database_url(os.getenv("DATABASE_URL") or default_database_url())
    secret_key: str = os.getenv("SECRET_KEY", DEFAULT_SECRET)
    access_token_minutes: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "10080"))  # 7 days
    jwt_algorithm: str = "HS256"


settings = Settings()

if settings.secret_key == DEFAULT_SECRET:
    warnings.warn("SECRET_KEY is not set; using an insecure development key.", stacklevel=1)
