# Test-mode representative outputs — Phase 3: profiling recipe + validation

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 3 of 4 of `draft/feature/autofit/test_mode_representative_outputs_size_realistic.md`.
Blocked until phase 2's library PR is merged (uses its API-change summary). This is
the phase that pays off the parent's motivation: instant cold SLaM runs with honest
resume timings for the `pipeline_resume` tier (born from autolens_profiling#70).

## Scope

- Wire the recipe into the @autolens_profiling `pipeline_resume` tier: cold run with
  `PYAUTO_TEST_MODE=2 PYAUTO_TEST_MODE_SAMPLES=<N>` completing in seconds-to-minutes,
  then the resume invocation **with `PYAUTO_TEST_MODE` still set** — output is
  namespaced under `output/test_mode/`, so unsetting it on resume silently looks at a
  different output tree.
- Validate size parity: samples.csv row count and byte size of a bypass-completed
  stage vs a real Nautilus SLaM stage at the chosen N; record the comparison in the
  tier's results.
- Measure resume overhead (samples CSV parse, zip/unzip restore, weight arithmetic)
  on the synthetic outputs and sanity-check against the production-sized numbers
  from autolens_profiling#70. Benchmarks on an idle machine.
- Update the tier README with the recipe and the known deltas (test mode auto-skips
  latents; search-internal state and adapt-image FITS values are not representative —
  fine for timing, not science).

## Ship

`ship_workspace`: single autolens_profiling PR (recipe + validation results + README).
