# LOSSampler default of 4 + 4 planes is too coarse; default… — SUPERSEDED 2026-11-26

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: `LOSSampler(z_lens=0.5, z_source=1.0)` with no plane arguments builds 99 planes of redshift width 0.01 (first and last 0.015) with the lens redshift as a plane centre; `los_planes_from` accepts a plane spacing and reproduces the existing (planes_before_lens, planes_after_lens) grids when those are passed instead; sampling one realisation with the default grid and a 1e7 solar mass lower limit takes under 10 s; and the per-plane negative sheets agree with the current `negative_kappa_from` values to 1e-3 relative on the (4, 4) grid.
Review-minutes: 20
Unattended: ready
Lane: any

## Superseded

Retired by the human on 2026-11-26, not shipped. Its fix (a default plane spacing of 0.01) is part of
`draft/feature/autolens/arrays_first_line_of_sight_halo_population.md`, the arrays-first line-of-sight
sampler promoted from the `dm_sightlines` science project. The measured convergence table below is
kept as that prompt's evidence.

## Finding

`@PyAutoLens/autolens/lens/los.py` `LOSSampler` defaults to `planes_before_lens=4, planes_after_lens=4`:
nine planes of redshift width 0.10 to 0.15 for z_lens = 0.5, z_source = 1.0. He et al. 2022
(arXiv 2010.13221), which the module follows, use a spacing of 0.01 and show in their Appendix A
that 0.05 can already matter. The default had never been tested.

Measured 2026-11-20 in the `dm_sightlines` science project with an independent sampler and ray
tracer that agree with `LOSSampler` (counts 1%, sheets 0.2%) and with the `Tracer` (1e-11 arcsec).
Sixteen realisations at a 1e7 solar mass lower limit and eight at 1e6, sampled with continuous halo
redshifts and re-binned onto coarser plane grids, compared with a spacing-0.002 reference (499
planes). Isothermal sphere lens, Einstein radius 1.5 arcsec, 0.05 arcsec pixels, peak S/N about 50.
Numbers are medians after removing the best-fit constant offset and linear term from the difference
in source-plane position (neither is observable); no macro model or source is refitted.

| plane spacing | planes | mean source-plane shift, 1 to 2 arcsec annulus | image delta chi-squared |
|---|---|---|---|
| 0.004 | 249 | 2e-5 arcsec | 0.07 to 0.14 |
| 0.01 | 99 | 4 to 5e-5 arcsec | 0.4 to 0.5 |
| 0.02 | 49 | 1e-4 arcsec | 2.0 to 2.4 |
| 0.05 | 19 | 2 to 3e-4 arcsec | 10 to 14 |
| 0.1 (the 4 + 4 default) | 9 | 4 to 6e-4 arcsec | 36 to 57 |

On the same measure the whole 1e6 to 1e7 solar mass decade of halos is worth 2.3e-4 arcsec and a
delta chi-squared of 10, and He et al.'s yardstick (0.1 dex above a 1e7 cutoff) 1.0e-4 arcsec and
2.0. So the default's plane error is four to six times the signal of the lowest mass decade, while
at a spacing of 0.01 it is 25 times below it in every realisation. The error is the same at both
lower mass limits: it comes from displacing the massive halos. The human ruled on 2026-11-20 that
0.01 is the default for the project.

## Why it matters

Every simulation made with the default settings carries a plane-discretisation error larger than
the low-mass signal the line-of-sight feature exists to simulate. Nothing reports it.

## Ask

1. Let `los_planes_from` and `LOSSampler` take a plane spacing (for example `plane_spacing=0.01`),
   choosing `round(z_lens / spacing) - 1` planes in front and `round((z_source - z_lens) / spacing) - 1`
   behind so the existing slicing formula and the lens-plane centre are unchanged. Make 0.01 the
   default. Keep `planes_before_lens` / `planes_after_lens` working when given explicitly.
2. This is not usable until the negative-sheet integral is fast: `negative_kappa_from` costs about
   4 to 6 s per plane (nested `scipy.integrate.quad` with an `fsolve` inside), so 99 planes would
   take minutes per realisation, although the result depends only on the configuration and not on
   the seed. Vectorise it (fixed quadrature over mass, Gauss-Hermite over the concentration
   scatter, a tabulated truncation ratio) and compute it once per sampler. The project's version
   does all 99 planes in about 1 s and matches the current values to 0.2%; see
   `Science/development/dm_sightlines/sightlines/population/sheets.py` for one way to do it. Do
   this first, in the same PR or one before it.
3. Update `@autolens_workspace/scripts/imaging/features/advanced/los_halos/simulator.py` and
   `simulator_jax.py` (they pass 4 and 4 explicitly) and say in the docstring what the spacing
   costs and why 0.01.
4. Fix the `los_planes_from` docstring, which says slices have equal comoving width; they have
   equal redshift width.

## Provenance

[from: dm_sightlines science project, phase 2B, 2026-11-20] Evidence, tables and figures:
`Science/development/dm_sightlines/results/phase2b_convergence/REVIEW.md`, `SUMMARY.md`,
`plane_spacing_dchi2.png`; script `scripts/phase2b_convergence.py`. Supersedes two `ideas.md`
bullets tagged `[from: research dm-sightlines-cdm]` (the negative-sheet integral and the plane
spacing default).

<!-- formalised by the Intake (Conception) Agent on 2026-11-20 from file:/tmp/claude-1000/-home-jammy-Science/4c8e2ded-c0f1-44a2-878a-797321efeaa7/scratchpad/raw/p_planes.md -->
