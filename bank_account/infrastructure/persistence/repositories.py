# bank_account/infrastructure/persistence/repositories.py

from sqlalchemy.orm import Session
from typing import Optional, List
from bank_account.domain.models import BankAccount, Operation
from bank_account.domain.exceptions import AccountNotFound
from bank_account.infrastructure.persistence import orm_models


class AccountRepository:
    """Adapter SQLAlchemy pour accéder aux comptes."""

    def __init__(self, db: Session):
        self.db = db

    # --- Conversion ORM → Domaine ---
    def _to_domain(self, orm: orm_models.AccountORM) -> BankAccount:
        account = BankAccount(
            number=orm.number,
            balance=orm.balance,
            account_type=orm.account_type,
            overdraft_limit=orm.overdraft_limit or 0.0,
            deposit_ceiling=orm.deposit_ceiling,
        )
        # on rattache les opérations
        account.operations = [
            Operation(
                date=op.date,
                kind=op.kind,
                amount=op.amount,
                balance_after=op.balance_after,
            )
            for op in orm.operations
        ]
        return account

    # --- Conversion Domaine → ORM ---
    def _to_orm(
        self,
        account: BankAccount,
        existing: Optional[orm_models.AccountORM] = None,
    ) -> orm_models.AccountORM:
        if existing is None:
            orm = orm_models.AccountORM(
                number=account.number,
                account_type=account.account_type,
                balance=account.balance,
                overdraft_limit=account.overdraft_limit,
                deposit_ceiling=account.deposit_ceiling,
            )
        else:
            orm = existing
            orm.balance = account.balance
            orm.overdraft_limit = account.overdraft_limit
            orm.deposit_ceiling = account.deposit_ceiling

        # reconstruire les opérations
        orm.operations = [
            orm_models.OperationORM(
                date=op.date,
                kind=op.kind,
                amount=op.amount,
                balance_after=op.balance_after,
            )
            for op in account.operations
        ]

        return orm

    # --- Récupérer un compte par numéro ---
    def get_by_number(self, number: str) -> BankAccount:
        orm = (
            self.db.query(orm_models.AccountORM)
            .filter(orm_models.AccountORM.number == number)
            .first()
        )
        if not orm:
            raise AccountNotFound(f"Compte {number} introuvable.")
        return self._to_domain(orm)

    # --- Lister tous les comptes ---
    def list_all(self) -> List[BankAccount]:
        orms = self.db.query(orm_models.AccountORM).all()
        return [self._to_domain(o) for o in orms]

    # --- Sauvegarder / mettre à jour un compte ---
    def save(self, account: BankAccount) -> BankAccount:
        orm = (
            self.db.query(orm_models.AccountORM)
            .filter(orm_models.AccountORM.number == account.number)
            .first()
        )
        orm = self._to_orm(account, existing=orm)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._to_domain(orm)
