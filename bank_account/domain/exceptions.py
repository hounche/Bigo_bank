# bank_account/domain/exceptions.py

class DomainError(Exception):
    """Base class for domain errors."""

class InsufficientFunds(DomainError):
    """Raised when trying to withdraw more than allowed."""
    pass

class OverdraftNotAllowed(DomainError):
    """Raised when trying to set overdraft on a saving account."""
    pass

class DepositCeilingExceeded(DomainError):
    """Raised when deposit would exceed account ceiling."""
    pass

class AccountNotFound(DomainError):
    """Raised when account is not found in repository."""
    pass
