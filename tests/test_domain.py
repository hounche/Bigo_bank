import pytest
from bank_account.domain.models import BankAccount, ACCOUNT_TYPE_CURRENT, ACCOUNT_TYPE_SAVINGS

def test_deposit_increases_balance():
    acc = BankAccount(ACCOUNT_TYPE_CURRENT)
    acc.deposit(200)
    assert acc.balance == 200
    assert len(acc.operations) == 1

def test_withdraw_decreases_balance():
    acc = BankAccount(ACCOUNT_TYPE_CURRENT, balance=500)
    acc.withdraw(300)
    assert acc.balance == 200

def test_withdraw_cannot_exceed_balance_without_overdraft():
    acc = BankAccount(ACCOUNT_TYPE_CURRENT, balance=100)
    with pytest.raises(ValueError):
        acc.withdraw(200)

def test_withdraw_with_overdraft():
    acc = BankAccount(ACCOUNT_TYPE_CURRENT, balance=100, overdraft_limit=150)
    acc.withdraw(200)
    assert acc.balance == -100

def test_savings_cannot_have_overdraft():
    acc = BankAccount(ACCOUNT_TYPE_SAVINGS, balance=100)
    with pytest.raises(ValueError):
        acc.withdraw(200)

def test_savings_respects_deposit_cap():
    acc = BankAccount(ACCOUNT_TYPE_SAVINGS, balance=20000, deposit_cap=22950)
    acc.deposit(2950)
    assert acc.balance == 22950
    with pytest.raises(ValueError):
        acc.deposit(1)
