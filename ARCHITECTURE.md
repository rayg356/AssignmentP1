# loan-calc Architecture Notes

This document explains what each part of the project does, based on the current codebase.

## Project structure

- `loan_calc/calculator.py`: core loan formulas and helpers.
- `loan_calc/__init__.py`: re-exports public functions from `calculator.py`.
- `cli.py`: command-line interface for quick manual calculations.
- `README.md`: setup and usage instructions.
- `tests/`: currently empty starter test folder.

### Constants

- `DEFAULT_CURRENCY = "INR"`
  - Declares the default currency code used by summary output.

### Helper function

- `_monthly_rate(annual_rate)`
  - Converts annual percentage rate into monthly decimal rate.
  - Current implementation does: `round(annual_rate / 1200, 4)`.
  - Example: 9% annual becomes `0.0075`.

### Core EMI and totals

- `emi(principal, annual_rate, tenure_months)`
  - Calculates monthly instalment.
  - Validates:
    - `tenure_months > 0`
    - `principal > 0`
  - If monthly rate is zero, uses simple division: `principal / tenure_months`.
  - Otherwise uses standard amortized-loan EMI formula:
    - `EMI = P * r * (1+r)^n / ((1+r)^n - 1)`
  - Returns rounded value to 2 decimals.

- `total_payment(principal, annual_rate, tenure_months)`
  - Computes total amount repaid over tenure:
    - `emi(...) * tenure_months`
  - Rounded to 2 decimals.

- `total_interest(principal, annual_rate, tenure_months)`
  - Computes total interest:
    - `total_payment(...) - principal`
  - Rounded to 2 decimals.

### Schedule and balances

- `amortisation_schedule(principal, annual_rate, tenure_months)`
  - Produces month-wise rows, each with:
    - `month`, `emi`, `interest`, `principal`, `balance`
  - Interest each month = `balance * monthly_rate`.
  - Principal component = `emi - interest`.
  - Running balance reduced by principal component.
  - Includes a guard to avoid negative balance by storing `max(balance, 0.0)`.

- `outstanding_after(principal, annual_rate, tenure_months, months_paid)`
  - Returns outstanding principal balance after a number of paid months.
  - If `months_paid <= 0`, returns original principal.
  - Builds amortisation schedule and returns balance from corresponding row.
  - If `months_paid` exceeds schedule length, returns `0.0`.

### Prepayment logic

- `remaining_tenure(balance, annual_rate, instalment)`
  - Estimates number of months needed to close a remaining balance at fixed instalment.
  - If `balance <= 0`, returns 0.
  - If rate is zero, returns `ceil(balance / instalment)`.
  - Validates that instalment is large enough to reduce principal.
  - Uses logarithmic rearrangement of amortization equation and rounds up with `ceil`.

- `prepayment_savings(principal, annual_rate, tenure_months, prepay_month, prepay_amount)`
  - Scenario: borrower pays a lump sum in a given month and keeps EMI unchanged.
  - Steps:
    1. Compute regular EMI.
    2. Generate full schedule.
    3. Get balance at `prepay_month`.
    4. Subtract lump-sum prepayment from that balance.
    5. Recompute months left for new balance using same EMI.
    6. Compare against original remaining months.
  - Returns:
    - `emi`
    - `months_saved`
    - `new_tenure`
    - `interest_saved`
    - `interest_paid_before_prepayment`

### Offer comparison and eligibility

- `compare_offers(principal, offers)`
  - Expects list of dicts with at least:
    - `bank`, `rate`, `tenure`
    - optional `processing_fee_pct`
  - For each offer computes:
    - EMI
    - total interest
    - processing fee
    - total cost = interest + fee
  - Sorts ascending by `total_cost`.
  - Returns sorted list.

- `eligible_amount(monthly_income, existing_emis, annual_rate, tenure_months, foir=0.5)`
  - Estimates max principal borrower can take.
  - FOIR (fixed obligations to income ratio) controls affordable EMI.
  - Available EMI capacity:
    - `monthly_income * foir - existing_emis`
  - If capacity <= 0, returns `0.0`.
  - If rate is zero, principal is `available * tenure_months`.
  - Else uses inverse EMI math to solve for principal.
  - Rounded to 2 decimals.

### Formatting and export

- `format_inr(amount)`
  - Formats amount as Indian currency string with ₹ and Indian comma grouping.
  - Handles negative values and 2 decimal places.
  - Example style: `₹10,00,000.00`.

- `schedule_to_csv(rows, path)`
  - Writes amortisation rows to CSV file.
  - Header:
    - `month,emi,interest,principal,balance`
  - Then one line per row.

### Summary

- `summary(principal, annual_rate, tenure_months, start=None)`
  - Builds high-level loan summary dict for display:
    - formatted principal
    - rate text
    - tenure text
    - formatted EMI
    - formatted total interest
    - formatted total payment
    - `last_emi` year-month
    - currency code
  - Uses today’s date if `start` not provided.

## `cli.py`

- Uses `argparse` to parse:
  - positional: `principal`, `rate`, `tenure`
  - optional: `--schedule`, `--prepay-month`, `--prepay-amount`
- Always prints summary as JSON.
- If `--schedule` is given, prints each amortisation row.
- If both prepayment flags are provided, prints prepayment savings JSON.


## `loan_calc/__init__.py`

- Re-exports calculator functions so users can import from `loan_calc` package directly.


## Important note for assignment work

The code currently has behavior that can produce incorrect numbers in some scenarios (as your assignment states). This document describes what the current functions are intended to do and how they are implemented now; tests and bug fixes should be applied in later steps.
