# bank_account/application/dto.py
from pydantic import BaseModel
from typing import Optional, List


class CreateAccountRequest(BaseModel):
    account_type: str  # "CURRENT" ou "SAVINGS"
    overdraft_limit: Optional[float] = 0.0
    deposit_ceiling: Optional[float] = None


class AccountResponse(BaseModel):
    number: str
    balance: float
    account_type: str
    overdraft_limit: float = 0.0
    deposit_ceiling: Optional[float] = None

    class Config:
        from_attributes = True


class OperationResponse(BaseModel):
    date: str
    kind: str
    amount: float
    balance_after: float


class StatementResponse(BaseModel):
    account_number: str
    account_type: str
    balance: float
    operations: List[OperationResponse]
