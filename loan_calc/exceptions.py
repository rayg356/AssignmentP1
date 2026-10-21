class LoanCalcError(Exception):
    """Base exception for loan calculator errors."""


class ValidationError(LoanCalcError):
    """Base exception for invalid user-provided input."""


class PrincipalValidationError(ValidationError):
    """Raised when principal amount is invalid."""


class TenureValidationError(ValidationError):
    """Raised when tenure value is invalid."""


class RateValidationError(ValidationError):
    """Raised when interest rate value is invalid."""


class InstalmentValidationError(ValidationError):
    """Raised when instalment value is invalid."""


class IncomeValidationError(ValidationError):
    """Raised when income/obligation values are invalid."""
