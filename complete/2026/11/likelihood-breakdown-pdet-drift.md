## Outcome

autolens_profiling `lint` had been red on main and every PR since PyAutoArray#682 (pseudo-determinant `ln det H` for smoothness regularizations, +9.21 nats per regularized mapper). Two tests pin this harness to the installed library and had drifted. Fixed by PR #524 (merged 2026-11-09, d92aad48), under the live human's Heart-RED development override.

- `reconstruction_steps.log_evidence_terms(..., grounding=None)` computes the #682 pseudo-determinant when given `inversion._intrinsic_regularization_blocks`.
- `FixedLightSystem.reg_grounding` carries it. The NumPy twin `fixed_light_cpu_common.log_evidence_terms_np` applies it.
- `xla_attribution._ABSTRACT_LOG_DET_REGULARIZATION_CALLER` is (1197, 1277), and `LIBRARY_ANCHOR_REVISION` is PyAutoArray main a589c35b.
- Validation: `pytest scripts/misc/*/test` gives 1903 passed, 6 skipped; every lint-job check passes; CI `lint` green.

Not shipped: the per-cell `likelihood_breakdown.py` / `fixed_light*` scripts still score `ln det(H)` without grounding. Re-filed as `draft/bug/autolens_profiling/likelihood_breakdown_cells_pdet_grounding.md`.

## Original prompt

# likelihood_breakdown tests drifted after PyAutoArray#682 (pseudo-determinant log det H)

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- ci
Difficulty: small
Autonomy: supervised
Priority: high
Consequence: judge
Filed: 2026-11-09
Issued: 2026-11-09
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/523

Human request (verbatim, 2026-11-09): "file the bug for the drifted likelihood_breakdown tests and then fix it and do both steps"

PyAutoArray#682 changed log det H to a pseudo-determinant for smoothness regularizations (+9.21 nats per regularized mapper) and moved `log_det_regularization_matrix_term`. autolens_profiling `lint` is red on main and on PR #522: test_active_set_steps (evidence -1007.90 vs -998.69) and test_xla_attribution (anchor (1197,1277) vs (1197,1258)). Plan and remaining drift: see the issue.
