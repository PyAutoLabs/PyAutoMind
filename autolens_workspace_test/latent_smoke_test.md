# Add a smoke test exercising all PyAutoLens library latents

## Context

Parent epic: [`PyAutoPrompt/z_features/latent_refactor.md`](../z_features/latent_refactor.md).
Depends on [`autolens/latent_module.md`](../autolens/latent_module.md) (lensing latent spine must be in place).

After sub-prompt #2 ships, PyAutoLens has a curated, yaml-toggled set of latents. We need a high-class smoke test that runs frequently (via `/smoke_test`) and exercises every default-enabled latent end-to-end, so library refactors don't silently break the latent pipeline.

## Task

1. **Add a single test script** at `autolens_workspace_test/scripts/<category>/latent_variables.py` — pick the directory that best matches existing smoke-test structure (likely `imaging/modeling/` or a fresh `latent/` dir).

2. **What it does:**
   - Sets up a minimal lens model (SIE + source) and a tiny imaging dataset (use existing test fixtures).
   - Runs a non-linear search under `PYAUTO_TEST_MODE=2` so the sampler is skipped — single representative draw is enough.
   - Verifies the `latent/` output dir contains the expected files (`samples.csv` or `latent_summary.json`).
   - Reads them back and asserts:
     - Every default-enabled key from `autolens/config/latent.yaml` is present.
     - All values are finite (no nan/inf — per memory `feedback_no_silent_guards`).
     - Each value falls within a sane order-of-magnitude bracket (loose but not vacuous).

3. **Add to `smoke_tests.txt`** — this is the rare case where adding to the smoke set is correct (per memory `feedback_smoke_tests_small_subset`, smoke is a curated subset; the latent pipeline is a structural regression risk worth catching often).

4. **Verify it works under `PYAUTO_TEST_MODE` properly** (memories `feedback_autofit_cache_resume_pyauto_test_mode` and `feedback_smoke_env_grid_mutations_inside_decorators`):
   - Output path must include the `output/test_mode/` segment.
   - Grid mutations from `PYAUTO_SMALL_DATASETS` etc. must not invalidate the latent calculations (e.g. magnification on a 15×15 grid should still be finite, even if numerically less accurate than full-res).

## Where to look

- Existing smoke-test scripts in `autolens_workspace_test/scripts/` — pick one of similar shape to mirror imports + structure.
- `autolens_workspace_test/smoke_tests.txt` — append the new script path.
- `autolens_workspace_test/config/build/env_vars.yaml` — if any env-var override is needed for this script, set it here (per memory `feedback_env_vars_yaml_overrides`, do **not** mutate `os.environ` from within the script).
- PYAUTO_TEST_MODE semantics: `autofit` repo, `PYAUTO_TEST_MODE=2` = skip sampler.

## Verification

```bash
source ~/Code/PyAutoLabs-wt/<task-name>/activate.sh
cd autolens_workspace_test
python scripts/<path>/latent_variables.py       # direct run
/smoke_test                                      # full smoke pass including the new test
```

Smoke test should complete in under ~10 seconds (in line with the rest of the smoke set).

## Affected repos

- autolens_workspace_test (primary)

## Suggested branch

`feature/latent-smoke-test`

## Notes

- Per CLAUDE.md model split: this is a test/dev script, comments are short API-usage notes — **Sonnet** is fine.
- Per memory `feedback_no_smoke_tests_in_library_test_dirs`: this lives in `autolens_workspace_test`, NOT in `PyAutoLens/test_autolens/`.
- Per memory `feedback_ship_workspace_binary_leak`: confirm the script's output dir (likely `output/test_mode/...`) is `.gitignore`d before `/ship_workspace`. Pre-flight `git diff --stat` for binaries.
- Single posterior draw is the right granularity — full search defeats the "high-class smoke" purpose.
