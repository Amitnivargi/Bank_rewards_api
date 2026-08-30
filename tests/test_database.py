# tests/test_database.py
# ─────────────────────────────────────────
# We're testing the DATABASE PLUMBING itself here — not
# any specific table yet (models come in Module 4). We
# want to confirm: can we actually CONNECT to MySQL, and
# does get_db() behave correctly as a generator?

from sqlalchemy import text
from app.database import engine , SessionLocal , get_db

def test_engine_can_connect_to_mysql():
    """
    Confirms the engine can actually open a real connection
    to MySQL using the DATABASE_URL from .env. If this fails,
    it usually means: MySQL isn't running, the database
    doesn't exist yet, or the password in .env is wrong.
    """
    # `connect()` actually opens a connection (not just
    # builds the engine object) — this is the real test


    # with means - Open a database connection, give me that 
    # connection in the variable connection, 
    # and automatically clean it up when I'm done.
    with engine.connect() as connection:
        # Run the simplest possible query just to prove
        # the connection is alive and MySQL responds
        result = connection.execute(text("SELECT 1"))
        # fetchone() gets the single row back: (1,)
        row = result.fetchone()
        assert row[0] == 1


def test_session_local_creates_valid_session():
    """
    Confirms SessionLocal() actually produces a usable
    Session object bound to our engine.
    """
    db = SessionLocal()
    try:
        # A real Session object should have a `.bind`
        # attribute pointing back to our engine
        assert db.bind is engine
    finally:
        # Always clean up manually here since we're not
        # going through get_db()'s generator in this test
        db.close()


def test_get_db_is_a_generator_that_yields_a_session():
    """
    Confirms get_db() behaves as expected: it's a generator
    (uses yield), and calling next() on it gives us back
    a usable Session object — mimicking exactly what
    FastAPI's Depends() system does behind the scenes.
    """
    # get_db() is a generator FUNCTION — calling it doesn't
    # run the code yet, it returns a generator OBJECT
    db_generator = get_db()

    # next() actually STARTS executing the function, runs
    # up to the `yield` line, and gives us that yielded value
    db_session = next(db_generator)

    # Confirm what we got back is a real, usable session
    assert db_session.bind is engine

    # Manually trigger the `finally` block (db.close()) by
    # exhausting the generator — this simulates FastAPI
    # cleaning up after the request completes
    try:
        next(db_generator)
    except StopIteration:
        # This is EXPECTED — the generator has nothing left
        # to yield after cleanup runs, so it raises
        # StopIteration. This confirms cleanup completed.
        pass

# 1st next() → Give me the DB session ✅
# 2nd next() → Finish the function + close DB
#               ↓
#           StopIteration
#               ↓
#         "That's expected" ✅

