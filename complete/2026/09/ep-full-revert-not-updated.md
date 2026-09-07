- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1571 (closed completed 2026-09-07)
- completed: 2026-09-07
- library-pr: PyAutoFit https://github.com/PyAutoLabs/PyAutoFit/pull/1574 (head `02763895`, merge `4e6a160d`)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1574
- classification: bug (PyAutoFit) — epic `graphical-ep`; bundle `ep-phase2-review` (Codex review of the phase-2 fixes, finding 2 + README wording carry-over). No workspace PR.
- ci: `Tests [pull_request]` unittest 3.12 / 3.13 / nojax green, `Docs [pull_request]` green; CLEAN.
- heart-ack: YELLOW "workspace validation not passing" (organism-scope, cloud#34099198772); nothing in this diff is in the release chain.

- summary: `MeanField.update_factor_mean_field` re-evaluated `check_valid()` after `update_invalid(last_dist)`, true by construction, so a projection that reverted every parameter still returned `updated=True` and never reached `_stale_factor_warnings`. Now compares the reverted message to `last_dist` per variable on natural parameters (`MeanField.check_changed`, exact); nothing changed = skipped, with an explicit status message; partial reverts still count as updates. README §3.5 now says the minimal Laplace EP reaches the stale-factor state, not a collapse; STALE FACTORS paragraph notes full reverts count as skipped.
- verdict: two new tests fail without the fix, one pins the partial-revert half; graphical 268 (270 with #1573); `analytic_gaussian_collapse.py` RECOVER 5/5, STALE 0/5, σ/μ identical; per-factor flag tallies shift because the flag now means "moved".
- remaining: partial reverts (the campaign graph's scatter reverting every sweep while other variables update) are still reported as updated — filed as `draft/feature/autofit/ep_stale_tracking_per_variable.md`.
- worktree: shared bundle worktree `~/Code/PyAutoLabs-wt/ep-phase2-review` removed at the bundle's close-out.

## Original prompt

# A fully reverted projection still reports `updated=True`, suppressing the STALE FACTORS warning

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: an EP run whose factor projection reverts every parameter each sweep lists that factor under `factors skipped`, not `factors updated`, and `ep_diagnostics.results` carries the STALE FACTORS line; new test in `test_autofit/graphical/functionality/test_factor_failure_recovery.py`; the two raising-optimiser stale tests still pass; `grep -n "reproduces the collapse" autofit/graphical/README.md` is empty
Review-minutes: 5
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-07
Issued: 2026-09-07

Finding 2 (P2) plus the README prose carry-over of the Codex review of the graphical-ep phase-2
fixes (review text verbatim in the sibling `ep_laplace_deterministic_hessian.md`). Reproduced on
`main` (f6a991504) on 2026-09-07.

## Reproduction (2026-09-07)

- Unit: a projection whose q* is wider than the cavity in every variable returns
  `flag=BAD_PROJECTION, success=False, updated=True`, with the returned message bit-identical to
  `last_dist`.
- End-to-end `EPOptimiser` (2-factor shared-variable graph, one factor fitted over-wide every
  sweep): that factor's message ends `[0., 10.]` = its starting prior, yet it is listed under
  `factors updated`, `factors skipped` is empty, and no STALE line is logged.
- The campaign graph (N=2, `TruncatedGaussianPrior(10, 0.5, 0, 100)` on sigma, Laplace): 4/4
  hierarchical projections `BAD_PROJECTION` with `updated=True`; the factor's sigma message stays
  `[10.0, 0.7071]` bit-identical while its other variables update — no warning. That *partial*
  revert needs per-variable tracking and is filed separately
  (`draft/feature/autofit/ep_stale_tracking_per_variable.md`); this prompt fixes the full revert.

## Mechanism

`autofit/graphical/mean_field.py:513-543` (`MeanField.update_factor_mean_field`, the
`if not factor_dist.is_valid` branch): line 525 replaces the invalid parameters with `last_dist`'s
via `update_invalid`; lines 528-530 then set `updated = True` when `factor_dist.check_valid().any()`.
`check_valid` is evaluated after the revert, and reverted parameters come from a valid message, so
it is true by construction: it measures validity, not change. `EPOptimiser.factor_step`
(`expectation_propagation/optimiser.py:399-403`) trusts the flag, so
`_stale_factor_warnings` (line 430, `(raised | skipped) - updated`) never names the factor. Only
the `success=False` early return (mean_field.py:485-497) sets `updated=False`, which is why the
#1562 tests pass.

## Fix

Replace the post-revert `check_valid().any()` test with a per-variable "changed vs `last_dist`"
comparison (a `MeanField.check_changed(other)` over the message parameters, or inline);
`updated = changed.any()`, and when nothing changed append
`"factor update skipped: every parameter reverted"` to `messages`. `success` semantics unchanged.

Test: a fixture optimiser that always returns an over-wide fit; assert the factor is in
`factors skipped`, absent from `factors updated`, and the STALE FACTORS line is in
`ep_diagnostics.results`. The existing stale tests
(`test_never_updating_factor_is_warned_about_loudly`,
`test_stale_factor_warning_is_written_to_the_diagnostics_file`) use a raising optimiser and never
reach the `status.updated` branch; keep them.

Docs: `autofit/graphical/README.md` §3.5 lines 244-246 — "reproduces the collapse under a Laplace
projection" → "reproduces the stale-factor state (every site update rejected, scatter returned at
its prior) under a Laplace projection" (the phase-1 wording error, already fixed in the workspace
by autofit_workspace_test#97). Add one sentence to the STALE FACTORS paragraph (~line 189) that a
fully reverted projection now counts as skipped.
