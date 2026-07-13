## test-mode-fake-sample-count
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1313
- completed: 2026-06-08
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1314 (merged 2e41016)
- repos: PyAutoFit
- notes: Expanded `PYAUTO_TEST_MODE=2/3` bypass-mode fake results from two to four deterministic samples so downstream latent-variable and multi-batch sample checks can run while still skipping the real sampler. Verified targeted `test_abstract_search.py` coverage, full PyAutoFit suite (`1413 passed, 14 skipped`), three latent robustness release blockers, PR CI, and local smoke across configured workspaces (`46 passed, 0 failed, 2 skipped`).

## Original prompt

# Test-mode fake sample count for latent robustness

## Original user request

ok back to the release list

## Context

The release PyAutoBuild run `2026-06-08T16-10-15Z` failed three latent robustness guards:

- `autofit_workspace_test/scripts/features/latent_nan_robustness.py`
- `autogalaxy_workspace_test/scripts/latent/latent_nan_robustness.py`
- `autolens_workspace_test/scripts/latent/latent_nan_robustness.py`

All three fail before exercising their intended latent masking assertion because the search result has only two samples:

```text
AssertionError: Need >3 samples for a multi-batch latent run; got 2.
```

The common cause appears to be PyAutoFit test-mode bypass. `autofit/non_linear/search/abstract_search.py::_build_fake_samples` always creates exactly two fake samples when `PYAUTO_TEST_MODE=2` or `PYAUTO_TEST_MODE=3`, which is too few for structural downstream guards that need multiple latent batches.

## Goal

Update PyAutoFit test-mode bypass so fake samples are still cheap but numerous enough for multi-batch downstream structural checks. Preserve existing bypass semantics: no real sampling, deterministic fake samples, and valid `SamplesPDF` summary behavior.

## Suggested verification

- Add / update PyAutoFit unit coverage for `_build_fake_samples` or bypass-mode fitting to assert at least four fake samples are returned.
- Run the relevant PyAutoFit unit tests.
- Run the three downstream latent robustness scripts, or at least confirm they progress past the sample-count assertion.
