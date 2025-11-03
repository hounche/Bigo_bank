# bank_account/infrastructure/persistence/orm_models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class AccountORM(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    account_type = Column(String, index=True)
    balance = Column(Float, default=0.0)
    overdraft_limit = Column(Float, default=0.0)
    deposit_ceiling = Column(Float, nullable=True)

    operations = relationship("OperationORM", back_populates="account", cascade="all, delete-orphan")


class OperationORM(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    date = Column(DateTime, default=datetime.utcnow)
    kind = Column(String)
    amount = Column(Float)
    balance_after = Column(Float)

    account = relationship("AccountORM", back_populates="operations")
