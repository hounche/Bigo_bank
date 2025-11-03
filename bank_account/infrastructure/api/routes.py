from fastapi import APIRouter, HTTPException
from application.services import BankService
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
service = BankService()


class AccountCreate(BaseModel):
    type: str
    overdraft_limit: Optional[float] = 0.0
    deposit_cap: Optional[float] = None


class OperationRequest(BaseModel):
    amount: float


@router.post("/accounts")
def create_account(data: AccountCreate):
    try:
        account = service.create_account(
            data.type, data.overdraft_limit or 0.0, data.deposit_cap
        )
        return {"id": account.id, "type": account.account_type, "balance": account.balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/accounts")
def list_accounts():
    return [
        {"id": acc.id, "type": acc.account_type, "balance": acc.balance}
        for acc in service.accounts.values()
    ]


@router.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, op: OperationRequest):
    try:
        acc = service.deposit(account_id, op.amount)
        return {"id": acc.id, "balance": acc.balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, op: OperationRequest):
    try:
        acc = service.withdraw(account_id, op.amount)
        return {"id": acc.id, "balance": acc.balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/accounts/{account_id}/statement")
def statement(account_id: str):
    try:
        return service.generate_statement(account_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/accounts/{account_id}/interest")
def apply_interest(account_id: str):
    """Endpoint pour appliquer les intérêts Livret B"""
    try:
        result = service.apply_interest(account_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
