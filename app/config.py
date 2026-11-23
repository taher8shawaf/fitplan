import os
import warnings

DEFAULT_SECRET = "dev-secret-change-me"


class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./fitplan.db")
    secret_key: str = os.getenv("SECRET_KEY", DEFAULT_SECRET)
    access_token_minutes: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "10080"))  # 7 days
    jwt_algorithm: str = "HS256"


settings = Settings()

if settings.secret_key == DEFAULT_SECRET:
    warnings.warn("SECRET_KEY is not set; using an insecure development key.", stacklevel=1)
