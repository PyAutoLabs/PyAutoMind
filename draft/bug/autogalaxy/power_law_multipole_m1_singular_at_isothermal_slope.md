# PowerLawMultipole with m=1 returns -inf / NaN deflections at slope exactly 2 (isothermal)

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
Themes:
- mass-profiles
- jax
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: `ag.mp.PowerLawMultipole(m=1, slope=2.0, multipole_comps=(0.01, 0.0)).deflections_yx_2d_from(grid)` either returns finite deflections from the correct limiting form, or raises a clear exception at construction naming the m=1 / slope=2 degeneracy; a unit test pins whichever is chosen, for numpy and jax.
Filed: 2026-09-27
Updated: 2026-09-27

## Finding

Found building the phase-2c model ladder (autolens_profiling#331, source-plane point-source campaign):
an m=1 `PowerLawMultipole` with its slope tied to an isothermal lens (slope 2) gives `-inf` / NaN
deflections, so the ladder used a satellite shear instead. The power-law multipole deflection
appears to carry a denominator that vanishes when m = 3 − γ, which makes the m=1 term degenerate at
γ = 2 (isothermal, the most common slope). If so, this is a singular limit of the formula rather
than a numerical accident — confirm against the implementation.

## Fix direction

Decide between (a) implementing the m=1, γ=2 limiting form (finite, likely with a log term) or
(b) refusing m=1 at slope 2 with a clear error (and in the model, when slope is a free parameter,
documenting the singular point). Check the literature form used for the other m (see the
multipole docstring's reference) before choosing.
