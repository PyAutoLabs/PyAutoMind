# Fix autofit workspace-test database scrape paths

Original user request:

> continue

Release report context:

The PyAutoBuild release run reports two failures in `autofit_workspace_test`:

- `scripts/database/scrape/grid_search.py`
- `scripts/database/scrape/sensitivity.py`

Both fail at `assert len(agg) > 0` after `Aggregator.from_database(...).add_directory(...)`.

Reproduction on current `main` using the PyAutoBuild environment:

```bash
(cd autofit_workspace_test && env PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1 PYAUTO_DISABLE_JAX=1 PYAUTO_FAST_PLOTS=1 JAX_ENABLE_X64=True NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib python3 scripts/database/scrape/grid_search.py)
```

The search writes results under `output/test_mode/database/scrape/...`, but the scrape scripts add `output/database/scrape/...`, so the aggregator finds zero search outputs.

Fix the workspace-test scripts so they scrape the actual output path used by the active PyAutoBuild/test-mode environment while preserving normal non-test-mode behavior.
