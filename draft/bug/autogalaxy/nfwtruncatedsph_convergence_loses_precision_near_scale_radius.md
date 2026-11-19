# NFWTruncatedSph convergence loses precision near r = r_s

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: A unit test evaluates `NFWTruncatedSph.convergence_2d_from` at r/r_s = 1 ± 10^-k for k = 3 … 15 (and exactly 1) and asserts every value agrees with the value at r/r_s = 1 to 1e-6 relative in float64.
Review-minutes: 3
Unattended: ready
Lane: any

## Finding

`@PyAutoGalaxy/autogalaxy/profiles/mass/dark/nfw_truncated.py` `NFWTruncatedSph.coord_func_l`
uses `coord_func_g` from `@PyAutoGalaxy/autogalaxy/profiles/mass/dark/abstract.py`, which forms
g(x) = (1 − f(x)) / (x² − 1). Near x = r/r_s = 1 both numerator and denominator go to zero and the
subtraction cancels. Measured on PyAutoGalaxy `main` 2ec0e361, 2026-11-19, with kappa_s=0.1,
scale_radius=1, truncation_radius=5 (relative error against the value at exactly x = 1):

    |x-1| = 1e-5: 1.4e-5    1e-6: 2.7e-5    1e-7: 8.2e-3    1e-8: 0.32
    x = 1 ± 1e-15: convergence negative; x = 1 - 1e-12: 5.7e4 (garbage)

Found while writing the total-mass witness for PyAutoGalaxy#734: a log-spaced radial grid with a
node at x = 1 + 1.3e-15 made a 2D mass integral 4e-4 low. The same `coord_func_g` serves
`NFWSph` / gNFW; check whether they show it too.

## Why it matters

Any grid point within ~1e-6 r_s of a halo's scale radius gets a wrong convergence (and the
deflection's `coord_func_m` should be checked the same way). Rare for one halo, routine for
a line-of-sight population of thousands of halos on an oversampled grid.

## Ask

1. Replace g(x) near x = 1 by its Taylor series (g(1) = 1/3, g'(1) known) within |x − 1| < ~1e-3,
   for real and JAX inputs; keep the complex continuation the gNFW family uses.
2. Check `coord_func_m_from` (deflection) at the same radii.
3. Add the witness test.

## Provenance

[from: shift worker 2026-11-19-pm, task nfwtruncatedsph_total_mass_method_omits_the_nfw] found
while writing the PyAutoGalaxy#734 witness test.
