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
