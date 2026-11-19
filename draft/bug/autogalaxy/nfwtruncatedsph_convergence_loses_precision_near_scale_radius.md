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
Witness: A unit test evaluates `NFWTruncatedSph.convergence_2d_from` at r/r_s = 1 ± 10^-k for k = 3 … 15 (and exactly 1) and asserts every value agrees with the value at r/r_s = 1 to 1e-6 relative in float64; and the same for `deflections_yx_2d_from` / `radial_deflection_from` (float64 to 1e-10, jax float32 to 1e-4 relative against an mpmath reference), and `jax.grad` of the deflection at exactly r/r_s = 1 agrees with the mpmath derivative to 1e-6.
Review-minutes: 3
Unattended: ready
Verified: 2026-11-19 5b85fbf0 (PyAutoGalaxy)
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

## Deflection near r = r_s — adversary measurements (2026-11-19)

The independent adversary review (Fable 5.2) of PyAutoGalaxy#737 (shift 2026-11-19-pm, finding F1)
measured the same cancellation in the **deflection** closed form (`nfw_truncated.py:92-95`, the
x ≥ 0.5 branch #737 leaves unchanged), identical on main:

    float64: 4e-13 at x = 1.0004, 5.6e-11 at x = 0.999999
    float32: 2.5e-4 at x = 0.9999 / 1.0001, 1.9e-3 at x = 0.99995, 9.5e-2 at x = 0.999999
             (~0.2% of points in 0.5 ≤ x ≤ 5 exceed 1e-5)
    jax.grad at exactly x = 1: d/dr 0.2715 vs true 0.00747 — from the `x == 1` constant
             branch in `coord_func_f_from`

So a float32 GPU line-of-sight run is still up to ~10% wrong for grid points within ~1e-6 r_s of
a halo's scale radius. Ask step 2 now covers this: series-expand the deflection near x = 1 too,
for real and JAX float32 inputs, and give the x = 1 branch the correct derivative. Land after
PyAutoGalaxy#737 (it rewrites the x < 0.5 branch of the same function).

## Provenance

[from: shift worker 2026-11-19-pm, task nfwtruncatedsph_total_mass_method_omits_the_nfw] found
while writing the PyAutoGalaxy#734 witness test.
[from: independent adversary review, Fable 5.2, shift 2026-11-19-pm] deflection measurements on PyAutoGalaxy#737 (F1).
