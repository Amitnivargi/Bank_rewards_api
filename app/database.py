# app/database.py
# ─────────────────────────────────────────
# This module sets up the THREE core SQLAlchemy building
# blocks: engine, session factory, and Base (for models).
# It also defines get_db() — the dependency every endpoint
# will use to safely access the database.

from sqlalchemy import create_engine
# create_engine → Connects your application to the database
# It creates the database engine, which knows where and how to 
# connect to your database.


from sqlalchemy.orm import sessionmaker , declarative_base
# sessionmaker → creates database sessions
# → Creates sessions for doing database work
# A Session is used to communicate with the database — 
# query, insert, update, delete data.

# declarative_base → creates base class for your models
# You use it to create a base class from which your database models inherit.

from app.config import settings
# Import our validated settings object from Module 2 —
# NOT reading environment variables directly here, we
# trust config.py already validated everything at startup

# 1. ENGINE — manages the actual connection pool to MySQL

engine = create_engine(
    settings.database_url,   # the mysql+pymysql://... string from .env

    # pool_pre_ping: before handing out a connection from
    # the pool, SQLAlchemy sends a tiny "are you alive?"
    # check first. This prevents the classic "MySQL server
    # has gone away" error caused by MySQL silently closing
    # idle connections after a timeout period.
    pool_pre_ping=True,

    # echo=False means SQLAlchemy won't print every SQL
    # statement to the console. Set this to True TEMPORARILY
    # if you ever want to debug exactly what SQL is being run.
    echo=False,
)

# 2. SESSION FACTORY — a template for creating new Sessions
# sessionmaker → creates database sessions
# → Creates sessions for doing database work
# A Session is used to communicate with the database — 
# query, insert, update, delete data.

SessionLocal = sessionmaker(
    autocommit=False,  # we explicitly call .commit() ourselves —
                         # nothing saves automatically, which
                         # gives us full control over WHEN
                         # changes actually hit the database

    autoflush=False,     # don't auto-sync pending changes to
                           # the DB before every query — again,
                           # WE control exactly when that happens

    bind=engine,           # ties every Session this factory
                             # creates to OUR engine above
)

Base= declarative_base()
# declarative_base → creates base class for your models
# You use it to create a base class from which your database models inherit.

def get_db():
    """
    Creates a NEW database session for a single request,
    hands it to the endpoint via `yield`, and guarantees
    it's closed afterward — even if the endpoint raises
    an exception.
    """
    # Create a fresh session for THIS request only
    db = SessionLocal()
    try:
        # Pause here and hand the session to whichever
        # endpoint declared: db: Session = Depends(get_db)
        yield db
    finally:
        # This runs AFTER the endpoint finishes (success
        # OR failure) — guarantees we never leak an open
        # connection back to the pool
        db.close()  








 