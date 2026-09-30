## analytic-gaussian-unseeded-graphical-column
- completed: 2026-09-30
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/105
- retired-by: /prm close-out of ep-moment-projection (`complete/2026/09/ep-moment-projection.md`). This prompt's scope sits inside that record.

### What shipped
- autofit_workspace_test#105 (merge 8f6e19c) seeds `run_joint_fit` in `scripts/graphical/analytic_autofit.py`. The new `SeededDynestyStatic` injects `rstate=np.random.default_rng(seed)` into the sampler kwargs, and `random` / `numpy.random` are seeded for the initializer's live-point draws. This is the "preferred" option in the prompt below.
- Witness met: after seeding, 3 smoke-profile runs of `analytic_gaussian.py` (96 / 130 / 104 s) gave byte-identical tables, as recorded in the PR #105 body. Before seeding, 2 of 6 smoke runs had exited 1 on the graphical column with EP green.
- `run_joint_fit` uses its own `seed=0` default, which equals the script's `SEED = 0`. It does not thread `SEED` through explicitly, so a future change to `SEED` would not reach it. This is a minor gap and does not reopen the prompt.

## Original prompt

# `analytic_gaussian.py`'s graphical column is an unseeded run, so its PARITY count is not reproducible

Type: bug
Target: graphical_ep
Repos:
- autofit_workspace_test
Themes:
- graphical-ep
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: glance
Witness: two consecutive runs of `scripts/graphical/analytic_gaussian.py` under the smoke profile print identical graphical-column numbers
Review-minutes: 5
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-07

## Why

`scripts/graphical/analytic_gaussian.py` compares a closed-form column, a
minimal-EP column and an autofit-EP column against a **graphical** column. The
graphical column is a live `DynestyStatic` run inside `run_joint_fit`, and
`run_joint_fit` sets no seed — the script's `SEED` only reaches `simulate` and
`run_autofit_ep`. Every other column in the script is deterministic and comes
back byte-identical run to run; the graphical one does not.

Two consequences:

- The PARITY count is not a regression signal. Two runs on an identical tree
  read 38/41 and 37/41; the run that lost a row lost it on `x_1` graphical,
  `a=0.101` against a `0.10` tolerance — pure sampler noise sitting on the
  tolerance edge, not a code change.
- The `[info] graphical median_pdf +/- mean|errors_at_sigma(1)|` lines drift
  run to run, so a diff of script output cannot be used to prove "no behaviour
  change" for the graphical column. (Observed while shipping finding D6: a
  control run on the unmodified tree drifted by the same magnitude as the
  edited one, which is how the drift was attributed to the sampler rather than
  the edit.)

## What

Before the moment-matching cure
(`draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md`) un-parks
this script from NEEDS_FIX, make the graphical column reproducible:

- seed `run_joint_fit`'s `DynestyStatic` from the script's `SEED` (preferred —
  it makes the whole script deterministic), **or**
- widen the graphical tolerance past the observed sampler spread, so a
  tolerance-edge row cannot flip the count.

Either way the PARITY count becomes a real regression signal instead of a
coin-flip, which is the point of the parked script.

## Links

- autofit_workspace_test#91 — the analytic Gaussian benchmark findings (D6)
- PyAutoFit#1577 — `errors_at_sigma(as_instance=True)` on a Prior-valued model
- https://github.com/PyAutoLabs/autofit_workspace_test/pull/99 — the D6 workspace docstring PR that surfaced this drift
