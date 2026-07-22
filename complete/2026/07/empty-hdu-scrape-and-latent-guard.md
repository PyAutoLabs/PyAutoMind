## empty-hdu-scrape-and-latent-guard
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1413 (CLOSED — auto-closed by the PR's `Closes` line)
- completed: 2026-07-22
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1415 (MERGED 2026-07-22T10:11:37Z)

**Outcome:** the prompt's premise was wrong for 3 of its 4 scripts. Filed from the 2026-07-21 census as four test-mode `NoneType` failures needing `env_vars.yaml` overrides ("small, pure env_vars work"); reproduction found one real defect, and it was a **library bug**, not env config.

**The real bug (fixed, merged).** `autofit/database/model/array.py` — the `HDU.hdu` setter assigned `hdu.data` into the inherited `Array.array` setter, which dereferences `array.dtype` unguarded, so any data-less HDU raised `AttributeError: 'NoneType' object has no attribute 'dtype'` and aborted the whole sqlite scrape. Not test-mode-specific and not env-dependent: minimal repro is `db.HDU(hdu=fits.PrimaryHDU())`. **User-facing** — `aggregate_fits.py:107` emits an empty `PrimaryHDU` as the first HDU of every aggregated HDUList (its own docstring at L94 says so), so the database path could not ingest the library's own aggregated FITS output. Fix = store a null payload, reconstruct with `data=None`, distinguish via a new `HDU.has_data` property.

**TRAP — the census false-positive mechanism (3 of 4 verdicts).** `PYAUTO_TEST_MODE=2` writes NO samples, so a *second* run against a warm output tree takes the `Fit Already Completed: skipping non-linear search` path and returns `result.samples = None`. Every downstream access then throws `NoneType` — `.parameter_lists`, `.sample_list`, `.model`, whichever the script reaches first. `rm -rf output/test_mode/<name>` and re-run before believing any such failure. `imaging/model_fit.py` and `latent/latent_variables_smoke.py` were verified passing untouched and need NO change.

**TRAP — green ≠ exercised.** `latent/latent_nan_robustness.py` passes but VACUOUSLY: `TEST_MODE=2` yields only 4 bypass samples, AND `DISABLE_JAX=1` silently flips its deliberate `AnalysisImaging(use_jax=True)` to `False` (PyAutoLens `analysis/analysis/dataset.py:89`), so the JAX column-masking branch the guard exists to catch never runs. Same shape as the existing `searches/MultiStartAdam` / `searches/BlackJAXNUTS` overrides.

**Verification:** new tests confirmed to FAIL without the fix with the exact reported error at `array.py:56` (non-vacuous); `test_autofit/` 1527 passed / 1 skipped; `profile_database.py` exit 0 (was the reported crash); `database/scrape/general.py` re-smoked exit 0 on the widened path; `black --check` clean; CI green on docs + unittest 3.12/3.13.

**Heart:** shipped YELLOW score 52, `red_reasons` empty, human-acknowledged for 4 pre-existing reasons (workspace validation 2026-07-20; 58 stale parked scripts; 10 slow scripts; PyAutoCTI open PR age) — none caused by this diff.

**Conflicts navigated:** `worktree_check_conflict` flagged PyAutoFit (claimed by `interpolator-stale-needs-fix`, `worktree: none`, in-place branch) — human approved proceeding in a dedicated worktree since files were disjoint. `autolens_workspace_test` was flagged with a LIVE worktree (`slow-skip-timeout-cap-doc`), which is why the workspace half was split out rather than forced.

**SPUN OUT — workspace half:** `latent-nan-guard-honest-run` in `planned.md`, blocked-by `slow-skip-timeout-cap-doc`. Needs a FRESH issue (#1413 is closed). Measurements banked: honest run 412s vs the 300s cap; `PYAUTO_TEST_MODE=1` does NOT help (455s) because Nautilus is not the bottleneck (~136s post-fit results update + ~56s latent compute on 100 samples) — sample count is the lever. Script is in the curated `smoke_tests.txt`, which DOES read `env_vars.yaml`.

**Follow-up not filed:** bypass-mode output dirs resolving as "Fit Already Completed" with `samples=None` is a genuine PyAutoFit resume-path trap, deliberately left out of scope.

## Original prompt

# Test-mode NoneType failures: scripts that need real samples/fits (env_vars overrides)

Type: bug
Target: workspaces
Repos:
- autolens_workspace_test
- autofit_workspace_test
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

From the 2026-07-21 census. These are NOT code bugs — they are the known "script needs real samples /
a real fit, but the smoke profile bypasses the sampler" env-config gap. Each fails with a NoneType
attribute error because the aggregator/samples object is empty under `PYAUTO_TEST_MODE=2`.

- autolens_workspace_test `imaging/model_fit.py` — `AttributeError: 'NoneType' object has no attribute 'parameter_lists'`
- autolens_workspace_test `latent/latent_nan_robustness.py` — `'NoneType' has no attribute 'sample_list'`
- autolens_workspace_test `latent/latent_variables_smoke.py` — `'NoneType' has no attribute 'model'`
- autofit_workspace_test `profiling/aggregator/profile_database.py` — database array HDU is None -> `'NoneType' has no attribute 'dtype'`

Fix: add per-script overrides in each repo's `config/build/env_vars.yaml` unsetting `PYAUTO_TEST_MODE`
(and `PYAUTO_SKIP_FIT_OUTPUT` where the script reads outputs), mirroring the existing
`guides/results/` and `database/scrape/` precedents. Keep them fast — prefer the minimum unset that
produces real samples. Verify each via `run_python.py <project> <scripts/dir>`; confirm no sibling
regressions and that runtimes stay within the per-script cap.
