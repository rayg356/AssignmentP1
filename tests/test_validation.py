import pytest

from loan_calc.calculator import eligible_amount, emi, prepayment_savings, remaining_tenure
from loan_calc.exceptions import (
    IncomeValidationError,
    InstalmentValidationError,
    PrincipalValidationError,
    RateValidationError,
    TenureValidationError,
)


def test_emi_raises_custom_exception_for_non_positive_principal():
    with pytest.raises(PrincipalValidationError):
        emi(0, 9, 120)


def test_emi_raises_custom_exception_for_non_positive_tenure():
    with pytest.raises(TenureValidationError):
        emi(100000, 9, 0)


def test_emi_raises_custom_exception_for_negative_rate():
    with pytest.raises(RateValidationError):
        emi(100000, -1, 120)


def test_remaining_tenure_raises_for_negative_balance():
    with pytest.raises(PrincipalValidationError):
        remaining_tenure(-100, 9, 5000)


def test_remaining_tenure_raises_for_negative_rate():
    with pytest.raises(RateValidationError):
        remaining_tenure(100000, -9, 5000)


def test_remaining_tenure_raises_for_non_positive_instalment():
    with pytest.raises(InstalmentValidationError):
        remaining_tenure(100000, 9, 0)


def test_prepayment_savings_raises_for_invalid_prepay_month():
    with pytest.raises(TenureValidationError):
        prepayment_savings(100000, 9, 24, prepay_month=0, prepay_amount=1000)

    with pytest.raises(TenureValidationError):
        prepayment_savings(100000, 9, 24, prepay_month=25, prepay_amount=1000)


def test_prepayment_savings_raises_for_negative_prepay_amount():
    with pytest.raises(PrincipalValidationError):
        prepayment_savings(100000, 9, 24, prepay_month=12, prepay_amount=-1)


def test_eligible_amount_raises_for_negative_inputs():
    with pytest.raises(IncomeValidationError):
        eligible_amount(-1, 0, 9, 120)

    with pytest.raises(IncomeValidationError):
        eligible_amount(100000, -1, 9, 120)


def test_eligible_amount_raises_for_invalid_rate_tenure_and_foir():
    with pytest.raises(RateValidationError):
        eligible_amount(100000, 10000, -9, 120)

    with pytest.raises(TenureValidationError):
        eligible_amount(100000, 10000, 9, 0)

    with pytest.raises(IncomeValidationError):
        eligible_amount(100000, 10000, 9, 120, foir=1.5)
