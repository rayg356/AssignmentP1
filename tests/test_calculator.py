import pytest

from loan_calc import (
    amortisation_schedule,
    emi,
    prepayment_savings,
    remaining_tenure,
    total_interest,
    total_payment,
)


def test_emi_assignment_reference_case():
    value = emi(1_000_000, 9, 240)
    assert value == pytest.approx(8997, abs=1)


def test_zero_interest_emi():
    assert emi(120_000, 0, 12) == 10_000.00


def test_one_month_tenure():
    assert emi(50_000, 12, 1) == 50_500.00


def test_very_large_principal_is_finite_and_positive():
    value = emi(100_000_000, 8.5, 360)
    assert value > 0
    assert value < 1_000_000_000


def test_total_payment_and_interest_consistency():
    p = 750_000
    r = 7.25
    n = 180
    assert total_payment(p, r, n) == pytest.approx(emi(p, r, n) * n, abs=0.01)
    assert total_interest(p, r, n) == pytest.approx(total_payment(p, r, n) - p, abs=0.01)


def test_schedule_has_full_tenure_length():
    rows = amortisation_schedule(300_000, 9, 24)
    assert len(rows) == 24


def test_schedule_last_month_matches_tenure_number():
    rows = amortisation_schedule(300_000, 9, 24)
    assert rows[-1]["month"] == 24


def test_prepayment_larger_than_balance_finishes_loan():
    result = prepayment_savings(200_000, 10, 24, prepay_month=23, prepay_amount=500_000)
    assert result["new_tenure"] == 23
    assert result["months_saved"] == 1


def test_remaining_tenure_zero_rate():
    assert remaining_tenure(120_000, 0, 10_000) == 12


def test_remaining_tenure_instalment_too_small_raises():
    with pytest.raises(ValueError):
        remaining_tenure(1_000_000, 12, 100)


def test_invalid_inputs_raise_for_emi():
    with pytest.raises(ValueError):
        emi(0, 10, 120)
    with pytest.raises(ValueError):
        emi(100_000, 10, 0)
