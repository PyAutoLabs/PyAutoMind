`NFWTruncatedSph.total_mass_solar_masses` (renamed from `mass_at_truncation_radius_solar_mass`, no alias since nothing called the old name) now divides by ln(1+c) - c/(1+c) and threads `xp`. It returns the BMO09 total mass, which matches the integrated convergence. The abstract dark-profile docstrings now say M200c / c200c / r200c. On main the old method read 0.958 / 1.489 / 1.835 x the integrated convergence for (M200, c) = (1e8, 5) / (1e9, 10) / (1e10, 15); it now reads 1 +/- 6e-7.

Witness: `pytest test_autogalaxy/profiles/mass/dark/test_nfw_truncated.py -k total_mass`, 3/3 passed (|total/integral - 1| = 1.2e-7, 3.3e-7, 6.1e-7); fails on main. mass/dark 250 passed; PyAutoLens full suite 1032 passed.

- adversary: CLEAN, from Fable 5.2 (author Opus 5.5), 2026-11-19. Its own scipy 2D integral and a 3D BMO density integral that touches no profile code agree to 1.000000000 on 15 configurations. Notes: MCR totals move a second time with PyAutoGalaxy#733; the method is not jit-able (pre-existing scipy fsolve); the PR removes the public method `mass_at_truncation_radius_solar_mass` with no alias.

Related, already filed: `draft/bug/autogalaxy/nfwtruncatedsph_convergence_loses_precision_near_scale_radius.md` (tNFW convergence loses precision within ~1e-6 of r = r_s, found while writing the witness).

Shipped in PyAutoGalaxy#735 (https://github.com/PyAutoLabs/PyAutoGalaxy/pull/735, merged 2026-11-19 by human /prm). Done by shift worker 2026-11-19-pm (76a27cc3).

## Original prompt

# NFWTruncatedSph total mass method omits the NFW mass factor

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: A unit test asserts that the total-mass method of `NFWTruncatedSph` agrees to 1e-4 with a numerical 2D integral of `convergence_2d_from` times the critical surface density for at least three (M200, concentration) pairs, and equals M200 times `mass_ratio_from_concentration_and_truncation_factor`.
Review-minutes: 3
Unattended: ready
Lane: any

## Finding

`@PyAutoGalaxy/autogalaxy/profiles/mass/dark/nfw_truncated.py`
`NFWTruncatedSph.mass_at_truncation_radius_solar_mass` returns

    mass_at_200 * tau^2 / (tau^2 + 1)^2 * ((tau^2 - 1) ln(tau) + tau pi - (tau^2 + 1))

The Baltz, Marshall and Oguri (2009) total mass is that bracket times the scale mass M0, and
M0 = M200 / [ln(1 + c) - c / (1 + c)]. The division by the NFW mass factor is missing. Measured on
PyAutoGalaxy `main` b9232172, 2026-11-19, the method reads 1.2 to 1.9 times too high across the
concentrations tested.

The static method `mass_ratio_from_concentration_and_truncation_factor` in the same class has the
correct ratio, and a numerical 2D integral of the convergence matches that correct total mass to
1e-5 for six halos.

Two further points on the same method: its name says "mass at truncation radius" but the formula
is the total mass integrated to infinity; and it uses `np.log` where the rest of the class threads
`xp`.

## Why it matters

Any mass budget or reported subhalo mass taken from this method is wrong by a
concentration-dependent factor. `LOSSampler` does not call it, so the negative mass sheets are
unaffected.

## Ask

1. Divide by ln(1 + c) - c / (1 + c), with c the profile's own concentration.
2. Name it for what it returns (total mass), keeping the old name as a thin alias if anything calls
   it; grep its callers first.
3. Thread `xp`.
4. Add the witness test.

Separately noticed, same file family: `mass_at_200_solar_masses` on the abstract dark profile is
documented as M200m and returns M200c. Fix the docstring in the same PR.

## Provenance

[from: research dm-sightlines-cdm] Check 6 of the verification run. Script and log:
`Science/scratch/dm_sightlines_research_2026-11-19/evidence/verify/check6_masssheet.py`, `check6.log`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-19 from file:/tmp/claude-1000/-home-jammy-Science/4c8e2ded-c0f1-44a2-878a-797321efeaa7/scratchpad/raw/b3.md -->
