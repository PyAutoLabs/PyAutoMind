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

EP staleness mask flags valid fixed points as stale

Type: bug
Target: PyAutoFit
Witness: EP restarted from its own converged EPMeanField on an exact two-factor Gaussian graph emits `_stale_factor_warnings() == []` and an empty `reverted_variables` column on every ep_history.csv row, while test_autofit/graphical stays green (278 passed).

Reproduced (verified 2026-09-08 against an external review of PRs #1574/#1576/#1578): an exact Gaussian graph restarted from its converged EPMeanField emits STALE FACTORS for every factor and lists the variable in ep_history.csv reverted_variables on every row, although every update is SUCCESS and no projection was rejected.

Root cause: the valid branch of the mean-field update (autofit/graphical/mean_field.py) derives `changed` from check_changed, a bit-exact natural-parameter equality test, rather than from projection acceptance; the optimiser stale-factor report and the diagnostics reverted_variables writer consume that mask. Unchanged does not imply rejected.

Fix: valid branch marks every variable accepted; invalid branch builds the mask from the check_valid result already computed before update_invalid; leave `updated` on the numerical comparison so the #1574 fully-reverted=skipped classification is untouched.

Tests: rewrite the docstring premise of test_partial_revert_is_recorded_in_ep_history_csv (its assertions still hold); add a regression test restarting EP from a converged mean field asserting no stale warnings and empty reverted_variables.

<!-- formalised by the Intake (Conception) Agent on 2026-09-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/a1f54e0d-4186-4d30-adbd-45b926f91c04/scratchpad/intake_ep_stale.md -->
