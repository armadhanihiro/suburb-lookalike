# Phase 1 Plan

## Goal
Build the UI skeleton first, with a placeholder-friendly structure, and establish a minimal testing pattern before adding real data.

## Findings
- `app.py` and `app1.py` currently contain duplicate Streamlit UI code.
- The app currently loads BigQuery data immediately on startup.
- There is no test suite or test files in the repo.
- The target screenshot shows a more advanced layout with:
  - left sidebar controls (reference suburb, match count, KPI weights, blend, presets)
  - main result panel (ranked similarity list, radar chart, explanation card)

## Phase 1 objectives
1. Choose and keep one canonical app entrypoint, e.g. `app.py`.
2. Prepare the app for UI-first development by separating layout and data-loading responsibilities.
3. Add test scaffolding and at least one unit test for the existing similarity logic.
4. Keep the initial changes small and non-disruptive.

## Desired changes in Phase 1
- Leave the current core logic untouched.
- Add a minimal `pytest` development dependency.
- Add a `tests/` folder with a simple test verifying `find_similar_suburbs`.
- Prepare a clear phase-2 implementation plan based on the UI wireframe.

## Next steps (phase 2 preview)
- Create the UI skeleton in `app.py` with placeholders for:
  - sidebar control cards
  - match results table
  - radar chart panel
  - explanation summary
- Add a placeholder dataset or sample data path for layout testing.
- Keep actual BigQuery integration as a later step.
- Add more tests for data loading and helper utilities.
