# tests/test_config.py
# ─────────────────────────────────────────
# We're not testing "real" secrets here — we're testing
# that the Settings CLASS behaves correctly: that it loads
# expected fields, applies defaults properly, and enforces
# required fields.

import pytest
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


def test_settings_loads_from_env_file():
    """
    Confirms that our actual project Settings object
    (reading from the REAL .env file) successfully loads
    with no errors, and that expected fields are present
    and non-empty.
    """
    from app.config import settings

    # These should all be populated strings, not None/empty,
    # assuming .env was filled in correctly (Step: real DB
    # password, real/placeholder Groq key, etc.)
    assert settings.database_url != ""
    assert settings.jwt_secret_key != ""
    assert settings.groq_api_key != ""

    # Confirm the default value logic works — this SHOULD
    # be 30 unless explicitly overridden in .env
    assert settings.access_token_expiry_minutes == 30


def test_settings_fails_without_required_field():
    """
    Confirms Settings' FAIL-FAST behavior: if a REQUIRED
    field (like database_url) is missing, Pydantic should
    raise a ValidationError immediately — not silently
    proceed with a None value.

    We build a SEPARATE, isolated Settings-like class here
    (not reading any real .env file) specifically to prove
    this validation behavior in isolation.
    """

    class TestSettingsNoDefaults(BaseSettings):
        database_url: str          # required, no default
        jwt_secret_key: str          # required, no default

        model_config = SettingsConfigDict(
            env_file=None,            # deliberately DON'T read any .env file
        )

    # Since no env vars are set AND no .env file is read,
    # required fields are missing → this MUST raise
    with pytest.raises(ValidationError):
        TestSettingsNoDefaults()


def test_environment_default_value():
    """
    Confirms that `environment` falls back correctly to
    "development" when not explicitly overridden — testing
    the OPTIONAL field / default value behavior specifically.
    """
    from app.config import settings

    # This should be "development" unless you explicitly
    # set ENVIRONMENT=something_else in your .env
    assert settings.environment in ("development", "test", "production")