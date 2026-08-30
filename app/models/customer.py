# app/models/customer.py
# ─────────────────────────────────────────
# Defines the "customers" table. Every Customer row
# represents one bank customer using the Edge Rewards system.

from sqlalchemy import Column , Integer , String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime , timezone

from app.database import Base

class Customer(Base):
    # __tablename__ tells SQLAlchemy the actual MySQL table
    __tablename__="customers"

    # Primary key column — auto-incrementing integer ID.
    # index=True speeds up lookups by id (common query pattern)
    id = Column(Integer,primary_key=True,index=True)

    # Customer's name — VARCHAR(100) in MySQL.
    # nullable=False means this field is REQUIRED at the DB level
    name=Column(String(100), nullable=False)

    # Email — VARCHAR(150), and unique=True means MySQL itself
    # will REJECT a duplicate email at the database level
    # (an extra safety net beyond just Pydantic validation)
    email=Column(String(150),unique=True,nullable=False,index=True)

    # We NEVER store plain-text passwords (Module 9 concept) —
    # this column holds the HASHED version only
    hashed_password=Column(String(255),nullable=False)

    # Automatically set to the current UTC time when a row
    # is first created — default= runs this function at
    # insert time, not when the class is defined
    created_at=Column(DateTime, default=lambda:datetime.now(timezone.utc))

    # ── RELATIONSHIPS (Python-level convenience, Module 5 concept) ──
    # customer.transactions will give us a LIST of all
    # Transaction objects linked to this customer.
    # back_populates keeps both sides in sync automatically.

    transactions=relationship("Transaction", back_populates="customer")

    # customer.reward_points gives us the ONE linked
    # RewardPoints object (not a list, since it's 1-to-1).
    # uselist=False tells SQLAlchemy "this is a single object,
    # not a collection" — without this, it would default to
    # treating it like a list even for a 1-to-1 relationship.
    reward_points=relationship(
        "RewardPoints" , back_populates="customer", uselist=False
    )

# CUSTOMER
# ┌────┬────────┬─────────────────┬─────────────────┬─────────────────────────┐
# │ id │ name   │ emain           │ hashed_password │ created_at              │
# ├────┼────────┼─────────────────┼─────────────────┼─────────────────────────┤
# │ 1  │ Amit   │ amit@gmail.com  │ $2b$...         │ 2026-08-30 11:45:23     │
# │ 2  │ Rahul  │ rahul@gmail.com │ $2b$...         │ 2026-08-30 12:10:45     │
# └────┴────────┴─────────────────┴─────────────────┴─────────────────────────┘










