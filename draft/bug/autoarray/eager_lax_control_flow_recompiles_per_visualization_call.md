# Eager lax control flow recompiles on every fit_for_visualization call

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- jax-compile
- visualization
- pixelization
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Filed: 2026-11-26 (shift 2026-11-26-pm2, from autolens_workspace_test#375)

## Symptom

Since PyAutoFit#1297, `Analysis.fit_for_visualization` is an eager `fit_from` backed by
per-function JAX JIT caches. Diagnosing autolens_workspace_test#375 (2026-11-26, PyAutoArray
main) with `jax_log_compiles` showed that warm calls are cache hits *except* for a few eager
`lax` control-flow primitives. These recompile on every call because their cond/body closures
are rebuilt per call, and closed-over arrays become new jaxpr constants:

- rectangular source, positive-only solver: one `jit(while)` per call, ~0.20s of a ~0.48s warm
  call (`autoarray/util/jax_active_set.py` `active_set_search` `cond_fun`/`body_fun` capture
  `Q`, `q`, `permanent`; `autoarray/util/jax_nnls.py` `converged_check` captures `max_iter`).
- Delaunay source: `jit(pure_callback)` 0.009s, `jit(scan)` 0.073s and two `jit(while)` 0.19s +
  0.25s per call, ~0.5s of a ~0.9s warm call (`autoarray/inversion/mesh/interpolator/delaunay.py`
  walk `while_loop`, qhull `pure_callback`, plus the solver while).

Inside the jitted likelihood these are traced once and are harmless. They cost only on the
eager paths: quick-update visualization and any un-jitted `fit_from`.

## Scope

Make the eager calls hit the cache: hoist the closures to module-level functions with the
captured values carried in the loop state, or wrap the entry points in a module-level `jax.jit`
with static knobs. Check that the jitted likelihood's numerics and gradients are unchanged.
Measure the warm `fit_for_visualization` time before and after on the
`modeling_visualization_{rectangular,delaunay}_jit.py` probes.

reproduce before fixing: with `jax.config.update("jax_log_compiles", True)`, the second and later
`analysis.fit_for_visualization(instance)` calls on a rectangular or Delaunay pixelization
analysis log `Finished XLA compilation of jit(while)` (and `jit(scan)`/`jit(pure_callback)` for
Delaunay) on every call.
