# CDM lens subhalo population sampler with the two frozen presets

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: PyAutoLens tests reproduce the project's expected subhalo counts for both presets to 1e-6 and a combined subhalo plus line-of-sight realisation renders through the chunked path and through `Tracer` to 1e-9 arcsec.
Review-minutes: 3
Unattended: ready
Lane: wsl-data

## Finding

PyAutoLens has no sampler for the subhalos of the lens galaxy. The only substructure population it
can draw is the line of sight.

Source of truth: the `dm_sightlines` science project, `~/Science/Science/development/dm_sightlines` (local git, no remote; commit 845c5b3 or later). Its presets were frozen by the human on 2026-11-26 (`wiki/project/phase5_note.md` section 8). Port the validated code; do not redesign the physics.

The project's `sightlines/population/subhalos.py` (`SubhaloConfig`, `SubhaloSampler`) draws lens
subhalos into the same realisation table as the line of sight, and `Realization.combined` merges
the two.

## What to build

- A subhalo sampler with composable choices (mass variable, concentration model, truncation,
  positions, compensating sheet) and the two presets exactly as frozen:
  - `cdm_fiducial`: infall M200c 10^6-10^10 M_sun, slope -1.9, f_sub = 0.016 inside 2 theta_E,
    Ludlow16 at the infall redshift with 0.15 dex scatter, Roche truncation (Gilman et al. 2020),
    cored-NFW positions, compensating negative sheet.
  - `ORiordan2025`: M_max 10^6-10^11 M_sun, slope -1.9, f_sub = 0.01 inside 2 theta_E, untruncated
    NFW in (v_max, r_max) from the Moline et al. 2022 redshift fit at the lens redshift, no scatter,
    uniform in the 2 theta_E disc, single plane, no sheet.
- The f_sub to sigma_sub converter, and `combined` realisations with the line-of-sight sampler.

## Evidence it is validated

- `tests/test_subhalos.py` (23 tests): analytic and Poisson counts, mass-function slope, infall
  redshift statistics, Roche radius and total mass, sheet against Monte Carlo, combined render
  against `Tracer`.
- O'Riordan preset: 958 subhalos inside 2 theta_E at theta_E = 1.6 arcsec, inside their published
  300-1,100.
- pyHalo 1.5.3 read and run: the infall-redshift model, structure at infall, normalisation form
  and Roche formula match (`results/phase5_pyhalo/NOTES.md`).

## Caveats to carry into the docstrings

- The surviving lensing signal of subhalos depends on the stripping model by a factor of about
  70 (Roche against pyHalo's tidal track). Open investigation:
  `draft/research/autolens/roche_against_pyhalo_tidal_track_subhalo_strippi.md`.
- The `ORiordan2025` M200c / M_max conversion is unresolved
  (`draft/research/autolens/o_riordan_m_max_to_virial_mass.md`) and the Moline fit is extrapolated
  below 6 km/s for M_max under about 10^6.8 M_sun.

## Out of scope

pyHalo's tidal-track stripping (the project calls pyHalo itself; not ported); tidal-track bound
masses; a truncated gNFW.

Depends on the NFWTruncatedSph constructors prompt and the line-of-sight sampler prompt (shared
realisation table).

Witness: PyAutoLens tests reproduce the project's expected subhalo counts for both presets to 1e-6 and a combined subhalo plus line-of-sight realisation renders through the chunked path and through `Tracer` to 1e-9 arcsec.

<!-- formalised by the Intake (Conception) Agent on 2026-11-26 from file:/home/jammy/Science/Science/scratch/dm_sightlines_phase6_prompts/4_subhalos.md -->
