## Outcome
autolens_profiling lint (`pytest scripts/misc/test/`) was red against PyAutoArray main after PyAutoArray#634 (`02aa2e48`, shared Cholesky factor for the positive-negative solve and log det). Fixed in autolens_profiling PR #424 (merge `02705788`, 2026-10-16), issue #423.

- `scripts/misc/likelihood_breakdown/xla_attribution.py`: every abstract.py anchor re-pinned to `02aa2e48` (difflib + AST between `02aa2e48^` and `02aa2e48`, anchored text identical); `LIBRARY_ANCHOR_REVISION` = "PyAutoArray main 02aa2e48 (2026-10-15)". Two whole-function spans (`reconstruction_scatter`, curvature caller) now enclose the NumPy-only #634 branch (never in an XLA trace).
- `library_solver_injection.positive_negative_probe` counts both route-(c) paths: `lu_solve` (`reconstruction_positive_negative_from`: JAX, and NumPy fallback when the factor is None) and `shared_cholesky` (`scipy.linalg.cho_solve` called directly from `AbstractInversion.reconstruction`); `calls` = sum. `fixed_light_library.py` records which path ran.
- Validation: 1457 passed / 6 skipped / 0 failed; ruff clean; CI lint green on `2432bdc2`.
- Shipped under a Heart RED development override (reasons: PyAutoFit/PyAutoGalaxy/PyAutoLens 1 commit behind origin; no rehearsal for current source); the human gave the explicit merge command in the same answer.

Lesson: anchors and probes that pin PyAutoArray internals break on any library PR that edits `abstract.py`; a library PR touching it should run autolens_profiling's `scripts/misc/test/` before merge.

## Original prompt

# autolens_profiling lint red after PyAutoArray#634: re-pin abstract.py anchors, probe the shared-Cholesky route

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: safe
Priority: high
Consequence: notify
Status: formalised
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/423
Filed: 2026-10-16
Issued: 2026-10-16

Original request (human, session 13efb443): "do the bug fix and then go to L2".

PR #422's lint job (run 38883395602) failed `pytest — scripts/misc/test/`, 2 failed / 1454 passed:
- `test_fixed_light_library.py::test_positivity_off_routes_to_the_positive_negative_solver` — "positivity off did not reach reconstruction_positive_negative_from"
- `test_xla_attribution.py::test_the_log_det_anchors_enclose_the_installed_library_functions` — `assert (1037, 1081) == (969, 1013)`

Cause: PyAutoArray#634 (`02aa2e48`, merged 2026-10-15 23:34, after main's last green lint 22:55) touched only
`autoarray/inversion/inversion/abstract.py` (+83). (1) NumPy positivity-off now solves by `scipy.linalg.cho_solve`
on the shared `_curvature_reg_matrix_cho_factor`, falling back to `reconstruction_positive_negative_from` only when
the factor is `None`, so `library_solver_injection.positive_negative_probe` (also used by
`scripts/imaging/pixelized/fixed_light_library.py:954`) never fires. (2) Every `xla_attribution.py` abstract.py
anchor below the insertion moved (pinned at d4298445).

Fix: re-pin every abstract.py anchor in `scripts/misc/likelihood_breakdown/xla_attribution.py` from the AST of
`02aa2e48^` vs `02aa2e48` (content identical, names `LIBRARY_ANCHOR_REVISION`); extend the probe to count the
shared-factor route as route (c) too. Done when the full lint.yml pytest step passes against PyAutoArray main.
