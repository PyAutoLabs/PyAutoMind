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
Status: draft
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
