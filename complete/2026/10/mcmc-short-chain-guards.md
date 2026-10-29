# mcmc-short-chain-guards

- completed: 2026-10-25
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1725
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1730
- head: 6830c2ee1b1df53dcce96784186c1cd04f31d535
- merge-commit: 5f770987f2642fdb3a0b83830c3707657282df97
- authorization: human "Yes I authorise" for development after disclosed RED; subsequent human "Prm" for merge and closeout. No release authorized or performed.

## Outcome and validation

Full library suite: 3922 passed, 1 skipped, 1 xfailed (Python 3.12.14). Focused MCMC tests: 14 passed, including real Emcee/Zeus reduced fits with default check_size=100. Additional real Emcee smoke: 10 walkers, 50 steps, test mode disabled, samples built and previous_times=None. Six new regression cases fail on unchanged main (zero thin and empty previous chain), while ordinary thinning remains unchanged. Author diff review passed.

Every workflow and job at the published head passed, including Python 3.12, Python 3.13 and no-JAX, plus docs where applicable. Freeze clear. Source and output identifier logic unchanged during PRM. Author review only; no independent adversary claimed. Published head is an ancestor of origin/main. Local authored commit has an identical tree to the API-published head (different commit metadata); no implementation changes between shipping and merge.

## Closeout

Issue closed as completed. Lifecycle close folds the original prompt, removes the active claim and refreshes the index. Dashboard regenerated with the records. Pending-release key repaired from the verified GitHub label before closeout and carried forward. All four worktrees and their local feature branches removed after verifying identical published trees and merged ancestry. Stage-1 shadow row appended from observed unchanged heads; count after the four closeouts: 53/20. Mind ledger branch will land through the repository ledger automation.

Original Heart RED disclosure retained (not cleared by this task): install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty.

## Original prompt

# Emcee/Zeus: thin can be 0, and check_size blows up on short chains

Issued: 2026-10-25
Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- mcmc
- test-mode
- robustness
Difficulty: small
Autonomy: supervised
Priority: normal
Status: active
Consequence: glance
Witness: `thin` is `max(1, int(max(times) / 2))` in both `emcee/search.py` and `zeus/search.py`, pinned by a unit test on a chain whose largest auto-correlation time is below 2 (`thin == 1`, no `ValueError`); Emcee guards `auto_correlations_from` on chains shorter than `check_size` the way Zeus does, so `af.Emcee(nsteps=10)` under `PYAUTO_TEST_MODE=1` completes; and the #1628 regression tests drop their `AutoCorrelationsSettings(check_size=5, ...)` workaround.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-14
Parent: draft/bug/autofit/emcee_zeus_samples_log_prob_misalignment.md

Two pre-existing robustness defects in the MCMC searches, found while fixing
PyAutoFit#1628 and deliberately left out of that PR because both change values
or behaviour rather than correcting a misalignment.

## 1. `thin` can be 0, which raises

Both `emcee/search.py` and `zeus/search.py` compute:

```python
thin = int(np.max(auto_correlations.times) / 2.0)
```

This is `0` whenever the largest auto-correlation time is below 2.0 — a short or
well-mixed chain. A zero slice step then raises
`ValueError: slice step cannot be zero` inside `get_chain`, and (after #1628)
inside `get_log_prob` as well.

The fix is presumably `max(1, ...)`, but that changes the `thin` **value** on
affected runs, so it needs a deliberate decision rather than a silent clamp:
confirm `thin=1` (no thinning) is the intended behaviour for a chain whose
auto-correlation time is under 2, rather than an error worth surfacing.

## 2. `check_size=100` blows up on chains shorter than 100

`auto_correlations_from` slices `chain[:-check_size]`. With the default
`check_size=100` and a chain shorter than that, the slice is empty and
`emcee.autocorr` raises `IndexError` before the samples object is ever built.

This is **always** true under `PYAUTO_TEST_MODE=1`, where `nsteps=10`.

`Zeus` already guards its equivalent with `except IndexError`; `Emcee` does not,
so the two searches behave differently on the same input. Either Emcee should
gain the same guard, or both should fail with a message naming `check_size` and
the chain length instead of an opaque `IndexError` from a third-party module.

Worked around in the #1628 regression tests by passing
`AutoCorrelationsSettings(check_for_convergence=False, check_size=5, required_length=2)`
— that workaround should become unnecessary once this is fixed.

## Note

Neither is a correctness bug in results: they are crashes and an inconsistency
between the two searches. Do not bundle them with a results-changing fix.

## Folded 2026-09-17

`draft/bug/autofit/emcee_crashes_in_autocorrelation_when_the_chain.md` (filed
2026-09-10) described item 2 above and was removed at the witness-campaign
close-out (PyAutoMind#398). Its witness — `af.Emcee(nwalkers=10, nsteps=50).fit(...)`
on the 1D Gaussian example completes with a warning instead of raising
`IndexError` — is part of this prompt's witness now (Emcee gains Zeus's guard).
