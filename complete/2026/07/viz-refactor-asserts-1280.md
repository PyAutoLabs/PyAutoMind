## viz-refactor-asserts-1280
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/187
- completed: 2026-07-21
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/190
- summary: Two visualization sweep-assert failures, both diagnosed as env-config (NOT code bugs); workspace-only, no library change. (1) imaging/visualization "dataset.png missing" = PYAUTO_FAST_PLOTS=1 short-circuits subplot_save() (PyAutoArray plot/utils.py:365 early-return); the env-override fix already landed on main (commit 0768310) so the script passes — only its stale no_run.yaml NEEDS_FIX marker remained (removed). (2) #1280 tangential-critical-curve family = NOT an algorithmic regression — curves recover everywhere (critical_curves_zero_contour small+full, imaging/visualization_jax 1 CC, cluster full-data 7 CC plane-1 / 1 CC plane-2). Only real blocker was cluster/visualization.py, wired into NEITHER config: same FAST_PLOTS PNG gap + required full-extent 250x250 viz_grid runs ~580s > 300s cap. Fix (3 parts): no_run.yaml drop imaging/visualization + add cluster/visualization SLOW; env_vars.yaml add cluster/visualization.py unset FAST_PLOTS+SMALL_DATASETS; refresh 8 stale "#1280/abd7b717 algorithmic regression" assert messages to a self-contained diagnostic (module docstrings left intact — accurate historical regression-guard context). GOTCHAS: PyAutoFit#1280 is a MERGED revert PR (use_jax_for_visualization→False), not an open blocker — the "#1280 family" script tags were stale self-references. Shipped past Heart RED (both reasons unrelated: PyAutoFit behind origin + PyAutoLens paper_jax/paper.md dirty) with human authorization. Concurrent PR#189 (jax-grad-env-vars-disable-jax) edits the same two config files — trial 3-way merge confirmed conflict-free; merged independently. FOLLOW-UP: the modeling_visualization_jit family stays no_run as SLOW (separate perf concern, not this bug); cluster/visualization's ~580s multi-plane critical-curve computation could be a future PyAutoGalaxy profiling target if smoke coverage is wanted.

## Original prompt

# Visualization-refactor asserts: dataset.png missing + tangential critical curve #1280 (parked)

Type: bug
Target: autolens
Repos:
- autolens_workspace_test
- PyAutoLens
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Two visualization/geometry assert failures the sweep surfaced:
- `imaging/visualization` — `AssertionError: dataset.png missing after visualization refactor`
  (autolens_workspace_test NEEDS_FIX): a subplot/output path renamed or dropped in a viz refactor.
- **#1280 tangential critical curve family** — the pre-tracked `zero_contour` / "no tangential
  critical curves recovered" asserts (self-documented "PyAutoFit #1280 family"), which also block
  cluster/visualization from fully passing.

First step: dataset.png is likely a quick assert/path update (check what the viz refactor renamed).
The #1280 family is the deeper one — confirm current status of PyAutoFit#1280 before investing;
the critical-curve recovery fails on small grids, so verify at full data first.
