- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/680
- completed: 2026-10-29
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/681
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/681
- summary: Merge 7efb52a. `lmp.Gaussian.potential_2d_from` (and GaussianGradient, every MGE stellar Basis) decomposed one Gaussian into 100 and was WRONG as well as slow (finite-difference gradient ≠ deflections, sign errors when elliptical). Now psi = ∫0^1 alpha(t r)·r dt over MGEDecomposer's 20-node Gauss-Legendre rule using the shared in-frame analytic deflection `_deflections_in_frame_from`. ∇psi = alpha to 1e-8, lap psi = 2 kappa; 40-member basis on 100x100 ~2.4 s (was >10 min stall in fit visualisation); JAX = NumPy to 5e-15.
- tests: 4 new in test_gaussian.py; full suite 1448 passed; CI green on f3cdf6ff (3.12, 3.13, nojax, docs).
- follow-up: draft/bug/autogalaxy/chameleon_potential_inconsistent_with_deflections.md (Chameleon potential ~60% inconsistent with deflections); euclid_dr1/twins/config visualisation overlay can be removed once #681 is in the RAL environment.

## Original prompt

# Fit visualisation stalls on the potential of an `lmp.Gaussian` basis (subplot_tracer, tracer.fits)

Type: feature
Target: autolens
Repos:
- PyAutoGalaxy
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: a FitImaging visualisation of a lens with a 40-member `lmp.Gaussian` stellar `Basis` (NumPy path) writes subplot_tracer and tracer.fits in under 10 s on the laptop, or the potential panel is skipped with a logged reason when it would exceed a budget
Filed: 2026-10-29
Issued: 2026-10-29
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/680

Seen in LensTwin phase 4 (euclid_dr1 twins): during `search.fit` visualisation, `subplot_tracer_from_fit` panel 5 and `fits_tracer` call `tracer.potential_2d_from`, which for a `Basis` of `lmp.Gaussian` goes through `autogalaxy/profiles/mass/abstract/mge.py` `potential_2d_via_mge_from` → `zeta_from` per member and grid point; a test-mode fit stalled > 10 min there (faulthandler trace). Workaround in the science project: `visualize/plots.yaml` `tracer: {subplot_tracer: false, fits_tracer: false}`. Options: a faster potential for elliptical Gaussians, a coarser grid for the potential panel, or skip the potential for MGE mass profiles. Affects any light-dark-mass SLaM fit with an MGE stellar basis.
