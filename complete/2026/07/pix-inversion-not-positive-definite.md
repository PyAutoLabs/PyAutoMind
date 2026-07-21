## pix-inversion-not-positive-definite
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/140
- completed: 2026-07-21
- workspace-pr: PyAutoLabs/autogalaxy_workspace#141 (MERGED), PyAutoLabs/HowToGalaxy#31 (MERGED)
- summary: |
    Pixelization/MGE inversion "matrix not positive definite / singular" NEEDS_FIX
    cluster — OUTCOME INVERTED: all 6 markers were STALE, NO code fix. Reproduction
    refuted the planned fix (opt scripts into log_det_method="slogdet"): the pix
    LinAlgError was fixed the same day the markers were filed (2026-04-10) by
    PyAutoArray GaussianKernel PD-guarantee f1817af0 (symmetrise + trace-scaled
    diagonal jitter on coeff*inv(gauss_cov)); the MGE manual np.linalg.solve now
    succeeds too. Evidence: 40-draw numpy inversion A/B across the full GaussianKernel
    LogUniform prior (coeff/scale 1e-6..~5e5) = 0 raises / 0 non-finite on BOTH
    cholesky (default) and slogdet; all 4 scripts GREEN end-to-end in the build-sweep
    mode that births the markers (PYAUTO_TEST_MODE=2, real data, SMALL_DATASETS unset).
    Shipped marker-only removal from config/build/no_run.yaml in both repos (3 markers
    each). Opened under the corrective-PR exception for Heart RED reason "58 stale
    parked script(s)"; merge human-authorized.
    Folded in (concurrent session): a mask_irregular no_run un-park rode along on both
    branches (Convolver.from_gaussian drift, fixed by PyAutoArray #360/#361; verified
    green) — autogalaxy_workspace + HowToGalaxy halves shipped here; autolens_workspace
    + HowToLens halves tracked under the separate mask_irregular_silent_failure prompt.
    Follow-ups / still distinct-and-open: Delaunay-pixelization-fit and SLaM
    FitException parked clusters (autolens_workspace/HowToLens) — NOT this cluster.

## Original prompt

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
