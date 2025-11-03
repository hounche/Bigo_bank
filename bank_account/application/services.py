from datetime import datetime, timedelta
from domain.models import BankAccount, ACCOUNT_TYPE_CURRENT, ACCOUNT_TYPE_SAVINGS, ACCOUNT_TYPE_LIVRET_B
from domain.exceptions import AccountNotFound

class BankService:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_type: str, overdraft_limit: float = 0.0, deposit_cap: float = None):
        """Création d’un compte avec paramètres automatiques selon le type"""
        if account_type == ACCOUNT_TYPE_CURRENT:
            account = BankAccount(account_type, overdraft_limit=overdraft_limit)
        elif account_type == ACCOUNT_TYPE_SAVINGS:
            account = BankAccount(account_type, deposit_cap=22950.0)
        elif account_type == ACCOUNT_TYPE_LIVRET_B:
            account = BankAccount(account_type, deposit_cap=100000.0, interest_rate=0.03)
        else:
            raise ValueError("Type de compte inconnu.")

        self.accounts[account.id] = account
        return account

    def get_account(self, account_id: str) -> BankAccount:
        if account_id not in self.accounts:
            raise AccountNotFound(f"Compte {account_id} introuvable")
        return self.accounts[account_id]

    def deposit(self, account_id: str, amount: float):
        acc = self.get_account(account_id)
        acc.deposit(amount)
        return acc

    def withdraw(self, account_id: str, amount: float):
        acc = self.get_account(account_id)
        acc.withdraw(amount)
        return acc

    def generate_statement(self, account_id: str):
        acc = self.get_account(account_id)
        now = datetime.now()
        one_month_ago = now - timedelta(days=30)
        recent_ops = [op for op in acc.operations if op.date >= one_month_ago]

        return {
            "account_id": acc.id,
            "type": acc.account_type,
            "balance": acc.balance,
            "period": f"{one_month_ago.date()} → {now.date()}",
            "operations": [
                {"type": op.type, "amount": op.amount, "date": op.date.isoformat()}
                for op in sorted(recent_ops, key=lambda o: o.date, reverse=True)
            ],
        }

    def apply_interest(self, account_id: str):
        """Applique les intérêts du Livret B"""
        acc = self.get_account(account_id)
        interest = acc.apply_interest()
        return {"id": acc.id, "added_interest": interest, "balance": acc.balance}
