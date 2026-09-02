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
