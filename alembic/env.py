# alembic/env.py
# ─────────────────────────────────────────
# This is Alembic's "control script" — it tells Alembic
# WHERE to find your database, and WHAT your models look
# like, so it can compare the two and generate migrations.

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ── Import our project's config and models ──
from app.config import settings
from app.database import Base
from app.models import Customer, Transaction, RewardPoints  # noqa: F401

# this is the Alembic Config object, giving access to values
# within the .ini file in use
config = context.config

# ── Override the sqlalchemy.url from alembic.ini with our
#    REAL database URL from settings (Module 2) ──
config.set_main_option("sqlalchemy.url", settings.database_url.replace("%", "%%"))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata is what Alembic compares against the
# real database when you run --autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without a live DB connection (generates raw SQL only)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations WITH a live DB connection (our normal use case)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()