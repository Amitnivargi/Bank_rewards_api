
# app/config.py
# ─────────────────────────────────────────
# Defines a typed, validated Settings object that reads
# from the .env file. Every other module in this project
# will import `settings` from here instead of reading
# os.environ directly — this keeps config access consistent
# and gives us validation "for free."

# BaseSettings is Pydantic's special model class that knows
# how to read values from environment variables / .env files

from pydantic_settings import BaseSettings , SettingsConfigDict

class Setting(BaseSettings):
    """
    Each attribute below corresponds to one environment
    variable. Pydantic matches names case-insensitively —
    e.g., `database_url` here matches DATABASE_URL in .env.
    """

    # Type hint `str` means this value is REQUIRED —
    # if DATABASE_URL is missing from .env, the app
    # will refuse to start (fail-fast behavior)
    database_url:str

    # JWT secret — also required, no default value
    jwt_secret_key:str

    # This one HAS a default (30) — so it's OPTIONAL in .env.
    # If not set, it silently falls back to 30.
    access_token_expiry_minutes:int=30

    # Groq API key — required for LLM-calling modules later

    groq_api_key:str

    # Environment name — has a default, so it's optional
    environment: str = "development"

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings=Setting()







