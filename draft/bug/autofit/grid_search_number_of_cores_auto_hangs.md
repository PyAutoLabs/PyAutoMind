# GridSearch hangs with number_of_cores="auto"

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Epic: likelihood-lifecycle
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-26

## Context

R6 (PyAutoLabs/PyAutoGalaxy#759, PyAutoFit#1800) flipped every search's default to `number_of_cores="auto"` except `GridSearch`. With `"auto"`, the PyAutoFit test suite hung inside the grid search's own `Process` job pool (`autofit/non_linear/grid/grid_search/__init__.py`, with a `MockMLE` sub-search), also with JAX absent. Human ruling 2026-11-26: keep `GridSearch` at 1 for now and file this bug.

## Ask

Find why the nested job pool hangs when the grid search resolves `"auto"` (likely the parent pool and per-job sub-search pools both taking all cores, or a fork/pickling deadlock), make `"auto"` safe (e.g. resolve the grid-level count once and force sub-searches to 1), then flip `GridSearch`'s default to `"auto"` with a test that would have hung.
