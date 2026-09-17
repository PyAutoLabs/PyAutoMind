# Emcee/Zeus: thin can be 0, and check_size blows up on short chains

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
Status: formalised
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
