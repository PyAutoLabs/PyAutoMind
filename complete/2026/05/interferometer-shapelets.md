## interferometer-shapelets
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/170
- completed: 2026-05-17
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/171
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/79
- notes: Built scripts/interferometer/features/advanced/shapelets/ (autolens) and scripts/interferometer/features/shapelets/ (autogalaxy) — modeling.py + fit.py + README + __init__ in both. Polar `ShapeletPolar` linear basis with shared centre/ell_comps/beta; autolens places it on the source (no lens light), autogalaxy on the single-galaxy bulge. Both use TransformerNUFFT (nufftax) and crucially set `Settings(use_positive_only_solver=False)` — shapelets require the positive-negative solver because their decomposition relies on negative-amplitude cancellations. Both `fit.py` smoke runs reproduce this in action: 31/66 (autolens) and 30/66 (autogalaxy) shapelets land at negative intensity on the example dataset, exactly the unphysical-but-required behaviour the prose explains. Path note: imaging shapelets live at imaging/features/advanced/shapelets/ in autolens but at imaging/features/shapelets/ in autogalaxy — the interferometer mirror preserves this asymmetry. Tutorial role swap is NOT central here (unlike MGE) — imaging shapelets already places the basis on the source (`simple__no_lens_light` dataset), so the interferometer adaptation is closer to a straight port than the MGE one was. Phase 1 moderate-pad scope: typos (peforms, assymetric, central→centre, case-of→case-if, shapelet-fit→shapelets-fit, non-of, trailing-t URL fragment, Shaeplet, definedon, of-that-are-composed) + duplicated `__Model__` section in autolens + `ShapeletCartesianSph` → `ShapeletPolar` naming correction (imaging script's prose claimed `ShapeletCartesianSph` but the actual model uses `ShapeletPolar`) — bundled into PRs. Did NOT add new imaging likelihood_function.py / slam.py (out of scope; separate task if wanted). Did NOT fix a pre-existing Cartesian-shapelet model-build bug at modeling.py lines 510-517 (loop reassigns out-of-scope `shapelet` variable rather than iterating the af.Collection — flagged in the issue completion comment as a follow-up). Tracker now 4 shipped / 4 outstanding (extra_galaxies, double_einstein_ring, mass_stellar_dark, scaling_relation remain).

## Original prompt

The imaging shapelets example needs improving and padding out before adapting to interferometer.
Source paths differ between repos: `autolens_workspace/scripts/imaging/features/advanced/shapelets/`
and `autogalaxy_workspace/scripts/imaging/features/shapelets/`.

Once the imaging versions are more complete, adapt to interferometer in **both** repos at the
matching paths: `autolens_workspace/scripts/interferometer/features/advanced/shapelets/` and
`autogalaxy_workspace/scripts/interferometer/features/shapelets/`.

Shapelets are a polar / Gauss-Hermite basis for galaxy morphology that previously was prohibitively
slow against visibilities (each basis component needs its own Fourier transform per iteration).
With nufftax, the full shapelet basis can be transformed in batches on GPU, making this feature
practical for interferometer modeling. The script should explain the basis, the visibility-domain
fit, and credit nufftax for the performance shift.
