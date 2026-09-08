# EP staleness mask flags valid fixed points as stale

- Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1579
- PR: https://github.com/PyAutoLabs/PyAutoFit/pull/1580 (merged 2026-09-08)
- Repo: PyAutoFit, branch `feature/ep-stale-mask-fixed-point`
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1580

## What shipped

An external review of the last three EP PRs (#1574 full-revert = skipped, #1576 per-variable staleness, #1578 errors_at_sigma instance) found one real P2 in #1576: the per-variable `Status.changed` mask in `autofit/graphical/mean_field.py` was a bit-exact `check_changed` test against the previous message, so an accepted projection sitting on its own fixed point read as reverted. EP restarted from its converged `EPMeanField` emitted `STALE FACTORS` for every factor and filled `reverted_variables` on every `ep_history.csv` row while every update was `SUCCESS`. Reproduced on main before any edit.

Fix: `Status.changed` now means "this variable's projection was accepted". The valid branch marks every variable accepted; the invalid branch builds the mask from the `check_valid()` result already computed, before `update_invalid` reverts. `updated` keeps the numerical comparison, so #1574's fully-reverted = skipped classification is unchanged. The optimiser stale-factor report and the diagnostics `reverted_variables` writer are untouched in code (docstrings and comments corrected in `utils.py`, `optimiser.py`, `diagnostics.py`).

Tests: docstring premise of `test_partial_revert_is_recorded_in_ep_history_csv` rewritten (assertions unchanged); new `test_restart_from_fixed_point_is_not_stale` (fails without the fix). `test_autofit/graphical` 279 passed; full suite 2473 passed, 2 skipped. CI: Docs + Tests (3.12, 3.13, nojax) all green on the head sha.

## Witness

EP restarted from its own converged EPMeanField on an exact two-factor Gaussian graph emits `_stale_factor_warnings() == []` and an empty `reverted_variables` column on every row, while `test_autofit/graphical` stays green — held by the new regression test.

## Notes

- #1574 and #1578 needed no action per the same review.
- Heart was YELLOW at ship time on unrelated autolens workspace validation failures and a missing release rehearsal; merge is a library change with no workspace API impact.

## Original prompt

# EP staleness mask flags valid fixed points as stale

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: EP restarted from its own converged EPMeanField on an exact two-factor Gaussian graph emits `_stale_factor_warnings() == []` and an empty `reverted_variables` column on every ep_history.csv row, while test_autofit/graphical stays green (278 passed).
Review-minutes: 3
Unattended: ready
Issued: 2026-09-08

EP staleness mask flags valid fixed points as stale

Type: bug
Target: PyAutoFit
Witness: EP restarted from its own converged EPMeanField on an exact two-factor Gaussian graph emits `_stale_factor_warnings() == []` and an empty `reverted_variables` column on every ep_history.csv row, while test_autofit/graphical stays green (278 passed).

Reproduced (verified 2026-09-08 against an external review of PRs #1574/#1576/#1578): an exact Gaussian graph restarted from its converged EPMeanField emits STALE FACTORS for every factor and lists the variable in ep_history.csv reverted_variables on every row, although every update is SUCCESS and no projection was rejected.

Root cause: the valid branch of the mean-field update (autofit/graphical/mean_field.py) derives `changed` from check_changed, a bit-exact natural-parameter equality test, rather than from projection acceptance; the optimiser stale-factor report and the diagnostics reverted_variables writer consume that mask. Unchanged does not imply rejected.

Fix: valid branch marks every variable accepted; invalid branch builds the mask from the check_valid result already computed before update_invalid; leave `updated` on the numerical comparison so the #1574 fully-reverted=skipped classification is untouched.

Tests: rewrite the docstring premise of test_partial_revert_is_recorded_in_ep_history_csv (its assertions still hold); add a regression test restarting EP from a converged mean field asserting no stale warnings and empty reverted_variables.

<!-- formalised by the Intake (Conception) Agent on 2026-09-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/a1f54e0d-4186-4d30-adbd-45b926f91c04/scratchpad/intake_ep_stale.md -->
