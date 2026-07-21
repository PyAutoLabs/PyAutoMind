# SLaM / advanced-pipeline FitException cascade (parked NEEDS_FIX)

Type: bug
Target: autolens
Repos:
- autolens_workspace
- HowToLens
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Parked cluster of `autofit.exc.FitException` in advanced pipelines (2026-07-20 sweep). The
double-einstein-ring note ("synthetic samples_summary lacks adapt_images") suggests a shared
SLaM adapt-image / samples-summary cascade; multi-wavelength may be separate.

Affected (remove NEEDS_FIX once green):
- autolens_workspace: `imaging/features/pixelization/slam`, `imaging/features/advanced/double_einstein_ring/slam`, `group/features/advanced/double_einstein_ring/slam`, `multi/features/wavelength_dependence/modeling`
- HowToLens: `imaging/features/pixelization/slam`, `multi/features/wavelength_dependence/modeling`

First step: reproduce autolens_workspace/imaging/features/advanced/double_einstein_ring/slam on clean
main; confirm whether the FitException is the synthetic-samples adapt_images gap (fixable in the SLaM
pipeline / samples_summary construction) or downstream of the pixelization-inversion-not-PD cluster.
Split into two prompts if multi-wavelength proves unrelated.
