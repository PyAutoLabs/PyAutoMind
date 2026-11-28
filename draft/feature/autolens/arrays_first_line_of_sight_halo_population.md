# Arrays-first line-of-sight halo population sampler

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: a PyAutoLens test shows expected halo counts per plane within 1% and sheet values within 0.5% of the existing `LOSSampler` for the same configuration, and a 10^6 M_sun realisation on 99 planes samples in under 3 s.
Review-minutes: 25
Unattended: ready
Lane: wsl-data

## Finding

`LOSSampler` (`autolens/lens/los.py`) builds one `Galaxy` per halo, fits a single power law to the
mass function on each plane, places every halo at its plane centre, defaults to 4 + 4 planes and
hard-codes the cone narrowing behind the lens. It is a valid reference but too slow and too coarse
for populations below 10^7 M_sun.

Source of truth: the `dm_sightlines` science project, `~/Science/Science/development/dm_sightlines` (local git, no remote; commit 845c5b3 or later). Its presets were frozen by the human on 2026-11-26 (`wiki/project/phase5_note.md` section 8). Port the validated code; do not redesign the physics.

The project's population layer (`sightlines/population/los.py`, `mass_function.py`, `planes.py`,
`sheets.py`, `concentration.py`, `geometry.py`, `realization.py`) samples a realisation as arrays.

## What to build

- A sampler returning a realisation table (redshift, plane, position, mass, concentration,
  truncation radius, population tag, derived masses, per-plane negative sheets), with save and
  load, selection by mask, and a converter to `Galaxy` objects for small realisations.
- Mass function tabulated from colossus and sampled by inverse CDF, so a different mass function
  is a change of table.
- Planes of fixed redshift width, default 0.01, with halo redshifts continuous inside each slice.
- Cone radius and its narrowing behind the lens as parameters (default 5 arcsec, 1.0 arcsec;
  pyHalo's cone as an option).
- Concentration relation as a choice (default Ludlow16, 0.15 dex scatter); truncation at r100 by
  default with r50 as an option.
- Negative sheets computed once per configuration and cached, not per seed.
- Fix the `los_planes_from` docstring (it says equal comoving width; slices have equal redshift
  width) and remove the dead `light_cone_radius_at_z`.
- Decide in the plan step whether `LOSSampler` is replaced or kept as a thin wrapper.

## Evidence it is validated

- Against `LOSSampler`: counts within 1%, negative sheets within 0.2%
  (`results/phase1_los_population/`, `tests/test_los.py`).
- Against pyHalo 1.5.3: mass function within 1-2% below 10^8.5 M_sun where the cones coincide
  (`results/phase5_pyhalo/`).
- Plane spacing converged at 0.01 (`results/phase2b_convergence/REVIEW.md`); the 5 arcsec cone
  agrees with 8 arcsec after a macro refit (`results/phase4b_cone_refit/REVIEW.md`).
- After a full refit, Diemer-Joyce concentrations change the lensing signal by 5%, r50 truncation
  and pyHalo's cone by under 1% (`wiki/project/phase5_note.md` section 5.2).
- 50 ms per realisation at 10^6 M_sun on 99 planes.

## Out of scope

The two-halo term; warm dark matter and SIDM populations.

## Supersedes

The draft bug on `LOSSampler`'s default of 4 + 4 planes, retired on 2026-11-26 to
`complete/archive/shelved/lossampler_default_of_4_4_planes_is.md`. That file holds the measured
plane-spacing convergence table; the default of 0.01 asked for here is its fix.

Witness: a PyAutoLens test shows expected halo counts per plane within 1% and sheet values within 0.5% of the existing `LOSSampler` for the same configuration, and a 10^6 M_sun realisation on 99 planes samples in under 3 s.

<!-- formalised by the Intake (Conception) Agent on 2026-11-26 from file:/home/jammy/Science/Science/scratch/dm_sightlines_phase6_prompts/3_los.md -->
