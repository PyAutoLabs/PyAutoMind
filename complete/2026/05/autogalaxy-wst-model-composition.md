## autogalaxy-wst-model-composition
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/26
- completed: 2026-05-05
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/27
- repos: autogalaxy_workspace_test
- notes: Task 2/9 of the autogalaxy_workspace_test parity epic (#5). Ported `multi_galaxy_mge.py` from autolens_workspace_test, stripped to autogalaxy semantics (two galaxies sharing one plane, MGE light bases, no mass / shear / ray-tracing). Identifier regression anchor `a6eb928ed9a1fb92d0c18cf5443af4a6`. Required adding a `model_composition/` override to `config/build/env_vars.yaml` (mirrors the existing autolens override) because the `PYAUTO_SMALL_DATASETS=1` smoke default reduces `total_gaussians` inside `ag.model_util.mge_model_from`, collapsing `gaussian_per_basis=2` to 1 and breaking the structural prior_count assertions. Umbrella issue #5 also updated to tick tasks 4 and 5 (already shipped via PRs #17 and #19, checkboxes were stale).
