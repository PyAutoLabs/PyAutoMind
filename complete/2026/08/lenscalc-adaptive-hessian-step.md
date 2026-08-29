- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/591 (CLOSED)
- completed: 2026-08-29
- library-pr: PyAutoGalaxy#593 (merged 1b311c61 -> main, the fix), PyAutoLens#717 (merged -> main, test follow-up)
- repos: PyAutoGalaxy, PyAutoLens
- summary: `LensCalc._hessian_via_richardson` (autogalaxy/operate/lens_calc.py) no longer uses a hardcoded 0.01" step. It now forms successive Richardson estimates from (h, h/2) and (h/2, h/4), halves the step on the unconverged subset only (reusing the previous half-step evaluation), converges where `|R_{k+1} − R_k| <= atol + rtol·|R_{k+1}|` with rtol=1e-7 / atol=1e-8, stops at a roundoff floor (when the successive change starts GROWING while already < 1e-4 relative, keep the pre-growth estimate — no warning), caps at 20 halvings, and emits exactly one UserWarning per call for points that never converge (genuinely singular points, e.g. exactly on an isothermal centre, whose relative change is pinned at ~0.5). Public `hessian_from(grid, xp)` unchanged; JAX path untouched. Control (IsothermalSph R_E=0.2, points 3e-4"–1e-3" from centre): on main κ was 46.5 vs analytic 100–333 (54–86 % off) and shear ~100 % off; now κ 1.14e-9 / shear 7.57e-9 relative. #480 multi-plane fixture: NumPy Hessian now agrees with the ray-traced Jacobian / JAX autodiff to 3.4e-4 (the stored reference's precision) with no warning. Smooth fields: 3 FD evaluations (was 2), results move ≤ 6e-9 relative toward the analytic value; 50×50 grid 0.011 s. Tests: 3 new in test_autogalaxy/operate/test_deflections.py; PyAutoGalaxy 1152 passed; PyAutoLens: the strict xfail in test_multi_plane_cross_validation.py XPASSed and became a regression assert (renamed ..._agrees_at_the_last_plane); `theta_for_beta` in test_solved.py relaxed tol 1e-14 → 1e-12 (scipy status 3 "xtol too small" at residual 8e-17 with every physics assertion holding — a termination-path artefact); PyAutoLens 570 passed. CI green on every leg (Galaxy docs + unittest 3.12/3.13/nojax; Lens unittest 3.12/3.13/nojax).
- decisions: the first gate (`|H(h/2)−H(h)|/3`) bounds the O(h²) un-extrapolated value, not the O(h⁴) extrapolant, so it warned on exactly the target configurations — replaced by the successive-R gate. rtol=1e-8 was measured and REJECTED: the multi-plane (nested-trace) FD path has a roundoff floor of ~3.3e-8 at 14 halvings after which the change grows, so 1e-8 warned permanently and returned the over-refined k=20 value; the floor rule makes the returned value tolerance-independent at the floor (rtol 1e-7/1e-8/1e-10 all give 3.403e-4 vs ref, no warning).
- known loud cases: PyAutoLens tests test_operate.py::test__operate_lens__sums_individual_quantities (1 of 22201 grid points — the origin on a centred isothermal), test_fit_dataset.py::..._all_to_all_solved and test_fluxes.py::..._real_isothermal_tracer (1 of 2 positions on the lens centre) emit the designed singular-point warning. Not a regression; a position exactly on a mass-profile centre has no finite Hessian.
- follow-up filed: draft/docs/autolens_workspace/multi_plane_guide_richardson_warning_update.md (gated on the release carrying #593) — the guide's live "not fixed" section.
- heart-ack: shipped/merged under human-acknowledged YELLOW (2026-08-29) — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source".

## Original prompt

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
