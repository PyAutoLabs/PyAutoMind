## Outcome

Corrective fix for Heart RED "release validation FAILED (stage integrate)",
merged as autolens_workspace_test#363 (eb30383, 2026-11-11). Live human
authorization on #362.

- Cause: `scripts/interferometer/model_fit.py`'s PR #504 non-vacuity guard
  used the net |figure_of_merit − log_likelihood| >= 1 nat as a proxy for
  "log-det terms present". PyAutoArray#683's pseudo-determinant raised
  log det H by 0.5·ln(1e8) per intrinsic-regularized mapper; the net crossed
  zero and landed at +0.80 nat at release resolution (integrate run
  42998439751: 814 pass / 1 fail).
- A/B at smoke scale: log det(F+H) 122.67 both sides, log det H
  113.04 → 131.46, net −4.83 → +4.39 (healthy terms, coincidental cancellation).
- Fix: assert each inversion log-det term >= 1 nat; the LLF == fom == call_wrap
  checks are unchanged.
- Evidence: smoke-scale full run passes (15 s); a zeroed-terms control fails;
  PR smoke CI green (it does not include this script).
- Post-merge: Stage 3 integrate re-run on the same wheels
  (2026.11.11.1.dev87401; library HEADs unchanged), PyAutoHeart run 43018956933.
- Split out: draft/bug/health_fixes/pr504_sibling_guards_net_gap_proxy.md.

## Original prompt

# interferometer/model_fit.py PR #504 non-vacuity guard trips after the pseudo-determinant

Type: bug
Target: autolens_workspace_test
Repos: @autolens_workspace_test
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-11-11
Issued: 2026-11-11

## Evidence

Release validation (rehearsal 2026.11.11.1.dev87401, Hands run 42995913484;
integrate https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/42998439751)
scored 814 pass / 1 fail / 85 skip / 0 timeout. Heart is RED
"release validation FAILED (stage integrate)". The one failure:

    scripts/interferometer/model_fit.py  AssertionError: CPU: figure_of_merit (-4719.047795054418)
    is within 1 nat of log_likelihood (-4719.848762254507) — pixelization regularization log-det
    terms are zero, this script no longer exercises the bug PR #504 fixed

The guard (`_assert_likelihood_sanity`) uses the NET gap `figure_of_merit -
log_likelihood` (|gap| >= 1 nat) as a proxy for "the log-det terms are
non-zero". PyAutoArray#683 (a589c35, pseudo-determinant for intrinsic
regularization; merged, pending release) raises `log det H` by 0.5·ln(1e8) per
intrinsic-regularized mapper. The 2026-11-10 pseudo-det rebaseline missed this
guard.

Smoke-scale A/B (PYAUTO_SMALL_DATASETS=1, prior medians, 2026-11-11):

| Array | log det(F+H) | log det H | reg | fom − logL |
|---|---|---|---|---|
| pre-#683 c020cc24 | 122.6716 | 113.0364 | 0.0153 | −4.8253 |
| main 2e494f94 | 122.6716 | 131.4571 (+18.42) | 0.0153 | +4.3851 |

The terms are large and healthy. The net gap crossed zero, and at
release resolution it landed at +0.80. The guard is a knife-edge proxy, the
same class of failure its own comment records for run 33220882817.

## Repair scope

Make the guard assert what its message claims: the inversion's log-det terms
are present and non-trivial (e.g. `log_det_curvature_reg_matrix_term` and
`log_det_regularization_matrix_term` each move the objective by >= 1 nat), plus
the existing LLF == figure_of_merit == call_wrap equalities, rather than the net
gap. Do not just loosen the threshold. Check sibling scripts with the same
proxy. Then re-run release validation.
