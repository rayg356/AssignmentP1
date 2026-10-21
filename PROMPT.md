# Prompt Log — Assignment P1 (loan-calc)

This file is my record of how I used AI support during the assignment, what advice was useful, and what needed correction after verification.

## Context

The repo started as a small loan calculator with no tests and reported calculation issues.  
The assignment required me to:
- explain the codebase in `ARCHITECTURE.md`,
- add docstrings/type hints for public functions,
- add pytest coverage for required edge cases,
- fix seeded bugs through test-driven verification,
- and reach at least 85% coverage.

---

## 1) Function-by-function explanation (`ARCHITECTURE.md`)

**What I asked AI to do**  
Summarize what each function in `loan_calc/calculator.py` and `cli.py` does.

**What AI returned**  
A structured walkthrough of all major functions and data flow.

**What I verified myself**  
I cross-checked each function with the source code and corrected wording where needed (especially around schedule behavior and prepayment flow), then rewrote sections in my own style.

**Result**  
`ARCHITECTURE.md` reflects the current code behavior and is phrased in my own words.

---

## 2) Seeded bug analysis and fix sequencing

**What I asked AI to do**  
Identify likely seeded bugs and suggest a safe commit-by-commit order.

**What AI returned (useful parts)**  
It highlighted three high-impact areas:
1. amortisation schedule loop boundary,  
2. final-month settlement behavior,  
3. incorrect monthly rate usage in remaining tenure logic.

**What I verified myself**  
I checked each claim against the file and only treated it as valid after confirming in code.

**Result**  
I used this as the basis for stepwise debugging and separate commits.

---

## 3) Test case proposal (including required edge cases)

**What I asked AI to do**  
Propose and generate pytest cases required by assignment:
- 0% interest,
- 1-month tenure,
- very large principal,
- prepayment larger than balance.

**What AI returned**  
A `tests/test_calculator.py` test set with these edge cases plus baseline consistency checks.

**What I verified myself**  
I reviewed each test for realism and direct alignment with assignment requirements before running.

**Result**  
Required edge cases are represented in tests.

---

## 4) Example where AI output was wrong/incomplete

**Issue recorded for acceptance criterion**  
At one point, AI progress tracking suggested docstrings/type hints were complete, but code review showed those edits were not actually present in file state yet.

**How I handled it**  
I treated file contents as source of truth, reverted checklist status, and continued only after actual code-level confirmation.

**Why this matters**  
This demonstrates that AI guidance was helpful but still required manual verification, as required by the assignment.

---

## 5) Test execution and coverage reality check

**What I asked AI to do**  
Run tests and assess progress.

**Observed output**  
Tests passed (`11 passed`), but coverage was only about `57%`.

**Interpretation**  
Passing tests did not satisfy assignment coverage threshold (>=85%).

**Action taken**  
I used coverage gaps to plan additional tests for under-covered functions and branches.

---

## Reflection

AI helped speed up exploration and drafting, but I had to verify every important claim against:
- actual file contents,
- pytest outputs,
- and coverage reports.

The most useful workflow was: **ask → verify in code/tests → accept or correct**.
