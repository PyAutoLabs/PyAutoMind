# HowToFit tutorials 6 and 7 die at the NUTS fit — `blackjax` is on no install route

Type: bug
Target: HowToFit
Repos:
- HowToFit
- PyAutoNerves
Themes:
- tutorials
- colab
- dependencies
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Witness: with only `pip install autofit numba` (or a Colab `setup_colab.setup("howtofit")`), `python3 scripts/chapter_1_introduction/tutorial_6_gradients.py` and `tutorial_7_the_details.py` both run to completion instead of raising `ModuleNotFoundError: No module named 'blackjax'`.
Filed: 2026-09-15
Issued: 2026-09-15

## Symptom

Measured 2026-09-15 against HowToFit main @ b174c03 (PR #62), PyAutoFit main,
Python 3.12.3, at real settings (no `PYAUTO_TEST_MODE`, visualization on):

    tutorial_6_gradients.py    FAIL (11.0s)  ModuleNotFoundError: No module named 'blackjax'
    tutorial_7_the_details.py  FAIL (67.1s)  ModuleNotFoundError: No module named 'blackjax'

Installing `blackjax>=1.6.2` and `nautilus-sampler` and re-running, nothing
else changed: tutorial 6 rc=0 in 43s, tutorial 7 rc=0 in 73s, both completing
their real `BlackJAXNUTS` (and, in 6, `Nautilus`) fits. The missing
dependency is the whole defect.

## Why no gate sees it

CI runs `PYAUTO_TEST_MODE=2` (`config/build/profile_smoke.yaml`), which
bypasses the sampler, so `af.BlackJAXNUTS` is never constructed and blackjax
is never imported. Both tutorials PASS the smoke gate — 18/18 green — while
being unrunnable by a reader. This is the same blind spot `config/build/no_run.yaml`
already documents for `tutorial_5_expectation_propagation` ("only passes today
because CI runs at PYAUTO_TEST_MODE=2, which bypasses the sampler").

## Why it is missing on every route

- `HowToFit/requirements.txt` is `autofit` + `numba`.
- PyAutoFit declares blackjax in the **optional** extra, not the base
  dependencies (`PyAutoFit/pyproject.toml:83`, `[project.optional-dependencies]
  optional`), so `pip install autofit` does not bring it. Same for
  `nautilus-sampler`, which tutorial 6 also runs (`:727`).
- Colab: `autonerves/setup_colab.py` installs `_SHARED_EXTRAS` with `--no-deps`
  (`:280`). `_SHARED_EXTRAS` (`:37-46`) lists pyvis, dill, jaxnnls,
  nautilus-sampler, timeout_decorator, anesthetic, emcee, dynesty — and no
  blackjax. Exactly the gap PyAutoNerves #166 closed for emcee and dynesty,
  one package short.

Searches actually run: tutorial 6 — LBFGS, MultiStartAdam, Emcee,
BlackJAXNUTS(`:685`), Nautilus(`:727`); tutorial 7 — DynestyStatic x3,
Emcee x2, MultiStartAdam x2, BlackJAXNUTS(`:1086`).

Tutorial 7's NUTS fit is **new tonight**: PR #62 moved the Hamiltonian
diagnostics out of tutorial 6 and gave tutorial 7 its own short BlackJAXNUTS
fit, so tutorial 7 is a fresh breakage, tutorial 6 a pre-existing one.

## Fix

1. `PyAutoNerves/autonerves/setup_colab.py`: add `"blackjax>=1.6.2"` to
   `_SHARED_EXTRAS`, tracking `PyAutoFit/pyproject.toml`'s specifier as the
   emcee/dynesty entries already do.
2. `HowToFit/requirements.txt`: add `blackjax` and `nautilus-sampler` so the
   documented local route installs what the tutorials run.
3. While there: `_SHARED_EXTRAS` pins `nautilus-sampler==1.0.4` where
   PyAutoFit's optional extra pins `==1.0.5`. Reconcile.

A follow-up worth its own prompt: the smoke profile's `PYAUTO_TEST_MODE=2`
cannot see a missing sampler dependency at all. A cheap guard is an import
check over the `af.<Search>` classes each script constructs, run at smoke
settings.
