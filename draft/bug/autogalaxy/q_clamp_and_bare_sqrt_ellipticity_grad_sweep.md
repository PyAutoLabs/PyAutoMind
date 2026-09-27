# Same-class q-clamp and bare-sqrt ellipticity gradient sites (follow-up to PyAutoGalaxy#631)

Type: bug
Target: @PyAutoGalaxy
Filed: 2026-09-27

#631 (PR #634) fixed jax.grad NaN at zero components in convert.py and removed the Isothermal q<=0.99999
clamp (series near q->1). The same classes remain elsewhere:

1. dPIE clamps: `MAX_ELLIP = 0.99999` in `dual_pseudo_isothermal_mass.py:362`, `:668`, `dual_pseudo_isothermal_potential.py:100` (zero radial gradient near the clamp edge).
2. Chameleon clamps: `axis_ratio if axis_ratio < 0.99999 else 0.99999` in `profiles/mass/stellar/chameleon.py:229`, `profiles/light/standard/chameleon.py:53` (Python branch, not JAX-traceable, zero gradient past the clamp).
3. MGE/Gaussian: `xp.where(axis_ratio < 0.9999, axis_ratio, 0.9999)` in `mass/abstract/mge.py:432`, `mass/stellar/gaussian.py:177` (documented Faddeeva-stability clamp, needs its own limit analysis).
4. Bare `sqrt(e0**2 + e1**2)` (NaN grad at ell_comps=0): `nfw.py:99,248,294`, `dual_pseudo_isothermal_mass.py:358,664`, `dual_pseudo_isothermal_potential.py:99`, `geometry_profiles.py:279` (`__model_constraint__`), `nfw_mcr_scatter.py:65` (NumPy only).
5. Pattern: `convert._nudge_off_origin` for the sqrt sites; a series near the limit for each clamp. Prove each with grad-vs-FD and a bit-identity check away from the limit; expect symmetric knife-edge pins to move (see PyAutoLens#754).
