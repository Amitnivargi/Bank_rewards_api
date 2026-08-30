# app/models/transaction.py
# ─────────────────────────────────────────
# Defines the "transactions" table. Every Transaction row
# is ONE purchase/payment event linked to a specific customer.

from concurrent.futures._base import PENDING
from sqlalchemy import Column , Integer , Float , String , DateTime , ForeignKey , Enum
from sqlalchemy.orm import relationship
from datetime import datetime , timezone
import enum

from app.database import Base


# A Python Enum restricts `status` to a FIXED set of values —
# MySQL will only accept one of these three strings, anything
# else gets rejected automatically (Module 2 concept, applied)

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class Transaction(Base):
    __tablename__="transactions"

    id=Column(Integer,primary_key=True,index=True)

    # ForeignKey("customers.id") creates the actual DATABASE-LEVEL
    # constraint — MySQL will REJECT inserting a transaction
    # with a customer_id that doesn't exist in the customers table
    customer_id=Column(Integer,ForeignKey("customers.id"), nullable=False, index=True)

    # Float for the transaction amount — good enough for our
    # learning project (production banking systems often use
    # Decimal/Numeric types instead, to avoid floating-point
    # rounding issues with money — worth knowing for interviews!)
    amount=Column(Float, nullable=False)

    # Which merchant the transaction was made at
    merchant=Column(String(150), nullable=False)

    # Uses our TransactionStatus enum above — MySQL column
    # type becomes an ENUM('pending','success','failed')
    status=Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    
    created_at=Column(DateTime, default=lambda:datetime.now(timezone.utc))

    customer=relationship("Customer", back_populates="transactions")





