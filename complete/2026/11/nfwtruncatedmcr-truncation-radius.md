`NFWTruncatedMCRLudlowSph`, `NFWTruncatedMCRScatterLudlowSph` and `NFWTruncatedMCRDuffySph` now truncate at 2 r200 in arcseconds (tau = 2c), not at 2 r200 in kpc read as arcseconds. At m200 = 1e9, z = 0.5 -> 1.0, Ludlow and Scatter (sigma = 0) tau went from 151.48 to 24.09 and Duffy from 116.13 to 18.47. The workspace subhalo simulators change deflection by 0.2% at 0.05", 1.3% at 1" and 4.5% at 3"; no subhalo dataset is committed.

Decision taken and accepted by the human at /prm (merged unchanged): the `mcr_util` helpers keep returning r200 in kpc (6 tests pin that contract) and the conversion happens in the truncated classes, not in the helpers as the issue plan said.

Witness: `pytest test_autogalaxy/profiles/mass/dark/ test_autogalaxy/test_priors_config.py`, 259 passed; new tests assert tau == 2c for all three classes at sigma = -1, 0, 1, and fail on main (151.48 vs 24.09).

- adversary: FINDINGS (PR description only), from Fable 5.2 (author Opus 5.5), 2026-11-19. Witness holds, with an independent astropy Planck15 recompute giving tau = 2c. The PR's workspace-impact list named `autolens_workspace_test` substructure/subhalo.py (which uses the untruncated `NFWMCRLudlowSph`); the real users are the three `autolens_workspace` subhalo simulators. Pre-existing on main, not this PR: Duffy and traced-redshift JAX tracing fail; Duffy docstring still says H0 = 70, tau = 2.0.

Shipped in PyAutoGalaxy#733 (https://github.com/PyAutoLabs/PyAutoGalaxy/pull/733, merged 2026-11-19 by human /prm). Done by shift worker 2026-11-19-pm (2bf4469f).

## Original prompt

# NFWTruncatedMCR truncation radius uses kpc as arcseconds

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- workspaces
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: A unit test builds `NFWTruncatedMCRLudlowSph(mass_at_200=1e9, redshift_object=0.5, redshift_source=1.0)` and asserts `tau == 2 * concentration` (24.08, not 151.48), and the same for `NFWTruncatedMCRDuffySph` and `NFWTruncatedMCRScatterLudlowSph`.
Review-minutes: 3
Unattended: ready
Verified: 2026-11-19 2ec0e361 (PyAutoGalaxy)
Lane: any

## Finding

`@PyAutoGalaxy/autogalaxy/profiles/mass/dark/nfw_truncated_mcr.py` and
`@PyAutoGalaxy/autogalaxy/profiles/mass/dark/nfw_truncated_mcr_scatter.py` pass
`truncation_radius=2.0 * radius_at_200` to `NFWTruncatedSph`. The `radius_at_200` returned by
`mcr_util.kappa_s_and_scale_radius_for_ludlow` and `kappa_s_and_scale_radius_for_duffy`
(`@PyAutoGalaxy/autogalaxy/profiles/mass/dark/mcr_util.py`) is in kpc. `NFWTruncatedSph` expects
`truncation_radius` in arcseconds and forms `tau = truncation_radius / scale_radius` with
`scale_radius` in arcseconds.

Measured on PyAutoGalaxy `main` b9232172, 2026-11-19, for `mass_at_200=1e9`, `redshift_object=0.5`,
`redshift_source=1.0`:

- Ludlow: concentration 12.04, 6.288 kpc per arcsecond, `tau = 151.48`. That is 2c times kpc per
  arcsecond; the intended value is 2c = 24.08. The truncation radius is 35.1 arcseconds, which is
  12.6 r200 and not 2 r200.
- Duffy: `tau = 116.13`, the same error.
- `NFWTruncatedSph.from_m200_concentration` is correct (`tau = 15.88` for truncation at r100).

Affected classes: `NFWTruncatedMCRLudlowSph`, `NFWTruncatedMCRScatterLudlowSph`,
`NFWTruncatedMCRDuffySph`.

## Why it matters

These profiles are effectively untruncated: the truncation sits far outside the region that lenses
anything. Their total mass and any mass-budget calculation built on it are wrong. `LOSSampler` does
not use these classes, so line-of-sight simulations are unaffected.

## Ask

1. Convert `radius_at_200` to arcseconds before forming the truncation radius (divide by kpc per
   arcsecond), or have the `mcr_util` helpers return it in arcseconds. Check the other callers of
   those helpers first (`cNFW` and `gNFW` variants take `radius_at_200` too).
2. Add the witness test.
3. This changes the lensing of the three classes. Grep the workspaces for their use and say in the
   PR whether any example or documented result depends on the old behaviour.

## Provenance

[from: research dm-sightlines-cdm] Check 7 of the verification run. Script and log:
`Science/scratch/dm_sightlines_research_2026-11-19/evidence/verify/check7_truncation_units.py`
and `check7.log`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-19 from file:/tmp/claude-1000/-home-jammy-Science/4c8e2ded-c0f1-44a2-878a-797321efeaa7/scratchpad/raw/b1.md -->
