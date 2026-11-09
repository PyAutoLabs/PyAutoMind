# Zero-contour critical curves: compile once per run by passing the mass model as a pytree

Type: refactor
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace_test
Themes:
- critical-curves
- visualization
- jax-compile
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: never
Lane: ral
Campaign: critical-curves
Blocked-by: human decision on whether zero-contour should draw interferometer/group figures (autolens_profiling#521 verdict, 2026-11-09)
Filed: 2026-11-06

Human request (verbatim, 2026-11-06): "file a draft prompt for the pytree caching fix"

## Problem

`zero_contour` critical curves and caustics recompile on every call during a modeling run, so they never reach JIT-warm cost.

- `LensCalc._make_eigen_fn` (`autogalaxy/operate/lens_calc.py`) wraps a closure over one tracer's `deflections_yx_scalar` in a `jax.tree_util.Partial` with no dynamic arguments. JAX keys the `ZeroSolver.zero_contour_finder` compile on that closure, so the mass-model parameters are compile-time constants. A new posterior sample means a new compile.
- `_zero_contour_cache` lives on one `LensCalc` instance. Production makes a fresh `LensCalc` per figure in `plot_utils._critical_curves_from`, and again in `_caustics_from`, so the cache never hits in a run. Critical curves and caustics compile separately even within one figure.

Evidence (autolens_profiling#521 pilot, laptop CPU fp64, imaging/hst phase-4 posterior draws): the production helper `_compute_critical_curve_lines` takes 21–38 s per figure with zero-contour against 1.2–1.4 s with marching squares. A repeat on the identical tracer still takes 23 s. Both engines match a 0.01″ reference to within 0.001″.

## Proposed change

- Make the eigenvalue function take the mass model (galaxies / tracer) as a **dynamic pytree argument** instead of capturing it. `Galaxies` is already a registered pytree (`autogalaxy/analysis/jax_pytrees.py`), which the jitted `fit_from` relies on. Check that `Tracer` and its fields (e.g. `MassField` shear) flatten too.
- Hold the compiled solver at module level, keyed on the model's static structure (pytree treedef: profile classes, galaxy count, plane redshifts) plus `(kind, pixel_scales, tol, max_newton, delta, N)`. A modeling run keeps one structure, so it compiles once per run per kind, and later figures are warm.
- Cover the automatic seed search (`_init_guess_from_coarse_grid`) the same way, if it is a recompile source.
- Bound the module cache (small LRU), so long sessions with many model structures do not grow memory without limit.

## Gate outcome (autolens_profiling#521, RAL 414456, 2026-11-09)

Warm zero-contour (0.2–0.8 s) only beats production marching squares where marching squares is slow:

| Scale | Marching squares | Zero-contour warm |
|---|---|---|
| interferometer/sma | 2.1–2.9 s | 0.18–0.37 s (about 8–12×) |
| group/euclid | 3.0–3.7 s | 0.84 s (about 4×) |
| HST imaging | 0.26–0.30 s | 0.30–0.58 s (no gain) |
| cluster | 0.11–0.13 s | 0.27–0.38 s (slower) |

**Caching alone is not enough to switch engines.** Before zero-contour can draw any modeling-run figure, three more things are needed, and they belong in this task if it goes ahead:

- **Seeds over the plotting field:** the automatic seed grid spans ±3″. Group curves (radius about 4.8″) are missed in 35 of 44 Delaunay/rectangular draws.
- **Duplicate removal:** interferometer fits trace the same curve 2–4 times.
- **Automatic fallback:** to marching squares, triggered by the coarse 0.2″ curve count plus a closure check. In #521 this flagged all 47 failures, with 2 false alarms in 150 draws.

Cluster stays on `point_sources.curves_for_planes`. The cheaper alternative lever, a smaller marching-squares grid around the lens for interferometer/group, is in scope for the visualization run-time campaign (`draft/research/autolens_profiling/visualization_run_time_campaign_measure_and_opti.md`). Pick one with the human before starting.

## Acceptance

- Curves are unchanged: the same components within 0.1″ against the #521 reference on its galaxy corpus, and the existing LensCalc zero-contour tests pass.
- Compile counts: two successive figures with different parameters but the same model structure trigger one compile (assert with a compile counter or `jax.log_compiles`), and the second call is warm.
- Gradients/`jacfwd` through `_f` still work. The existing zero-contour differentiability tests pass.
- Re-time with the #521 harness (`scripts/lens/critical_curves/modeling_viz_feasibility.py`): report figure cost, first and subsequent, against marching squares.
- No default change: `critical_curves_method` stays `marching_squares` unless a separate decision, informed by #521, flips it.
