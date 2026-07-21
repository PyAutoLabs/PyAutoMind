## interpolator-aggregator-test-mode
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1401
- completed: 2026-07-21
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1402

Phase 1 of the workspaces API-drift umbrella (`draft/bug/workspaces/api_drift_callsite_fixes.md`, which stays in draft/ — 5 items remain).

**What shipped:** `Aggregator.from_directory` (`autofit/aggregator/aggregator.py`) is now test-mode-aware. Refactored the directory walk into a nested `scan()` helper; when `is_test_mode()` is active and the first scan yields zero search-outputs, it retries once against the `test_mode` sibling (`<dir>.parent / "test_mode" / <dir>.name`) if it exists. +2 tests in `test_autofit/aggregator/test_from_directory.py` (fallback fires under test mode; does NOT fire when off). Merged 2026-07-21.

**Root cause (reproduced on clean main):** `features/interpolate.py:213` (in-memory `LinearInterpolator`) always worked; the crash was at `interpolate.py:265`, the aggregator/DB section, and ONLY under test mode. Searches write results beneath an inserted `test_mode` segment (`output/test_mode/<prefix>`, via `_test_mode_segment()` in `non_linear/paths/abstract.py`), but `from_directory` walked the hardcoded real-run path (`output/<prefix>`) → 0 results → empty `LinearInterpolator` → `IndexError: no instances`. Real user runs were never affected.

**Traps / notes:**
- The umbrella prompt's framing was partly stale: HowToFit `tutorial_5_results_and_samples` was paired as "same family" but does NOT use the interpolator or aggregator — EXCLUDED. The NEEDS_FIX markers named in the prompt are no longer literally in the files (curated from an earlier triage sweep). `interpolate.py` is not in the smoke set (so CI never caught this; a full-script test-mode sweep did).
- Fix is behaviour-compatible: all 23 `from_directory` call-sites across the workspaces keep working; real-run behaviour byte-identical (gated by `is_test_mode()`). Workspace impact = (iii) NONE — `interpolate.py` fixed by the library alone, no script edit, notebook stays in sync. No `ship_workspace` follow-up.
- `--auto` run: Heart was RED solely on the unrelated `PyAutoLens/paper_jax/paper.md` WIP (recurring environmental RED); human-waived. Other 3 gate legs: tests 58/93, smoke n/a (validated directly), review CLEAN.

**Remaining umbrella items (open as follow-up tasks):** `ell_comps` kwargs KeyError (autogalaxy_workspace + HowToGalaxy), ellipse kwargs KeyError (HowToGalaxy ellipse/modeling), plotter `plot_grid_lines` kwarg drift (HowToGalaxy over_sampling), group/slam PriorException (autolens_workspace + HowToLens), `__hash__` non-int TypeError (autolens_workspace_test database/scrape).
