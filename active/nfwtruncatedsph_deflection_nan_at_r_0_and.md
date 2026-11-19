# NFWTruncatedSph deflection NaN at r=0 and imprecise at small radius

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: A test evaluates `NFWTruncatedSph.radial_deflection_from` and `deflections_yx_2d_from` at r/r_s from 1e-10 to 1e-2 and at r = 0, under numpy float64, jax float64 and jax float32, and asserts every value is finite, is zero at r = 0, and agrees with a high-precision reference (mpmath or the small-radius series) to 1e-8 in float64 and 1e-4 in float32; `jax.grad` of the vmapped deflection is finite at r = 0.
Review-minutes: 3
Unattended: ready
Lane: any

## Finding

`@PyAutoGalaxy/autogalaxy/profiles/mass/dark/nfw_truncated.py`. The radial deflection is
`4 kappa_s r_s / eta * m(eta, tau)`, with `m` from `coord_func_m_from`, which subtracts large,
nearly equal terms at small `eta` and is then divided by `eta`.

Measured on PyAutoGalaxy `main` b9232172, 2026-11-19, for a 1e9 solar mass halo at z = 0.5:

- At exactly r = 0 the deflection is NaN, in the object path, in the vmapped path
  (`vmapped_deflections_from`) and under `jax.grad`.
- float64: relative error 9e-6 at r/r_s = 5e-6, 14% at 5e-8, and the wrong sign below about 5e-9.
- float32: still finite at 1e-3 arcseconds but already 0.85% off there, and zero or garbage below
  about 1e-4 arcseconds.

At ordinary radii the profile is right: it agrees with lenstronomy `TNFW` to 5e-9 in deflection and
2e-13 in convergence over 1e-3 to 10 arcseconds, and the JAX hook agrees with the object path to
1e-12.

## Why it matters

Harmless for a handful of halos. A line-of-sight population with a 1e6 solar mass lower limit has
about 10,000 halos whose scale radii are below a pixel, evaluated on an oversampled grid; grid
points land within 1e-3 arcseconds of halo centres routinely, and a GPU run in float32 would be
wrong there. A NaN from one halo sitting exactly on a grid point poisons the whole summed
deflection field and any gradient.

## Ask

1. Add a small-`eta` series for the deflection (as `potential_func_sph_from` in the same file
   already does for the potential) and switch to it with `xp.where`, keeping every branch finite
   for JAX tracing.
2. Return zero at r = 0.
3. Consider replacing the complex-arithmetic merge of the r < r_s and r > r_s branches with a
   real-valued form; it is the same change and is faster on GPU.
4. Add the witness test.

Related: `draft/feature/jax_substructure/6_deflection_equivalence_test.md`.

## Provenance

[from: research dm-sightlines-cdm] Check 8 of the verification run. Scripts and logs:
`Science/scratch/dm_sightlines_research_2026-11-19/evidence/verify/check8_tnfw_lenstronomy.py`,
`check8b_smallr.py`, `check8.log`, `check8b.log`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-19 from file:/tmp/claude-1000/-home-jammy-Science/4c8e2ded-c0f1-44a2-878a-797321efeaa7/scratchpad/raw/b5.md -->
