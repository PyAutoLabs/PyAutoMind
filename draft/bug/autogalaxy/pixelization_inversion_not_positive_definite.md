# Pixelization/MGE inversion "matrix not positive definite / singular" (parked NEEDS_FIX)

Type: bug
Target: autogalaxy
Repos:
- PyAutoArray
- PyAutoGalaxy
- autogalaxy_workspace
- HowToGalaxy
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Parked-since-2026-04-10 cluster surfaced by the 2026-07-20 build sweep NEEDS_FIX banners.
`LinAlgError: matrix not positive definite` (and one "matrix singular") in pixelization/MGE
inversions — almost certainly ONE-TO-TWO root causes in the inversion/regularization
conditioning (PyAutoArray inversion), fanning across imaging + interferometer + MGE.

Affected scripts (remove each NEEDS_FIX marker from the repo's config/build/no_run.yaml once green):
- autogalaxy_workspace: `imaging/features/pixelization/modeling`, `interferometer/features/pixelization/modeling`, `interferometer/features/multi_gaussian_expansion/likelihood_function` (singular MGE inversion → InversionException)
- HowToGalaxy: `imaging/features/pixelization/modeling`, `interferometer/features/pixelization/modeling`, `chapter_4_pixelizations/tutorial_5_model_fit`

First step: reproduce ONE on clean `main` (e.g. autogalaxy_workspace/imaging/features/pixelization/modeling)
with real data (unset PYAUTO_SMALL_DATASETS) and localise whether it's regularization scale,
a non-PD regularization matrix, or ill-conditioned mapper. Likely related to the
[[project_pix_nan_localised_reg_logdet]] / slogdet lineage. Related but distinct parked clusters:
Delaunay-pixelization-fit and slam-advanced-fitexception.
