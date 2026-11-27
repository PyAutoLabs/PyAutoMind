# Add a combined-profile "effective Einstein radius" defined by the mean-convergence criterion…

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: for a single IsothermalSph, Galaxy.einstein_radius_via_mean_convergence_from equals MassProfile.average_convergence_of_1_radius to 1e-6; for NFWSph + SersicSph it matches an independent scipy brentq on the summed enclosed mass.
Review-minutes: 3
Unattended: ready
Lane: any

Add a combined-profile "effective Einstein radius" defined by the mean-convergence criterion, as used in papers: "We calculated the effective θE by numerically solving for the angular radius within which the radial convergence profile of our NFW + Sérsic profile integrates to [a mean convergence of 1]". The source text was truncated, so confirm the criterion: mean enclosed convergence = 1, i.e. M_enc(<θE) = π θE^2 in angular units.

What exists already:
- MassProfile.average_convergence_of_1_radius (autogalaxy/profiles/mass/abstract/abstract.py:332) does this root solve, but only for a single profile.
- Galaxy.mass_angular_within_circle_from (autogalaxy/galaxy/galaxy.py:346) sums the enclosed mass over a galaxy's mass profiles, but nothing root-solves it.
- LensCalc.einstein_radius_from (operate/lens_calc.py:1314) uses the tangential critical curve area. That is a different definition and does not match the paper convention for NFW + Sérsic (stellar + dark) decompositions.
- mass_angular_within_circle_via_grid_from (operate/lens_calc.py:2186) integrates any object (Galaxy, Galaxies, Basis) on a grid, with a free centre.

Wanted:
- A Galaxy method (and Galaxies / Tracer in PyAutoLens), e.g. einstein_radius_via_mean_convergence_from, that root-solves mean enclosed convergence = 1 over the summed radial convergence of all mass profiles (NFW + Sérsic + MGE basis, etc.) about a chosen centre.
- Decide between quadrature (sum of per-profile radial integrals; spherical/circularised) and grid integration (works for Basis and elliptical profiles). Document the ellipticity convention.
- Unit tests: matches average_convergence_of_1_radius for a single isothermal profile; an NFW + Sérsic case against an independent scipy reference.
- Expose it on the PyAutoLens Tracer and mention it in the workspace mass-budget / Einstein-radius examples, contrasting it with the critical-curve definition.

<!-- formalised by the Intake (Conception) Agent on 2026-11-27 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/7dd31e85-edae-4f94-a1e8-3e150dd65259/scratchpad/intake.md -->
