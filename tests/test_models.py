# tests/test_models.py
# ─────────────────────────────────────────
# We're testing that our models are STRUCTURALLY correct —
# that tables can be created, rows can be inserted, and
# relationships navigate correctly — using a temporary
# SQLite database so we NEVER touch real MySQL data during tests.

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Customer, Transaction, RewardPoints, TransactionStatus


# ── Test-only database setup (isolated, in-memory) ──
# SQLite in-memory means this database exists ONLY during
# the test run, in RAM — nothing touches disk or real MySQL

TEST_DB_URL="sqlite:///:memory:"
# Use a temporary SQLite database that exists only in RAM (memory), 
# not as a database file on disk.


test_engine=create_engine(
    TEST_DB_URL ,  connect_args={"check_same_thread": False}
)

# connect_args={"check_same_thread": False}
# means:
# Allow the SQLite connection to be used by different threads.


TestSessionLocal=sessionmaker(bind=test_engine)

@pytest.fixture
def db_session():
    """
    Creates ALL tables fresh before each test function runs,
    yields a session to use, then drops everything after —
    guaranteeing each test starts with a clean, empty database.
    """

    Base.metadata.create_all(bind=test_engine)
    # Base.metadata.create_all(bind=test_engine) knows which tables to 
    # create because your model classes (Customer, Transaction, 
    # RewardPoints) are imported from app.models, and those classes 
    # inherit from the same Base imported from app.database; 
    # when Python loads those classes, SQLAlchemy automatically registers 
    # their table information in Base.metadata, so create_all() simply looks 
    # at that metadata and creates all registered tables in the test 
    # SQLite database.

    session=TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


def test_create_customer(db_session):
    """Confirms a Customer row can be created and saved."""
    customer = Customer(name="Amit", email="amit@axisbank.com", hashed_password="fakehash123")
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)

    # id should be auto-assigned after commit
    assert customer.id is not None
    assert customer.name == "Amit"




def test_customer_transaction_relationship(db_session):
    """
    Confirms the 1-to-many relationship works: creating a
    transaction linked to a customer, then accessing it
    via customer.transactions, returns it correctly.
    """

    customer = Customer(name="Amit", email="amit2@axisbank.com", hashed_password="fakehash123")
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    #db_session.refresh(customer) means "reload the customer Python object 
    # with the latest data from the database." For example, after db_session.
    # commit(), the database may have automatically generated the customer's id, 
    # so refresh(customer) fetches that saved row from SQLite/MySQL and 
    # updates the Python object with the actual database values, such as 
    # customer.id, created_at, etc.

    txn = Transaction(
        customer_id=customer.id,
        amount=500.0,
        merchant="Flipkart",
        status=TransactionStatus.SUCCESS,
    )

    db_session.add(txn)
    db_session.commit()

    # Refresh customer to make sure relationship data is current
    # Reload this Python object from the database.
    db_session.refresh(customer)

    assert len(customer.transactions)==1

def test_customer_reward_points_one_to_one(db_session):
    """
    Confirms the 1-to-1 relationship: creating a RewardPoints
    row linked to a customer, then accessing customer.reward_points
    gives back a SINGLE object (not a list).
    """
    customer = Customer(name="Amit", email="amit3@axisbank.com", hashed_password="fakehash123")
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)

    reward = RewardPoints(customer_id=customer.id, points=100)
    db_session.add(reward)
    db_session.commit()
    db_session.refresh(customer)

    # Should be a SINGLE RewardPoints object, not a list —
    # this confirms uselist=False worked correctly
    assert customer.reward_points is not None
    assert customer.reward_points.points == 100

def test_reward_points_enforces_uniqueness(db_session):
    """
    Confirms the unique=True constraint on customer_id
    actually PREVENTS creating a second RewardPoints row
    for the same customer — enforcing true 1-to-1 at the
    database level, not just in our Python assumptions.
    """
    customer = Customer(name="Amit", email="amit4@axisbank.com", hashed_password="fakehash123")
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)

    reward1 = RewardPoints(customer_id=customer.id, points=50)
    db_session.add(reward1)
    db_session.commit()

    # Attempting a SECOND RewardPoints row for the SAME
    # customer_id should raise an IntegrityError from the DB
    reward2 = RewardPoints(customer_id=customer.id, points=75)
    db_session.add(reward2)

    with pytest.raises(Exception):  # SQLAlchemy raises IntegrityError
        db_session.commit()
    #"I expect db_session.commit() to fail and raise an exception; 
    # if an exception occurs, the test passes."    














