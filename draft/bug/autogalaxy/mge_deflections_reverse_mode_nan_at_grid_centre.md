# Reverse-mode `jax.grad` of MGE deflections returns NaN when the profile centre lands exactly on a grid coordinate

Type: bug
Target: autogalaxy
Repos:
- @PyAutoGalaxy
- @autolens_profiling
Themes:
- jax
- mass-profiles
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Witness: `jax.grad` and `jax.jacfwd` of a gNFW (MGE-routed) deflection field w.r.t. `centre` agree and are finite at a pixel-aligned centre on the hst grid (`autolens_profiling/scripts/lens/deflections/` build), recorded in the JAX-audit section of `results/notes/numpy_deflections_cpu.md`.
Review-minutes: 10
Filed: 2026-09-03

> Found during the JAX Faddeeva / clamp audit (PyAutoGalaxy#600, phase A probe
> `autolens_profiling/scripts/misc/hazards/mge_faddeeva.py`). Unrelated to that task's two
> verdicts and pre-existing, so filed separately.

## Symptom

The hst grid contains exactly one point at r = 0 from a pixel-aligned centre. Whenever a
profile centre coincides with a grid coordinate, reverse-mode `jax.grad` of an MGE-routed
deflection (gNFW, MGE-30) returns **NaN**, while forward-mode `jax.jacfwd` returns a finite value
at the same point (143.15 at `centre_x = 0.05"` in the probe). The measure-zero r = 0 site is
reachable on any pixel-aligned centre — a sampler proposing such a centre gets a NaN gradient.

## Likely mechanism

A `where`/`abs`/`sqrt`-style construct in `zeta_from` (`ys = xp.abs(y)`, the `ind_pos_y` conjugate
select) or in the phase-B spherical branch (`alpha_r(0) = 0` via a guarded division) whose
reverse-mode cotangent multiplies an `inf` by a masked zero (the classic double-`where` trap,
see memory `feedback_jax_masking_and_aux_gradient_traps`). Forward-mode does not see it.

## Steps

1. Reproduce with the phase-A probe's transect at `centre_x = 0.05"` under `jax.grad` vs `jax.jacfwd`.
2. Locate the offending primitive with `jax.debug` / a per-term bisection of `zeta_from`.
3. Fix with the safe-`where` pattern (mask the *inputs* before the non-differentiable op, not
   the outputs), keeping the numpy path bit-identical (deflection pins rtol 1e-6, no re-pin).
4. Add the r = 0 site to the JAX validation run and the hazards check.

## Also record (documentation, same PR)

Finite-difference checking of JAX MGE gradients was unsafe below `h ≈ 1e-5` with the old
rational Faddeeva (a seam crossing between the ± evaluations made the FD estimate O(1) wrong at
that point). Phase B replaced the routine with a seam-free one; confirm the hazard is closed and
say so in the hazards README.
