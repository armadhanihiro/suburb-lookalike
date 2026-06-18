# Test Plan

## Purpose
Provide a concrete test strategy for the Suburb Lookalike Finder project and describe how CI will run unit tests and measure coverage.

## Objectives
- Ensure core logic (similarity, sample data, feature processing) has unit test coverage.
- Prevent regressions by running tests automatically on PRs and pushes.
- Measure test coverage and enforce a minimum threshold.

## Test Types and Scope
- Unit tests: fast, deterministic tests that exercise `engine` modules and helpers.
- Integration-smoke: non-networked checks that ensure `ui` helpers import correctly and sample data loads.
- Avoid running real BigQuery calls in tests; instead, mock the BigQuery client or use the sample data in `engine/sample_data.py`.

## Test Data
- Use `engine/sample_data.get_sample_suburbs()` for local data-dependent tests.
- For BigQuery-related modules, add tests that mock `client.query().to_dataframe()` to return a small DataFrame.

## Local Commands
1. Create and activate a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\Activate.ps1 on Windows
```

2. Install deps and dev deps:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install pytest-cov coverage
```

3. Run tests with coverage:

```bash
pytest --cov=engine --cov-report=term-missing
```

## CI Behavior (GitHub Actions)
- Run test matrix on supported Python versions (3.10, 3.11).
- Install project and dev dependencies, run `pytest` with `pytest-cov`, generate `coverage.xml` and upload as an artifact.
- Enforce a coverage floor (configured in workflow; start with 70%).

## Recommendations / Next Steps
- Add more unit tests for `similarity_weighted.py` and `engine/features.py` (mock BigQuery client). 
- Add linting (ruff/flake8) to CI.
- If using code coverage services (Codecov/Coveralls), add token upload step in a later PR.
