- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1575 (closed completed 2026-09-07)
- completed: 2026-09-07
- library-pr: PyAutoFit https://github.com/PyAutoLabs/PyAutoFit/pull/1576 (head `9b2429f9`, merge `2680b32d`)
- workspace-pr: autofit_workspace_test https://github.com/PyAutoLabs/autofit_workspace_test/pull/98 (head `8184d046`, merge `7050ac3b`)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1576
- pending-release: autofit_workspace_test@https://github.com/PyAutoLabs/autofit_workspace_test/pull/98
- classification: feature (PyAutoFit + autofit_workspace_test) — epic `graphical-ep`; second half of Codex phase-2 review finding 2 (after PyAutoFit#1574); human decided 2026-09-07 on the diagnostics lever.
- ci: PyAutoFit `Tests [pull_request]` 3.12 / 3.13 / nojax + `Docs` green; autofit_workspace_test `Smoke Tests [pull_request]` changes / 3.12 / 3.13 green; both CLEAN; library merged first.
- heart-ack: YELLOW "workspace validation not passing" (organism-scope, cloud#34099198772) + stale "release validation incomplete: no rehearsal for current source"; nothing in either diff is in the release chain.

- summary: `Status.changed` carries the per-variable changed mask out of `MeanField.update_factor_mean_field` (computed on both branches, after `update_invalid`); `EPOptimiser` accumulates seen / changed variables per factor **name** across sweeps (serial and parallel), and `_stale_factor_warnings` names every (factor, variable) pair no member of the group ever moved, keeping the `STALE FACTORS` token. `ep_history.csv` gains `reverted_variables`. The referee `analytic_gaussian_collapse.py` reads it: STALE also when the scatter is reverted on every HierarchicalFactor row; new `sig-rev` column.
- decision: the first cut keyed pairs by factor object and flagged all five referee seeds, because a HierarchicalFactor decomposes into per-dataset sub-factors sharing a name and a few members never move sigma even when the aggregate is healthy; grouping by name clears the healthy seeds (sig-rev 8/10, 10/14, 9/14, 6/11, 8/13 — never n/n) and still catches a group that never moves it.
- verdict: PyAutoFit graphical 275 / messages 95 / full suite 2469 passed; referee RECOVER 5/5, STALE 0/5, warnings (none) on every seed, σ/μ identical to the phase-2 record; workspace smoke gate 14/14.
- remaining: the campaign's N=2 witness configuration (TruncatedGaussian(10, 0.5, 0, 100) on sigma) is expected to drive sig-rev to n/n and be named; not run as a curated script. The moment-matching projection cure stays `draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md`.
- worktree: `~/Code/PyAutoLabs-wt/ep-stale-tracking-per-variable` removed at close-out; 4.7 MB smoke-run scratch deleted (re-derivable).

## Original prompt

# Track EP staleness per (factor, variable), not per factor

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
Themes:
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: the phase-2 campaign graph (N=2, `TruncatedGaussianPrior(10, 0.5, 0, 100)` on sigma, Laplace) names the sigma variable as stale in `ep_diagnostics.results` when its message never moves while the factor's other variables update
Review-minutes: 10
Unattended: needs-slicing
Epic: graphical-ep
Filed: 2026-09-07
Issued: 2026-09-07

Follow-up to `complete/2026/09/ep-full-revert-not-updated.md` (PyAutoFit#1574, finding 2 of the Codex review of
the phase-2 fixes). That fix makes a *fully* reverted projection count as skipped. It cannot name a
*partial* revert: on the campaign graph every hierarchical projection is `BAD_PROJECTION` with the
sigma variable reverted in each one (its message stays `[10.0, 0.7071]` bit-identical, the reported
E[sigma] never leaves the hyper-prior mean), while the factor's mean and per-dataset variables
update — so the factor is "updated" and no STALE FACTORS line appears, which is exactly the #1405
stale-scatter state the warning exists to catch.

Human decided 2026-09-07: the diagnostics lever (per-variable tracking) goes ahead now; the
moment-matching projection cure stays its own prompt.

## Scope

- `EPOptimiser.factor_step` / `_stale_factor_warnings`
  (`autofit/graphical/expectation_propagation/optimiser.py:399-430`): track which *variables* of
  each factor changed on each sweep (the per-variable `changed` mask the bug fix introduces in
  `MeanField.update_factor_mean_field`), and warn on any (factor, variable) pair that never
  changed once — "HierarchicalFactor: variable `sigma` never completed a single update".
- `ep_history.csv` gains a per-variable column or a `reverted_variables` field so the referee
  scripts (`autofit_workspace_test/scripts/graphical/analytic_gaussian_collapse.py`) can tally it.
- The STALE classification in `analytic_gaussian_collapse.py` should then read the per-variable
  flag rather than "no SUCCESS on the HierarchicalFactor".

A prototype tracker exists from the 2026-09-07 verification session (scratch only). Gated by the
campaign's EP-internals check-in like the moment-matching cure
(`ep_hierarchical_scatter_moment_matching.md`); the human decides whether the diagnostics or the
projection is the right lever.
