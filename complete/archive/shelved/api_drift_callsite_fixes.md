# Workspace API-drift call-site fixes (kwargs / Prior / interpolator / plotter) — RESOLVED 2026-07-21

Type: bug
Target: workspaces
Repos:
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
- autolens_workspace_test
- HowToGalaxy
- HowToLens
- HowToFit
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: RESOLVED — 1 real bug shipped, 5 stale (all verified on clean main). Nothing actionable remains.

## OUTCOME (full triage 2026-07-21)

Every item reproduced on clean `main`. Only ONE was a live bug; the other five were stale markers from
an earlier curated sweep (the umbrella had aged badly — some item paths were even wrong). Lesson logged:
always reproduce a curated NEEDS_FIX list on clean main before claiming worktrees.

- ~~**InstanceInterpolator IndexError**~~ — ✅ **REAL, SHIPPED (PyAutoFit#1402 merged, issue #1401 closed).** Root cause was NOT the interpolator: `features/interpolate.py:265` aggregator/DB section under test mode (searches write `output/test_mode/<prefix>`, `Aggregator.from_directory` read `output/<prefix>`). Fixed by making `from_directory` test-mode-aware. HowToFit `tutorial_5` was mis-paired (does NOT use interpolator/aggregator) — EXCLUDED. Completion record: `complete/2026/07/interpolator-aggregator-test-mode.md`.
- ~~**`ell_comps` kwargs KeyError**~~ — ✅ **STALE.** `autogalaxy_workspace/scripts/imaging/modeling.py` (path was "HowToGalaxy" — wrong) runs exit 0 under test mode, ell_comps prints fine in results.
- ~~**ellipse kwargs KeyError** `'ellipses.0.centre_0'`~~ — ✅ **STALE.** `autogalaxy_workspace/scripts/ellipse/modeling.py` (path was "HowToGalaxy" — wrong) runs exit 0, ellipse results print fine.
- ~~**plotter kwarg drift** `plot_grid_lines`~~ — ✅ **STALE.** `autogalaxy_workspace/scripts/guides/advanced/over_sampling.py` (path was "HowToGalaxy" — wrong) runs exit 0; the `plot_grid_lines` kwarg no longer exists in the script.
- ~~**group/slam PriorException** (upper<=lower)~~ — ✅ **STALE.** `autolens_workspace/scripts/group/slam.py` runs exit 0 under test mode (full SLaM pipeline, no PriorException).
- ~~**`__hash__` returns non-int TypeError**~~ — ✅ **STALE.** `autolens_workspace_test/scripts/database/scrape/general.py` as a REAL run (env_vars.yaml unsets PYAUTO_TEST_MODE for `database/scrape/`) → exit 0, subplot/FitImagingAgg clean. Fixed by PyAutoGalaxy#374 (`0dcea475`, pytree_token made ephemeral); marker predates it.

## Latent parallel (not a live bug, noted for later)
`general.py` under FORCED test mode dies at line 112 — the DATABASE `autofit.database.aggregator.Aggregator.add_directory` scrape isn't test-mode-aware (sibling of the #1402 fix). Not a live bug (that path is intentionally run real via env_vars.yaml). If ever wanted, mirror the #1402 fix into the SQLAlchemy aggregator's scrape — file as its own small prompt.

This prompt is retired to `complete/archive/shelved/` — no remaining work.
