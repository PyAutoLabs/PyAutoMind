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
Status: draft
Consequence: judge
Campaign: critical-curves
Blocked-by: autolens_profiling#521 warm-floor result (see Gate)
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

## Gate (read before starting)

Do this only if autolens_profiling#521 shows the **warm** zero-contour call (`zero_contour_reused_calc_s.warm`) is clearly below production marching squares (~1.3 s per figure at galaxy scale). If warm zero-contour is still around a second, marching squares stays the default and this refactor has no payoff. Then retire this prompt with a pointer to the #521 verdict. The cluster seed-coverage gap (phase 3a: ±3″ automatic seeds miss cluster curves) is out of scope here. This fixes cost, not coverage.

## Acceptance

- Curves are unchanged: the same components within 0.1″ against the #521 reference on its galaxy corpus, and the existing LensCalc zero-contour tests pass.
- Compile counts: two successive figures with different parameters but the same model structure trigger one compile (assert with a compile counter or `jax.log_compiles`), and the second call is warm.
- Gradients/`jacfwd` through `_f` still work. The existing zero-contour differentiability tests pass.
- Re-time with the #521 harness (`scripts/lens/critical_curves/modeling_viz_feasibility.py`): report figure cost, first and subsequent, against marching squares.
- No default change: `critical_curves_method` stays `marching_squares` unless a separate decision, informed by #521, flips it.
