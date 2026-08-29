# LensCalc NumPy Hessian step is too coarse for multi-plane tracers

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Themes:
- point-source
- jax-gradient
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

Issued: 2026-08-29
Filed: 2026-08-27

LensCalc's NumPy Hessian uses a hardcoded finite-difference step that is too coarse for
multi-plane configurations, returning magnifications that are wrong by >100% with flipped signs.

Found on 2026-08-27 while cross-checking the fix for PyAutoLens#480. It is a separate, pre-existing
bug: #480's fix is accurate, and this was found by the control arm of that check.

`LensCalc._hessian_via_richardson` (autogalaxy/operate/lens_calc.py) evaluates the Hessian by
central finite differences at a hardcoded `buffer=0.01` arcsec, Richardson-extrapolated at h and
h/2. That step is fixed regardless of the scale the deflection field actually varies on.

Measured, on the tracer from PyAutoLens#480 (lens z=0.5 Isothermal R_E=1.6; source z=1.0 with its
own Isothermal R_E=0.2; source z=2.0), magnification at the four image positions of the z=1.0
source, computed three ways:

  last plane (z=2.0)
    numpy Richardson FD   -0.00694  -0.00221   0.00139   0.00246
    jax exact autodiff     0.04508   0.01099  -0.08602  -0.01118
    ray-traced Jacobian    0.04508   0.01099  -0.08602  -0.01101

JAX autodiff (float64) and a Jacobian derived independently from `traced_grid_2d_list_from` agree
with each other; the NumPy path disagrees by 122% and has the WRONG SIGN on three of four points.
The ray-traced values are stable across step sizes h=1e-4 to 1e-7, so this is not noise in the
cross-check.

The same three-way comparison at the intermediate plane (z=1.0) agrees to 1.7e-08. So the failure
is configuration-dependent, not general: the map to z=1.0 involves only the smooth main lens, while
the map to z=2.0 additionally passes the compact z=1.0 deflector (R_E=0.2), whose deflection field
varies on scales where a 0.01 arcsec step is far too coarse.

Why it matters: the NumPy path is the default. `AbstractFitPoint.magnifications_at_positions` uses
it, so point-source flux fits and source-plane chi-squareds on multi-plane models with a compact
intermediate deflector are exposed, as is `PointSolver`'s magnification threshold. A sign flip on a
magnification is not a small error.

Scope to consider: scale the step to the local deflection scale rather than hardcoding it; or
error-estimate from the Richardson pair (the h vs h/2 difference already bounds the truncation
error and is currently discarded) and warn or refine when it is large; or make the JAX path
reachable from NumPy callers. A regression test should pin the multi-plane configuration above
against the ray-traced Jacobian, which is the independent oracle used to find this.

<!-- formalised by the Intake (Conception) Agent on 2026-08-27 from file:/tmp/claude-0/-home-user/73120990-acb3-5546-bddd-2d75b5a0c771/scratchpad/intake1.md -->
