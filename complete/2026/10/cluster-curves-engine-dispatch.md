## cluster-curves-engine-dispatch
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/807
- completed: 2026-10-28
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/808
- epic: cluster-strong-lensing (phase 3a subtask; ledger draft/feature/autolens/source_cluster_arc.md)
- summary: Cluster `plot_critical_curves` / `plot_caustics` (`autolens/cluster/plot/cluster_plots.py`)
  now read `general.critical_curves_method` once per call through PyAutoGalaxy's
  `autogalaxy.util.plot_utils._critical_curves_method()` (shared unknown-value and
  missing-`jax_zero_contour` fallbacks) and route each source plane's tangential/radial critical
  curves and caustics via `_CURVE_ROUTINES` / `_curve_list_from`: `marching_squares` (default,
  unchanged) → `*_list_from(grid=grid)`; `zero_contour` → `*_list_via_zero_contour_from()` with
  defaults, as the other plots do. Multi-plane LensCalc per plane, colours, labels, radial option
  and source-plane mapping preserved. No public API change (merge 1faa99a).
- tests: 6 new in test_autolens/cluster/plot/test_cluster_plots.py (two-source-plane PowerLaw
  fixture: per-plane routing for both engines, distinct plane geometry, default radial option,
  missing-dependency fallback with logged warning). Full suite 979 passed / 1 skipped / 1 xfailed;
  CI green on a0666e7. Workspace cluster visualisation smoke not run (autolens_workspace not in the
  remote session).
- traps: `zero_contour` takes no grid and seeds from `LensCalc._init_guess_from_coarse_grid`'s
  25×25 scan over ±3", so cluster-scale curves outside it are not drawn (silently `[]`) — remaining
  phase-3 scope. A real jax_zero_contour trace takes ~5–8 s per curve on the fixture, so tests stub
  it. `IsothermalCore` first call ~288 s (numba compile) — avoid in fixtures. The selector warns via
  `logging`, not `warnings` (use caplog). Test config lacks `critical_curves_method` (KeyError →
  marching_squares).
- notes: CORRECTION — the cluster epic ledger had marked this prompt DEFERRED (entangled with zero_contour seed-coverage robustness, separated by the human 2026-10-23; label stale, should be 3c); it was issued and merged without reading the ledger. Default behaviour unchanged; human ruled KEEP 2026-10-28 (see ledger). Feature Agent's top pick, chosen by the human as the next task 2026-10-28. Consequence:
  judge — merged on the human's /prm (freeze clear). Opus worker implementation; review, PR wording
  in the main session. Heart STALE, environment reasons only.

## Original prompt

# Cluster plots honor the configured critical-curve engine

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- cluster
- critical-curves
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-10-28
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/807
Consequence: judge
Epic: cluster-strong-lensing
Phase: 3a
Parent: complete/archive/epics/source_cluster_arc.md

## Original user request (verbatim)

> Continue the 'Cluster strong lensing — Source & Cluster arc' epic. Its canonical state lives in draft/feature/autolens/source_cluster_arc.md — read that ledger (and any DECISIONS/RESULTS files beside it) first. Cross-check this epic's entry in PyAutoMind/epics.md, any related rows in PyAutoMind/active.md, and the referenced repos' open issues and PRs, to work out the last completed phase and what is currently in flight. Then pick the next logical step and continue it through the normal workflow (/start_dev — filing the phase's prompt first if none exists), updating the ledger as the work advances. Note: 12 phased prompts under draft/; issue phases ONE at a time as predecessors near shipping — no bulk issue queues. Science half: the PyAutoCortex project ledger of the science project it births (arc phase 11).

## Bounded phase-3a task

Make `autolens/cluster/plot/cluster_plots.py` select the existing configured critical-curve engine for each source plane in `plot_critical_curves` and `plot_caustics`. Preserve `LensCalc.from_tracer(use_multi_plane=True, plane_j=j)` and per-plane colours, labels, radial option and source-plane mapping. The default remains `marching_squares`; explicit `zero_contour` uses the existing LensCalc zero-contour methods. Use PyAutoGalaxy's existing private method selector so config and missing-dependency fallback agree with other plots. Keep changes in PyAutoLens only.

Verify both configured engines on a two-source-plane cluster fixture, including tangential and radial curves and caustics. Tests must assert method routing and distinct per-plane geometry, not merely saved image paths. Check the configured-zero-contour behavior when the dependency is unavailable. Run focused PyAutoLens tests and appropriate workspace cluster visualization smoke. Do not claim JIT or gradient safety from a plotting test.

The umbrella phase-3 prompt is too large. On 2026-10-02, source inspection found the former twin `autogalaxy/plot/plot_utils.py` already removed; only `autogalaxy/util/plot_utils.py` remains. Its selector is still config-only, and cluster plots still call marching-squares methods directly. Context-aware JIT dispatch, docstring fixes, broad cluster-scale accuracy/performance and the former `jax_zero_contour` triage remain separate phase-3 scope after this task. File only this subphase now; no later issue queue.
