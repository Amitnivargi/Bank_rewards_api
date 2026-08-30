# tests/test_migrations.py
# ─────────────────────────────────────────
# We're testing that migrations were actually APPLIED
# correctly to the real database — confirming the tables
# Alembic created match what our models expect.
#
# Note: unlike Module 4's tests (isolated SQLite), THIS
# test intentionally checks your REAL MySQL database,
# since that's literally what this module is about.

from sqlalchemy import inspect
from app.database import engine


def test_all_expected_tables_exist():
    """
    Confirms that after running `alembic upgrade head`,
    all 3 expected tables (plus alembic's own tracking
    table) exist in the real database.
    """
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    assert "customers" in table_names
    assert "transactions" in table_names
    assert "reward_points" in table_names
    # Confirms Alembic's own version-tracking table exists too
    assert "alembic_version" in table_names


def test_customers_table_has_expected_columns():
    """
    Confirms the customers table's actual MySQL columns
    match what we defined in app/models/customer.py.
    """
    inspector = inspect(engine)
    columns = {col["name"] for col in inspector.get_columns("customers")}

    expected_columns = {"id", "name", "email", "hashed_password", "created_at"}
    assert expected_columns.issubset(columns)


def test_transactions_table_has_foreign_key_to_customers():
    """
    Confirms the customer_id column in transactions is
    ACTUALLY registered as a foreign key pointing to
    customers.id at the database level — not just assumed
    in our Python relationship() code.
    """
    inspector = inspect(engine)
    foreign_keys = inspector.get_foreign_keys("transactions")

    # There should be at least one FK, and it should
    # reference the "customers" table
    assert any(fk["referred_table"] == "customers" for fk in foreign_keys)


def test_reward_points_customer_id_is_unique():
    """
    Confirms the unique constraint on reward_points.customer_id
    was actually created in MySQL — enforcing true 1-to-1
    at the database level (not just in Python).
    """
    inspector = inspect(engine)
    unique_constraints = inspector.get_unique_constraints("reward_points")
    indexes = inspector.get_indexes("reward_points")

    # Depending on MySQL/SQLAlchemy version, the uniqueness
    # might show up as a unique constraint OR a unique index —
    # so we check both possibilities
    has_unique_constraint = any(
        "customer_id" in uc["column_names"] for uc in unique_constraints
    )
    has_unique_index = any(
        "customer_id" in idx["column_names"] and idx["unique"]
        for idx in indexes
    )
    assert has_unique_constraint or has_unique_index