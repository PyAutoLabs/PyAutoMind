# NFWTruncatedSph: constructors from physical parameters and derived masses

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: unit tests in PyAutoGalaxy reproduce the project's `tests/test_tnfw.py` values to 1e-6 through the new constructors, and a halo built from (v_max, r_max) has its circular-velocity peak at r_max.
Review-minutes: 3
Unattended: ready
Lane: wsl-data

## Finding

`NFWTruncatedSph.from_m200_concentration` only builds a halo truncated at an overdensity radius. CDM
subhalo and line-of-sight populations need three things it cannot give: a truncation radius set in
kpc (Roche and tidal-track truncation), the (v_max, r_max) convention of O'Riordan et al., and the
derived masses every population table carries (M_max, bound or total truncated mass).

Source of truth: the `dm_sightlines` science project, `~/Science/Science/development/dm_sightlines` (local git, no remote; commit 845c5b3 or later). Its presets were frozen by the human on 2026-11-26 (`wiki/project/phase5_note.md` section 8). Port the validated code; do not redesign the physics.

The project holds these as plain functions in `sightlines/population/tnfw.py` (`lensing_parameters`,
`lensing_parameters_from_physical`, `m_max`, `total_mass`, `mass_ratio`, `tau_from_concentration`) and
the (v_max, r_max) conversion in `sightlines/population/subhalos.py`.

## What to build

- A constructor from (M200c, concentration, truncation radius in kpc, redshifts, cosmology).
- A constructor from (v_max, r_max, redshifts, cosmology), untruncated in the limit of large tau.
- Properties or methods for M_max, v_max, r_max and the total truncated (bound) mass.
- Cosmology passed in to the `mcr_util` mass-concentration helpers instead of hard-coded Planck15.
- Fix the docstring of `mass_at_200_solar_masses`: documented as M200m, returns M200c.

## Evidence it is validated

- `tests/test_tnfw.py`: tau and the mass ratio match the library solver to 1e-6; lensing parameters
  match `from_m200_concentration` where the two overlap; physical size is kept when the plane moves.
- `tests/test_subhalos.py`: v_max round trip, NFW from (v_max, r_max) peaks at r_max, Roche radius
  and total mass.

## Out of scope

A truncated gNFW with a free inner slope; tidal-track bound masses.

Witness: unit tests in PyAutoGalaxy reproduce the project's `tests/test_tnfw.py` values to 1e-6 through the new constructors, and a halo built from (v_max, r_max) has its circular-velocity peak at r_max.

<!-- formalised by the Intake (Conception) Agent on 2026-11-26 from file:/home/jammy/Science/Science/scratch/dm_sightlines_phase6_prompts/1_tnfw.md -->
