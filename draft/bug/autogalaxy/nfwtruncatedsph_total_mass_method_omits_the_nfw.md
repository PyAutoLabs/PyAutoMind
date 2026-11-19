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
