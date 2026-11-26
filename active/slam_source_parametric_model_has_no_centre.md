# `subhalo/sensitivity/slam_source_parametric.py` fails: `'Model' object has no attribute 'centre'` in `base_model_narrow_priors_from`

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- subhalo
Difficulty: small
Autonomy: supervised
Priority: low
Status: active
Consequence: judge
Witness: `scripts/imaging/features/advanced/subhalo/sensitivity/slam_source_parametric.py` runs to completion in test mode (`MPLBACKEND=Agg PYAUTO_TEST_MODE=2`).
Review-minutes: 10
Unattended: no
Lane: any
Filed: 2026-11-25
Issued: 2026-11-26

## Context

Found by the 5F PR2 worker. It fails on unedited HEAD too, at line ~786 in `base_model_narrow_priors_from`, with `AttributeError: 'Model' object has no attribute 'centre'`. It is likely an API drift in how a model component is read (a Model vs an instance). The sibling `slam_source_pixelized.py` was fixed by `complete/2026/11/sensitivity-slam-source-pixelized-mappervalued.md` (autolens_workspace#694). That task also found three more defects in this script, which this task should fix the same way:

- The source bulge is an MGE `Basis` (`al.model_util.mge_model_from`), which has no `centre`. The script reads `bulge.centre` (lines ~379 and ~469 read `instance.galaxies.source.bulge.centre`; line ~786 reads the model's `bulge.centre`). This is the likely cause of the reported error.
- `perturb_model.mass.log10m_vir` (lines ~1025 and ~1053): `NFWMCRLudlowSph` takes `mass_at_200`. Use the human's answer on autolens_workspace#685: a fixed `mass_at_200 = 1e9` injection and `af.LogUniformPrior(lower_limit=1e6, upper_limit=1e12)` in `perturb_model_prior_func`.
- `analysis._adapt_images = self.adapt_images` in `BaseFit`/`PerturbFit` (lines ~632 and ~710) is dead. Pass `adapt_images=` to `AnalysisImaging` instead. Otherwise test mode hides every sensitivity fit's failure as a sentinel likelihood: check the log for "TEST MODE 2: likelihood verification raised FitException", not just the exit code. `sensitivity/start_here.py` has the same dead line, and the same stale "1e6 MSun and 1e13 MSun" docstring.

## Scope widened by the human (2026-11-26)

"fix those other bits too whilst we're here", followed by approval of the plan. This task also covers `scripts/imaging/features/advanced/subhalo/sensitivity/start_here.py`: its dead `analysis._adapt_images` line (pass `adapt_images=` to the `AnalysisImaging` constructor) and its stale "1e6 MSun and 1e13 MSun" docstring. The adapt-image construction block in both scripts stays untouched; adapt-mesh-weighting phase 3 (autolens_workspace#693) rewrites it.
