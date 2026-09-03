# Numpy deflections phase 3: PowerLaw series with factor-driven term count, NFW/NFWSph masks, Isothermal hoists, rotation-matrix grid transform

Type: feature
Epic: numpy-deflections-cpu
Phase: 3
Target: autogalaxy
Repos:
- @PyAutoGalaxy
- @PyAutoArray
- @autolens_profiling
Themes:
- numba-cpu
- mass-profiles
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-09-02
Issued: 2026-09-03

> Phase 3 of the `numpy-deflections-cpu` epic — ledger
> `draft/feature/autogalaxy/numpy_deflections_cpu_speedup.md`, which holds the measured before-table,
> the goal, the request's constraints (no new public functions; keep the `xp` API single-bodied) and
> the approved decisions 1–5. Phase 1
> (`draft/feature/autoarray/numpy_deflections_p1_sph_decorator_tracer.md`) is a hard predecessor: it
> lands the `scripts/lens/deflections/` cells this phase reports through. Phase 2 touches disjoint
> files, so 2 and 3 may run in either order.

## Goal

The closed-form profiles and the geometry every profile pays: **PowerLaw 0.0074 s/call** (complex
`scipy.special.hyp2f1` ~35 %, `axis_ratio` re-derived 11×/call), **NFW 0.0024 s** (both `where`
branches evaluated in full), **Isothermal 0.0014 s** (`axis_ratio` re-derived ~8×/call, ~1 ms
grid-transform floor). Isothermal is the floor to measure the shared-geometry lever against.

## Steps

1. **PowerLaw** `total/power_law.py:86-153`: the numpy branch uses the `omega` recurrence
   (`jax_utils.omega`, Tessore & Metcalf eq. 29) that JAX already uses — 4–5× faster than the complex
   `hyp2f1` — with `n_terms` chosen from `factor` for rtol 1e-6. Hoist `axis_ratio`/`angle` to one
   call; form `z` from `hypot`; drop the in-place multiply on a complex view.

   **The term count must follow `factor`; a fixed count is not acceptable.** Convergence is geometric
   in `f = (1 − q)/(1 + q)`. Measured over slope 1.5–2.8 × q 0.3–0.99, worst cell:

   | n_terms | worst relative error |
   |---|---|
   | 20 | 2.9e-6 |
   | 30 | 4.6e-9 |

   A fixed count fails for **q ≲ 0.25**, which is already a recorded hazard,
   `component.power-law.series-vs-hyp2f1-divergence`; take the policy edges from
   `scripts/misc/hazards/power_law_omega.py:33-35`. Use a plain Python int for `n_terms` on the numpy
   branch. **The JAX default stays 20** unless separately decided — changing it moves every recorded
   JAX result.
2. **NFW / NFWSph** `dark/nfw.py`, `dark/nfw_hk24_util.py`, `dark/abstract.py:18-30`: evaluate each
   `where` branch on its own mask only; real-valued `coord_func_f_from` on the spherical path (today's
   `complex64` ones-array is a silent promotion for a real result).
3. **Isothermal**: hoist `axis_ratio` and `sqrt(1 − q²)` to one evaluation each.
4. **Shared geometry** `autoarray/geometry/geometry_util.py:489-531`
   (`transform_grid_2d_to_reference_frame`) and the inverse: build the rotation matrix from one
   scalar `cos`/`sin` of the angle instead of per-pixel `sqrt` + `arctan2` + `sin` + `cos`; count and
   cut the `Grid2D`/`VectorYX2D` re-wraps per call. Benefits every profile.
5. **Masked-branch `RuntimeWarning`s** removed by masking the inputs, not by wrapping in `errstate` —
   a fix to the branch, not a guard over it.

## Verification

- Per-profile pins rtol 1e-6 from the phase-1 cells, hst + euclid; before/after artifacts committed
  under `results/lens/deflections/`; README auto-table regenerated (`build_readme.py --check` is a
  lint gate). No re-pin is expected in this phase — the series is the *more* accurate routine; if a
  pin moves, that is a finding, not a re-pin.
- Series accuracy re-verified against `mpmath.hyp2f1` over the slope × q grid before shipping.
- Likelihood pins unchanged, rtol 1e-6: `pixelization_numba.py` / `delaunay_numba.py` hst + euclid —
  hst rectangular 27661.910133664103.
- `test_autogalaxy` numerical tests green: `test_power_law.py`, `test_isothermal.py`, `test_nfw.py`,
  `test_gnfw.py`, `test_transform_rotate_back.py`; `test_autoarray` green; `ruff check` +
  `ruff format --check`; lint smoke green.

## Ship

Library-first: PyAutoArray PR (geometry) → PyAutoGalaxy PR (profiles) → autolens_profiling PR with
the after-numbers and the note update.

## Out of scope

The MGE / Faddeeva kernel (phase 2); the JAX path's speed and its 20-term default; CSE (not on any of
the nine default deflection paths — NFW's CSE is opt-in); `convergence_2d_from` /
`potential_2d_from`; new mass profiles or public methods.
