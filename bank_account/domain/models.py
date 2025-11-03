from datetime import datetime
import uuid
from typing import List, Optional

ACCOUNT_TYPE_CURRENT = "CURRENT"
ACCOUNT_TYPE_SAVINGS = "SAVINGS"
ACCOUNT_TYPE_LIVRET_B = "LIVRET_B"  #nouveau type

class Operation:
    def __init__(self, type: str, amount: float, date: Optional[datetime] = None):
        self.type = type
        self.amount = amount
        self.date = date or datetime.now()

class BankAccount:
    def __init__(
        self,
        account_type: str,
        balance: float = 0.0,
        overdraft_limit: float = 0.0,
        deposit_cap: Optional[float] = None,
        interest_rate: Optional[float] = None,
    ):
        self.id = str(uuid.uuid4())
        self.account_type = account_type
        self.balance = balance
        self.overdraft_limit = overdraft_limit
        self.deposit_cap = deposit_cap
        self.interest_rate = interest_rate
        self.operations: List[Operation] = []

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Le montant du dépôt doit être positif.")

        if self.deposit_cap is not None and self.balance + amount > self.deposit_cap:
            raise ValueError("Dépôt refusé : plafond du compte atteint.")

        self.balance += amount
        self.operations.append(Operation("DEPOSIT", amount))

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Le montant du retrait doit être positif.")

        available = self.balance
        if self.account_type == ACCOUNT_TYPE_CURRENT:
            available += self.overdraft_limit

        if amount > available:
            raise ValueError("Fonds insuffisants pour ce retrait.")

        self.balance -= amount
        self.operations.append(Operation("WITHDRAW", -amount))

    def apply_interest(self):
        """Calcul automatique des intérêts pour Livret B"""
        if self.account_type == ACCOUNT_TYPE_LIVRET_B and self.interest_rate:
            interest = round(self.balance * self.interest_rate / 12, 2)
            if interest > 0:
                self.balance += interest
                self.operations.append(Operation("INTEREST", interest))
            return interest
        return 0.0
