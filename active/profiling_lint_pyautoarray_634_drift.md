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
