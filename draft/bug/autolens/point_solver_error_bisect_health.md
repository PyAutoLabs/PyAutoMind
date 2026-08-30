# PointSolver error-behavior change: bisect the 2025-11→2026-05 candidates, then health-harden

Type: bug
Target: PyAutoLens
Repos:
- PyAutoArray
- PyAutoLens
- autolens_profiling
- PyAutoNerves
Themes:
- point-source
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: cluster-strong-lensing
Phase: 1
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# PointSolver error-behavior change: bisect the 2025-11→2026-05 candidates, then health-harden

Part of the Source & Cluster arc (phase 1 of 12). User request (verbatim): "Research
PointSolver change of error approx 3-9 months ago, where the input size or shape of
triangles was changed. See if it can find it in git history and investigate. Then do a
general health check on the PointSolver, make sure its JAX use and computation seems
correct."

Git archaeology already done (2026-08-19 session) — prime suspect confirmed against the
user's memory ("went from being related to triangle size … or some given input during
the solver to a new value"), plus three secondary candidates. The task is to A/B them
numerically, not re-find them:

1. **PRIME: magnification-filter Hessian step decoupled from triangle scale**
   (PyAutoLens 14826f6c7 "Refactor OperateDeflections from mixin to composition" +
   3db51dd38 "update to LensCalc API", 2026-03-02/04). Before:
   `_filter_low_magnification` called
   `tracer.magnification_2d_via_hessian_from(grid=points, buffer=self.scale)` — the
   finite-difference step WAS the solver's initial triangle scale (= solver grid pixel
   scale, e.g. 0.2"). After: routed through `ag.LensCalc.from_mass_obj(tracer)` with no
   buffer → hardcoded default `buffer=0.01`; then eacdcd77 (2026-04-18) Richardson-
   extrapolated the numpy path and the JAX path became exact jacfwd (no buffer at all).
   Net: the filter's μ near critical curves changed by up to the difference between a
   ~0.2"-smoothed FD and a near-exact local derivative — which images survive
   `|μ| > magnification_threshold` changed, and solver tests thereafter needed
   `magnification_threshold=1e-8` (was 0.1 default). Decide deliberately: is the exact
   local μ the RIGHT filter quantity, or was scale-matched smoothing physically
   intentional (a triangle-sized image region's average μ)? Document the decision.
2. **Nov 2025 arc** (PyAutoArray e0e2f28e/314e2d09 + PyAutoLens 0ea7c6000/c36f8a6ec/
   dd82ce386, 2025-11-03→18): single JAX fixed-size triangle implementation split into
   NumPy(dynamic)/JAX(padded); `solve()` went from a fixed 15-row inf-padded array to
   variable-length real images (`remove_infinities=True` default). e0e2f28e also deleted
   the module-level `jax_enable_x64` — triangles now rely on autonerves' env auto-enable.
3. **fca58c468** (2026-04-21): `max_containing_size` argument REMOVED from
   `for_grid`/`for_limits_and_scale` — the "maximum number of multiple images expected"
   input became hard-fixed `MAX_CONTAINING_SIZE=15` (history: 10 in Aug 2024 → 15 in the
   Jun 2025 JAX refactor 1094154c).
4. **d24339c37** (2026-05-24): `remove_infinities` default is path-dependent (True numpy,
   False JAX) — output shape differs by backend.

Method: fixed test problems (isothermal 4-image quad + the near_caustic preset from
autolens_profiling/scripts/misc/simulators/point_source.py), checkout each boundary sha,
compare solved positions / image counts / position errors across the four boundaries.
Report which change moved the error behavior; decide whether to restore a configurable
containing-size input (cluster lenses can exceed 15 candidate containing triangles —
silent truncation risk) or fix the value with a loud guard (no silent guards).

Health-hardening follow-ons from the audit, same branch:
- No unit test asserts multi-image positional accuracy against a known analytic
  configuration (only a trivial `abs=1e-1` check survives; the 15-vs-5 padded-count test
  died in PR #420). Add an isothermal-quad accuracy test with tight tolerances.
- `autoarray/structures/triangles/array.py:132,199` hard-code `dtype=jnp.float32` NaN
  placeholders — wrong dtype if x64 not enabled; verify + fix.
- ~~Absorb `draft/bug/autolens/point_jax_vmap_parity_nondeterministic.md`~~ — NO LONGER
  THIS TASK'S. Split out and shipped separately on 2026-08-23 as
  `point-source-dataset-cap-guard` (PyAutoLens#710). The parity failure was not a
  triangle-solve question at all: `should_simulate` deletes the committed JSON
  point-source dataset under `PYAUTO_SMALL_DATASETS=1`, so the script read degenerate
  data. `point.py` passes on current main. The short-circuit (now at
  `point_solver.py:119`, not `:111`) was confirmed to return a fixed model-independent
  pair and now emits a one-shot warning, so this epic no longer needs to carry it.

Blocks: every later phase of the arc (profiling, cluster source science, point
magnification) assumes a trusted PointSolver.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase01_point_solver_error_regression_bisect.md -->
