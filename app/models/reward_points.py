# app/models/reward_points.py
# ─────────────────────────────────────────
# Defines the "reward_points" table. Each row is the CURRENT,
# ongoing points balance for exactly ONE customer (1-to-1).

from sqlalchemy import Column , Integer , DateTime , ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime , timezone

from app.database import Base

class RewardPoints(Base):
    __tablename__="reward_points"

    id = Column(Integer, primary_key=True, index=True)

    # unique=True here is CRITICAL — this is what actually
    # ENFORCES the 1-to-1 relationship at the database level.
    # Without unique=True, MySQL would happily allow the SAME
    # customer_id to appear in multiple rows (making it 1-to-many
    # by accident, even though our Python code assumes 1-to-1)
    customer_id=Column(Integer , ForeignKey("customers.id") , unique=True , nullable=False)

    points=Column(Integer, default=0 , nullable=False)

    # Tracks the last time this balance changed — useful for
    # auditing/debugging ("when was this last updated?")

    updated_at=Column(
        DateTime, default=lambda:datetime.now(timezone.utc),
        onupdate=lambda:datetime.now(timezone.utc),
    )

    customer=relationship("Customer",back_populates="reward_points")





