## numpy-deflections-p2
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/596 (closed, completed)
- completed: 2026-09-02
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/597 (MERGED 8d152b151)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/212 (MERGED 624774d1f)
- epic: numpy-deflections-cpu — phase 2 (ledger draft/feature/autogalaxy/numpy_deflections_cpu_speedup.md)
- shipped: PyAutoGalaxy — `MGEDecomposer.wofz` dispatches to `scipy.special.wofz` when `xp is np`; the hand-rolled
  rational Faddeeva lives on as `_wofz_rational` for JAX with coefficients hoisted to module tuples and
  Python-float accumulators (jitted gNFW deflections bit-identical, 0.0 max abs diff); `Gaussian.wofz =
  staticmethod(MGEDecomposer.wofz)` (was a byte-identical copy); `_wofz_masked` skips the second Faddeeva call
  where the Gaussian envelope underflowed (`|w| ≤ 1` for Im z ≥ 0, exact to < 1e-15; falls back to full
  evaluation when nothing underflows); `_spherical_mge_deflections_from` — numpy-only exact q→1 radial form
  `α_r = Σ_j 2 A_j σ_j² (1 − e^{−r²/2σ_j²}) / r` for MGE-routed profiles and `Gaussian` when the UNCLAMPED axis
  ratio is exactly 1; `amps, _ = decompose_convergence_via_mge(...)` where sigmas were discarded.
  autolens_profiling — `dark.py` / `stellar.py` re-pinned with provenance, `total.py` untouched, note
  "After phase 2" (mpmath adjudication, clamp-convergence, run-spread tables, re-scoped targets).
- measured: hst 15,361 pts, `OMP_NUM_THREADS=1`, three passes — gNFW 293 → 96 ms (2.4–3.1×), gNFWSph
  301 → 4.5 ms (58–67×), Gaussian 11.1 → 6.6 ms (1.7–1.8×), Gaussian(q=1) 12.9 → 2.1 ms (6–9×); euclid
  agrees. Against the prompt: gNFWSph beat 20×, Gaussian met 1.5×, gNFW short of 5× — the remainder is two
  genuine Faddeeva evaluations on 460,830 points. test_autogalaxy 1161 (2 new), test_autolens 576,
  scripts/misc/test 293; numba likelihood pins unchanged (hst 27661.910133664, euclid bit-identical).
- finding: the hand-rolled Faddeeva has max relative error 3.0e-6 vs mpmath (dps 40); scipy 1.3e-14 — the
  replaced routine was the inaccurate side, so the ≤ 4e-6 relative deflection shifts are corrections.
- finding: every spherical MGE-routed profile (gNFWSph, gNFWVirialMass*Sph, SersicCoreSph, Gaussian at q=1)
  was evaluated as elliptical at the q = 0.9999 clamp: ~6e-5 relative bias + spurious cross-axis deflections
  (hst sample −3.1e-8 → exactly 0). The elliptical path converges to the spherical form linearly in 1−q
  (6.4e-4 / 6.4e-6 / 6.4e-7 at q = 0.999 / 0.99999 / 0.999999). cNFWSph and dPIEPotentialSph are analytic,
  not MGE-routed — no unit-test literal moved.
- finding: elliptical Gaussian inputs sit in scipy's series regime (|z| ≲ 3.3), so the swap alone is ~1.07×;
  its 1.7× came from the mask + dedupe. `decompose_convergence_via_mge` is 0.34 ms/call — the prompt's
  cache lever was dropped on measurement.
- trap: gate the spherical branch on the UNCLAMPED geometry (`convert.axis_ratio_from(ell_comps)`), never on
  `self.axis_ratio()` which is already clamped; the branch is numpy-only (static under jit).
- trap: `staticmethod(MGEDecomposer.wofz)` is load-bearing in `Gaussian` — a bare assignment binds `self` as `z`.
- trap: `--repin` on a value that becomes exactly 0 reports a relative shift of 1.0 and needs `--repin-force`;
  read the refused diff first and force only the entries the mechanism explains.
- gate: Heart YELLOW (PyAutoArray open PR 10d; no release rehearsal) acknowledged on the active.md entry.
- epic next: phase 3 `draft/feature/autogalaxy/numpy_deflections_p3_closed_form_geometry.md`; JAX-path audit
  `draft/research/autogalaxy/jax_faddeeva_seams_and_spherical_clamp_audit.md`; successor
  `draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md` after the epic.
- affected-repos:
  - PyAutoGalaxy
  - autolens_profiling

## Original prompt

# Numpy deflections phase 2: MGE / Faddeeva — scipy wofz on numpy, spherical MGE branch, cached decomposition

Type: feature
Epic: numpy-deflections-cpu
Phase: 2
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
Priority: high
Status: active
Filed: 2026-09-02
Issued: 2026-09-02

> Phase 2 of the `numpy-deflections-cpu` epic — ledger
> `draft/feature/autogalaxy/numpy_deflections_cpu_speedup.md`, which holds the measured before-table,
> the goal, the request's constraints (no new public functions; keep the `xp` API single-bodied and
> split only where an `xp is np` branch buys a clear win) and the approved decisions 1–5. Phase 1
> (`draft/feature/autoarray/numpy_deflections_p1_sph_decorator_tracer.md`) is a hard predecessor: it
> lands the `scripts/lens/deflections/` cells this phase reports its before/after numbers through,
> and it removes the `*Sph` decorator cost that otherwise masks gNFWSph's MGE cost.

## Goal

The two MGE profiles are the slowest numerics in the epic: **gNFW 0.202 s/call**, **gNFWSph 0.830 s**
(of which ~0.5 s is the phase-1 decorator bug, the rest an elliptical MGE evaluated at `q = 0.9999`
for a spherical profile). The driver is MGE-30: `MGEDecomposer.wofz` on `(30, N)` complex128, three
branches × two calls, with the decomposition rebuilt on every call. Targets: **gNFW ≥ 5×,
gNFWSph ≥ 20× on top of phase 1, Gaussian ≥ 1.5×.**

## Steps

1. **`scipy.special.wofz` on the numpy branch.** `abstract/mge.py:80-168` + `stellar/gaussian.py:189-278`:
   when `xp is np`, call `scipy.special.wofz`. On JAX keep the hand-rolled routine, with its
   coefficient arrays hoisted to module constants and only the selected branch's inputs evaluated
   (today all three branches are evaluated in full and then `where`-selected).
2. **Remove the duplicate.** `Gaussian.wofz` is byte-identical to `MGEDecomposer.wofz` — point one at
   the other; do not keep two bodies. `test_gaussian.py:225,241` pin the hand-rolled branches: keep
   those tests, retargeted at the JAX-path routine.
3. **Spherical branch inside `_deflections_2d_via_mge_from`** when the axis ratio is 1: the real
   `(1 − exp(−r²/2σ²))/r` form, so `gNFWSph` stops paying a `q = 0.9999` complex Faddeeva.
4. **Cache `decompose_convergence_via_mge`** (parameters-only) on the profile instance — each
   evaluation calls it four times. Drop the discarded `sigmas` at `mge.py:202/215`.

## Verification

- Per-profile pins rtol 1e-6 from the phase-1 cells (`total.py`/`dark.py`/`stellar.py`, hst + euclid),
  before/after artifacts committed under `results/lens/deflections/`, README auto-table regenerated
  (`build_readme.py --check` is a lint gate).
- **Re-pin is expected here and only here** (epic decision 5): the hand-rolled `wofz` is the *less*
  accurate routine (~6 significant digits, 2.7e-6 abs vs `scipy.special.wofz`), so deflections may
  move up to ~3e-6 relative. Re-pin via `--repin --repin-reason` against an `mpmath` reference
  recorded in `results/notes/numpy_deflections_cpu.md`; shifts > `--repin-max-shift` (1e-3) still
  refuse without `--repin-force`, and `pin_provenance` is embedded in the JSON.
- Likelihood pins unchanged, rtol 1e-6: `pixelization_numba.py` / `delaunay_numba.py` hst + euclid —
  hst rectangular 27661.910133664103.
- `test_autogalaxy` numerical tests green, `test_gaussian.py` and `test_mge.py` in particular;
  `ruff check` + `ruff format --check`; lint smoke green.

## Ship

Library-first: PyAutoGalaxy PR → autolens_profiling PR with the after-numbers and the note update.

## Out of scope

The closed-form profiles and shared geometry (phase 3); the JAX path's speed; CSE (not on any of the
nine default deflection paths — NFW's CSE is opt-in); `convergence_2d_from` / `potential_2d_from`;
new mass profiles or public methods.
