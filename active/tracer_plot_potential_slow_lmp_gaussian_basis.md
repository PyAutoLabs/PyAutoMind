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
