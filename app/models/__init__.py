
# app/models/__init__.py
# ─────────────────────────────────────────
# This file makes it easy to import all models from one place:
#     from app.models import Customer, Transaction, RewardPoints
# instead of three separate import lines.
#
# It's ALSO functionally important: SQLAlchemy needs to know
# about ALL model classes before Base.metadata.create_all()
# runs (Module 5) — importing them here ensures they're
# registered with Base as soon as `app.models` is imported
# anywhere in the project.

from app.models.customer import Customer
from app.models.transaction import Transaction, TransactionStatus
from app.models.reward_points import RewardPoints