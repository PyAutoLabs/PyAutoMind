## autofit-scrape-test-mode-paths
- issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/35
- completed: 2026-06-09
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/36 (merged b5a6a43)
- repos: autofit_workspace_test
- notes: Fixed the database scrape release failures by making `scripts/database/scrape/grid_search.py` and `scripts/database/scrape/sensitivity.py` use `autoconf.test_mode.with_test_mode_segment(Path("output"))` for both sqlite cleanup and scrape-directory selection. This matches PyAutoFit's `output/test_mode/...` search and database paths under `PYAUTO_TEST_MODE`, while preserving normal `output/...` behavior outside test mode. Verified both direct PyAutoBuild repro commands, the full `autofit_test scripts/database/scrape` PyAutoBuild directory run (5/5 passed), and PR CI on Python 3.12/3.13 before merge.
