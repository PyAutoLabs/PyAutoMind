## wcs-json-slow-suite-pixelized-fit
- issue: none — asked for directly in session ("make sure this is in one of the quick smokes, maybe the latent one"), the test follow-up to `wcs-json-pixelized-source-clumps`
- completed: 2026-09-12
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/73 (merge `a363f574`)
- repos:
  - euclid_strong_lens_modeling_pipeline
- summary: the pipeline's one real-mode CI fit (`tests/test_latent_run_level.py`,
  the `slow` job) now runs **two** `af.Drawer` fits under one pushed config — the
  light-profile source (10 draws) and the `vis_pix` pixelized source (3 draws,
  builder shared from the new `tests/pixelized_model.py`) — and asserts the
  pixelized `wcs.json` carries `source_model == "pixelized"`, one clump with four
  finite mapper-route images and the solver keys filled from its peak, and that
  `Aggregator.from_directory(..., completed_only=True, unzip_temporary=True)` +
  `agg.values("wcs")` (the call `lens_mass.py` / `magnitudes.py` make) returns
  both records decoded, nested clump list included. Slow suite 4 → 6 passed in
  ~28 s (13 s before); fast 120.
- decision: **not a smoke.** Every `smoke_tests.txt` entry runs under
  `PYAUTO_TEST_MODE`, and `skip_fit_output()` gates the whole of `save_results`
  (`abstract_search.py:617`), so no smoke can ever see `wcs.json`; the latent
  run-level test is the only quick real check the repo has, so it is where
  per-fit file writes are proven. AGENTS.md "Testing" now says so.
- trap: the pixelized fit's latents integrate an inversion per draw and cost
  ~6 s each, five times the light-profile fit's; three draws prove the write
  path, ten would double the job's wall time.
- trap: the aggregator constructor is `autofit.aggregator.Aggregator.from_directory`
  — `af.Aggregator` has no `from_directory`.
- ci: as on #71/#72, every pytest job on the PR reported `skipped` (the Heart
  smoke-gate gap); merged on the local suites; the push to `main` runs the full
  matrix, including the `slow` job this extends.
