## numpy-deflections-p3
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/598 (closed, completed)
- completed: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/519 (MERGED 62feb7eb2)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/599 (MERGED e5fb32f79)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/213 (MERGED d735d9506)
- epic: numpy-deflections-cpu — phase 3 of 3, epic COMPLETE (ledger draft/feature/autogalaxy/numpy_deflections_cpu_speedup.md)
- shipped: PyAutoArray — `transform_grid_2d_to_reference_frame` as a rotation matrix instead of the polar form
  (7× cheaper, 0.21 vs 1.42 ms on hst); `VectorYX2D` reuses the `Grid2D` it is handed, so a deflection call
  builds one `Grid2D` instead of two. PyAutoGalaxy — numpy branch of `PowerLaw.deflections_yx_2d_from`
  evaluates the Tessore & Metcalf (2015, eq. 29) omega series in Horner form with real coefficients instead
  of scipy's complex `hyp2f1`; term count from the second flattening `f = (1 − q)/(1 + q)` via the tail bound
  `f^N/(1 − f) ≤ 1e-10` (11 terms at q = 0.8, 39 at 0.3, 124 at 0.1, 254 at 0.05); verified vs `mpmath.hyp2f1`
  (40 digits) over slope 1.5–2.99 × q 0.05–0.99 to 5.7e-11 relative, so no `hyp2f1` fallback is kept; private
  helpers `_omega_n_terms_from` / `_omega_series_from`; `axis_ratio` derived once (was 11× per call). NFW —
  `capital_F_from` evaluates its arctanh / arctan branches on their own grid subsets on numpy (JAX keeps the
  `where` cascade); the HK24 deflection masks the centre point's inputs to the unit ellipse and zeroes it via
  the prefactor, so the three per-call `RuntimeWarning`s are gone without `errstate`. NFWSph —
  `coord_func_f_from` / `coord_func_g` evaluate each branch on domain-masked inputs and keep the input dtype
  (real arithmetic end to end; was `complex128` promoted from a `complex64` ones-array). Isothermal —
  `axis_ratio` and `sqrt(1 − q²)` hoisted to once per call (were ~8×). JAX branch and its 20-term default
  untouched. autolens_profiling — after-numbers hst + euclid, `stellar` re-pinned with provenance for the one
  on-axis sample the exact rotation makes 0.0 (was 4.8e-17), note "After phase 3".
- measured: same box, `OMP_NUM_THREADS=1`, hst 15,361 pts `Grid2D` call — PowerLaw 9.59 → 1.68 ms (5.7×),
  Isothermal 1.95 → 0.94 ms (2.1×), NFWSph 3.65 → 1.92 ms (1.9×), NFW 2.97 → 1.83 ms (1.6×), Gaussian q = 1
  1.75 → 0.89 ms (2.0×); euclid 4.3× / 1.7× / 1.6× / 1.6× / 2.0×. Field-level A/B vs `main` on the hst grid:
  ≤ 1.1e-8 relative for PowerLaw (the `hyp2f1` side's own accuracy), < 1e-9 for every other profile. Deflection
  pins held at rtol 1e-6 (`total` / `dark` unchanged); likelihood pin hst rect 27661.910133665442 held.
  test_autoarray 1349 passed, test_autogalaxy 1151 passed (1 skipped); the touched profile tests also run under
  `-W error::RuntimeWarning`.
- finding: the "rotate-back re-wrap" the prompt asked to cut never existed — `GridMaker.result` passes a bare
  array through unchanged; the second `Grid2D` per call was inside `VectorYX2D`, now cut.
- finding: NFW lands at 1.6×, under the epic's 2× line; the remaining cost is the HK24 polynomial arithmetic
  itself, not a mask or hoist — no further lever short of a different formulation.
- trap: a fixed 20-term omega series fails rtol 1e-6 below q ≈ 0.25 (hazard
  `component.power-law.series-vs-hyp2f1-divergence`); the term count must follow `factor`.
- trap: `--repin` on a value that becomes exactly 0 reports a relative shift of 1.0 — force only the entry the
  mechanism explains, with provenance.
- session: shipped from a web/mobile session (no local worktree or branches); merged and closed out via /prm
  from the CLI 2026-09-03. Both libraries are pending-release.
- epic next: epic complete. Follow-ups queued: JAX-path audit
  `draft/research/autogalaxy/jax_faddeeva_seams_and_spherical_clamp_audit.md`; successor
  `draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md`.
- affected-repos:
  - PyAutoArray
  - PyAutoGalaxy
  - autolens_profiling

## Original prompt

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
