## gaussian-precompute-p1
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/601 (closed, completed)
- completed: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/602 (MERGED a647aa32f)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/214 (MERGED 5f7a3ab1d)
- epic: gaussian-deflections-precompute — phase 1 of 3, **epic stays open** (ledger
  draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md)
- shipped: a fixed-geometry deflection memo on the numpy path. **L1** caches the whole deflection
  field for a geometry that has not moved; **L2** caches the *unit-ratio* field, so `Gaussian`, `lmp`
  and `lmp_linear` rescale by their free mass-to-light ratio instead of recomputing the field —
  the whole point of the epic, since in an MGE fit the geometry is fixed and only the amplitudes are
  free. `GaussianGradient` takes L1 only (its ratio is not a plain scale factor). Keyed on a
  **content-keyed grid fingerprint** (sha256) — 936 µs cold, **0.55 µs cached** — with a byte cap of
  **256 MB**, the kill switch `AUTOGALAXY_DEFLECTIONS_MEMO=0`, and a `memo_disabled()` context
  manager. The hooks live at the `Galaxy` and `Basis` summation sites, not inside the profiles, so no
  profile learned about caching. New module `autogalaxy/profiles/mass/abstract/deflections_memo.py`.
- measured: Basis-30 deflections hst **135.6 → 6.3 ms (21.5x)**, euclid **33.6 → 2.5 ms (13.5x)**.
  A SLaM-shaped likelihood **0.583 → 0.195 s (3.0x)** and **bit-identical** — the memo returns the
  same field, not an approximation of it. The `_wofz` call-count witness reads **[60, 0, 0]** against
  the **[60, 60, 60]** controls, which is the proof that the speedup is the cache and not a faster
  kernel. L2 rescaling max relative error **2.4e-13**. test_autogalaxy **1176 passed**, 15 new tests.
- finding: the deflections driver's `tracer_s` column **silently became a hit-path timing** the moment
  the memo existed — it was reporting the cost of a cache lookup as the cost of the computation, and
  nothing failed. Caught and fixed by making `_driver.measure_profile` hold `memo_disabled()` for the
  duration of the measurement. Any future memo needs the same treatment in any harness that times the
  thing being memoised.
- trap: the grid fingerprint cost **9x the plan's estimate** (936 µs, not ~100 µs). At one fingerprint
  per call that would have eaten the win outright, which is why the design gained a weakref cache
  keyed on the grid object — the plan did not have one.
- close-out: autolens_profiling#214 could not merge as opened — it and #215
  (`jax-faddeeva-clamp-audit`, the parallel claim on the same two repos) **both append a section to
  `results/notes/numpy_deflections_cpu.md`**, and #215 merged first, leaving #214 `CONFLICTING`. This
  is the "second to merge rebases" case the parallel claim was granted under. Resolved by merging
  `origin/main` into the branch (`af7445e`) and keeping both sections — main's "JAX-path audit" and
  its updated numpy-deflections-cpu epic ledger first, then this branch's "Fixed-geometry deflection
  memo — phase 1" — verified verbatim against both sides; every other path in that merge was
  one-sided. #214's earlier `lint` failure (`ModuleNotFoundError: deflections_memo`) was never a real
  break: the profiling CI checks out the library `main`s, so it could only pass once #602 had merged.
- heart: RED at PR-open, human-acknowledged for PR-open only — release validation FAILED (stage
  integrate), PyAutoArray open PR 11d old. Neither touches this diff.
- session: local CLI; merged and closed out via /prm 2026-09-03. PyAutoGalaxy is pending-release.
- epic next: phase 2 — draft/feature/autogalaxy/gaussian_precompute_p2_jax_trace_time_constant.md
  (the JAX branch: make the memo a trace-time constant). Phase 3 is the downstream sweep,
  draft/feature/autogalaxy/gaussian_precompute_p3_downstream_sweep.md.
- affected-repos:
  - PyAutoGalaxy
  - autolens_profiling

## Original prompt

# Gaussian precompute phase 1: numpy deflection memo — fixed-geometry whole field, `mass_to_light_ratio` rescale

Type: feature
Epic: gaussian-deflections-precompute
Phase: 1
Target: autogalaxy
Repos:
- @PyAutoGalaxy
- @autolens_profiling
Themes:
- numba-cpu
- mass-profiles
- profiling
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: active
Filed: 2026-09-03
Issued: 2026-09-03
Parent: draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md

> Phase 1 of the `gaussian-deflections-precompute` epic — ledger
> `draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md`, which holds the user's
> verbatim idea, the baseline timings and the gates. Successor to the completed `numpy-deflections-cpu`
> epic (archived ledger `complete/archive/epics/numpy_deflections_cpu_speedup.md`), whose
> `scripts/lens/deflections/` cells this phase reports through. Numpy path only; JAX is phase 2.

## Goal

In the SLaM `mass_light_dark` stage every Gaussian of an MGE lens light is **fixed** — centre,
`ell_comps`, `sigma`, `intensity` come from the light-stage instance
(`autogalaxy/analysis/chaining_util.py:484-511`) — and the whole stack shares **one** free
`mass_to_light_ratio`. Yet every likelihood call re-evaluates each Gaussian's Faddeeva field
(`profiles/mass/stellar/gaussian.py:104-112`: `m2l * intensity * sigma * sqrt(2π/(1−q²)) * zeta_from(grid)`),
which is **exactly linear in `m2l`** with every other factor fixed; same shape for the MGE stack
(`profiles/mass/abstract/mge.py:341-347`). Memoise the fixed field once and rescale it.

## Steps

1. **New module `autogalaxy/profiles/mass/abstract/deflections_memo.py`** — private, no public API.
   Module-global dict, **byte-capped** (default 256 MB, FIFO eviction — *not* entry-capped: over-sampled
   grids are large), kill switch `AUTOGALAXY_DEFLECTIONS_MEMO=0`, and `memo_stats()` counters (hits,
   misses, evictions, bytes) for the witness. Shape follows the existing precedent
   `PyAutoArray/autoarray/inversion/inversion/imaging_numba/sparse.py:20-51` (`AUTOARRAY_NUMBA_OPERATED_MEMO`)
   and `nnls_memo.py`: `sha256` key, read-only stored arrays, failure modes are **misses, never stale hits**.
2. **Grid fingerprint** (no helper exists yet): `sha256` of `grid.array` bytes + `grid.shape` +
   `pixel_scales`. Content-keyed, because grid *identity* is not stable — `FitDataset.grids` rebuilds the
   grid every call via `subtracted_and_rotated_from`
   (`PyAutoArray/autoarray/fit/fit_dataset.py:186-212`), so `id(grid)` would miss every time. ~0.1 ms on
   the hst grid (15,361 points) against 7 ms (Gaussian) / 139 ms (gNFW MGE-30) per call. Free
   `grid_offset` / `grid_rotation_angle` change the bytes → miss, correct by construction.
3. **L1 — whole-field memo for a fully-fixed mass profile (any class).** Key = `sha256` of (profile class
   name, the profile's constructor-argument values as floats, grid fingerprint). Hit → return the stored
   (y,x) field re-wrapped for the incoming grid. Covers fixed dark-matter / total profiles in a fixed-lens
   stage too, not only Gaussians. Exact by construction — no arithmetic changes hands.
4. **L2 — Gaussian geometry/amplitude split.** For `mp.Gaussian` (and the `lmp` / `lmp_linear` Gaussian
   subclasses that inherit it) with `m2l` varying but geometry fixed: key on (centre, `ell_comps`, `sigma`,
   `intensity`, grid fingerprint); store the **unit-ratio field** (the `m2l = 1` deflections, computed once
   through the normal path); return `m2l × field`. `Basis.deflections_yx_2d_from`
   (`profiles/basis.py:226-251`) sums as today, so N Gaussians with one shared ratio become N multiply-adds.
   `GaussianGradient` (`m2l_base`, `m2l_gradient`) is **not** linear in one scalar → L1 only.
5. **Hook** in `MassProfile.deflections_yx_2d_from` (`profiles/mass/abstract/abstract.py`) at the level
   *above* `@transform` — the undecorated public entry (e.g. `stellar/gaussian.py:70`, which delegates to
   the `@to_vector_yx` / `@transform(rotate_back=True)`-decorated `deflections_2d_via_analytic_from`) — so
   the stored field is the final rotated-back field for the *untransformed* grid. `@transform` mutates
   grid-derived objects with an `is_transformed` flag
   (`PyAutoArray/autoarray/structures/decorators/transform.py:62-88`); hooking above it keeps the memo
   clear of that state.
6. **Numpy only in this phase**: the memo engages solely when `xp is np` **and** every key value is a
   Python/numpy scalar. Anything else falls through unchanged.
7. **autolens_profiling**: new cell `scripts/lens/deflections/basis.py` — a `Basis` of 30 fixed Gaussians
   with one shared ratio, hst + euclid, pinned per the existing `_driver.py` / `_profiles.py` contract.
   Add the **call-count witness** (a `_wofz` invocation counter across 3 consecutive evaluations: first
   call N, later calls 0) and a likelihood-level before/after on the existing numba imaging cell with a
   fixed-MGE lens light + free ratio (the SLaM shape). Record both in
   `results/notes/numpy_deflections_cpu.md` under a new section.

## Verification

- `test_autogalaxy` green (numpy-only, incl. the new memo tests); `ruff check` + `ruff format --check` clean.
- New unit tests: hit/miss on repeated values; `m2l` rescale exactness (rtol 1e-12); grid-content keying
  (the same coordinates in a fresh `Grid2D` **hits**, a shifted grid **misses**); kill switch; byte-cap
  eviction; `GaussianGradient` takes L1 only.
- `scripts/lens/deflections/{total,dark,stellar}.py` pins **unchanged** (rtol 1e-6, no re-pin — the memo
  returns the same arithmetic); new `basis.py` cell pinned, second-call time ≈ N multiply-adds.
- Witness: `_wofz` call counter 0 on evaluations 2+ with fixed geometry; non-zero every call when a geometry
  parameter varies (control) and with `AUTOGALAXY_DEFLECTIONS_MEMO=0` (kill-switch control).
- Likelihood pins on the numba imaging cells hold (hst rect 27661.910133665442); before/after time on the
  fixed-MGE-light + free-ratio fit recorded in the note.
- Memory bound: the memo never exceeds its byte cap in the profiling run (assert in the cell).

## Ship

Library-first: PyAutoGalaxy PR → autolens_profiling PR with the after-numbers, the new cell and the note.

## Out of scope

The JAX branch (phase 2); the downstream `test_autolens` / SLaM / workspace_test sweep (phase 3);
`convergence_2d_from` / `potential_2d_from`; any profile with a traced or free geometry parameter; new
public API beyond the private memo module and its env switch.
