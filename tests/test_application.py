import pytest
from bank_account.application.services import BankService
from bank_account.domain.exceptions import AccountNotFound

def test_create_account():
    service = BankService()
    acc = service.create_account("CURRENT", overdraft_limit=500)
    assert acc.account_type == "CURRENT"
    assert acc.overdraft_limit == 500

def test_deposit_and_withdraw():
    service = BankService()
    acc = service.create_account("CURRENT")
    service.deposit(acc.id, 300)
    assert acc.balance == 300
    service.withdraw(acc.id, 100)
    assert acc.balance == 200

def test_overdraft_logic():
    service = BankService()
    acc = service.create_account("CURRENT", overdraft_limit=100)
    service.withdraw(acc.id, 50)  # balance = -50
    assert acc.balance == -50

def test_statement_generation():
    service = BankService()
    acc = service.create_account("CURRENT")
    service.deposit(acc.id, 100)
    service.withdraw(acc.id, 20)
    statement = service.generate_statement(acc.id)
    assert statement["type"] == "CURRENT"
    assert len(statement["operations"]) == 2

def test_invalid_account_raises_exception():
    service = BankService()
    with pytest.raises(AccountNotFound):
        service.get_account("fake-id")
