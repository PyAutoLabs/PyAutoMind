# Database scripts fail on release wheels: "Failed to load latent variables" → AssertionError

Type: bug
Target: autofit
Repos:
- PyAutoFit
- autofit_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Surfaced burning down the 2026-07-13 release-validation tail (PyAutoHeart#72). On the release
wheels (mode=release), **all six** `autofit_workspace_test/scripts/database/**` scripts fail
FAST (4–13 s) with a bare `AssertionError`:

```
scripts/database/directory/general.py       ... FAIL (5.4s) AssertionError
scripts/database/directory/multi_analysis.py... FAIL (4.4s) AssertionError
scripts/database/scrape/general.py          ... FAIL (4.3s) AssertionError
scripts/database/scrape/grid_search.py      ... FAIL (8.8s) AssertionError
scripts/database/scrape/multi_analysis.py   ... FAIL (4.4s) AssertionError
scripts/database/scrape/sensitivity.py      ... FAIL (12.7s) AssertionError
```

with a recurring warning:

```
autofit.database.aggregator.scrape - WARNING - Failed to load latent variables for <hash>
```

**Not jax, not perf, not the release profile.** These **PASS on the current dev venv
(jax 0.10.2) even under the release profile (`PYAUTO_TEST_MODE=0`)** — the latent-variable
load emits only the WARNING there and the assertion passes. The wheel code is identical to
main HEAD, so the delta is the **wheel-env dependency set**: the release stack resolves
`SQLAlchemy 2.0.51`, `dill 0.4.1`, `numpy 2.4.6` (full list in the rehearsal install log of
run `29279095224`). The most likely culprit is a **serialization/deserialization
incompatibility in the latent-variable load path** (`autofit.database.aggregator.scrape` →
whatever loads latent samples from the SQLAlchemy-backed database) under one of those
dependency versions.

**Reproduce with the wheel dependency set** (the dev venv won't show it): build a venv with
the release stack — `pip install --index-url https://test.pypi.org/simple/ --extra-index-url
https://pypi.org/simple/ "autolens[optional]==2026.7.13.1.dev65601" jax jaxnnls jax_zero_contour`
(a scratch `rel-venv` approximating this already exists from the 2026-07-14 session) — then run
`scripts/database/scrape/general.py` from `autofit_workspace_test/` and capture the full
traceback (the one-line CI summary hides the assertion detail). Isolate which dependency flips
it (SQLAlchemy vs dill vs numpy) by pinning them one at a time.

Fix the producer of the bad load (don't silence the warning — [[feedback_no_silent_guards]]):
if latent variables genuinely fail to deserialize under the newer dep, fix the
load/serialization in `autofit.database`; if the scripts' assertion is over-strict about a
tolerable-missing latent, fix the assertion. Release run: PyAutoHeart workspace-validation
`29279095224`, TestPyPI `2026.7.13.1.dev65601`. See [[project_release_2026_07_13_blocked_3bugs]].
