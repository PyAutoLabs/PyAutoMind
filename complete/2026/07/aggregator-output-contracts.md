## aggregator-output-contracts
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1324
- completed: 2026-07-07
- library-pr: none; PyAutoFit PR https://github.com/PyAutoLabs/PyAutoFit/pull/1326 closed as unnecessary
- workspace-prs:
  - https://github.com/PyAutoLabs/autogalaxy_workspace/pull/122 (merged 3fcfc07)
  - https://github.com/PyAutoLabs/autolens_workspace/pull/229 (merged 512add1)
  - https://github.com/PyAutoLabs/autolens_workspace_test/pull/146 (merged 76982f6)
- repos: autogalaxy_workspace, autolens_workspace, autolens_workspace_test
- notes: Centralised Autogalaxy and Autolens results/workflow examples on `_quick_fit.py`, generating two release-mode fits in `output/results_folder` with full Nautilus samples, aggregator CSV/PNG/FITS artefacts, and latent summaries. Removed workspace-side test-mode path handling and kept user-facing scripts on plain `output/results_folder`; release smoke unsets `PYAUTO_TEST_MODE` for results guides instead. Fixed Autolens result FITS reload noise-map validation and the workspace-test convolution image directory. Verified fresh smoke after clearing `output`: autogalaxy_workspace 8/8, autolens_workspace 9/9, autolens_workspace_test 15/15.

## Original prompt

# Fix release aggregator and generated-output contracts

## Context

Seven release failures involve results that are absent, shorter than examples assume,
or written to a different location. Several pass in a stateful local checkout, so the
first task is a clean, directory-ordered reproduction. Primary owners are @PyAutoFit,
@autogalaxy_workspace, @autolens_workspace, and @autolens_workspace_test.

## Scripts

- `autogalaxy_workspace/scripts/guides/results/start_here.py`
- `autogalaxy_workspace/scripts/guides/results/aggregator/samples_via_aggregator.py`
- `autolens_workspace/scripts/guides/results/start_here.py`
- `autolens_workspace/scripts/guides/results/aggregator/galaxies_fits.py`
- `autolens_workspace/scripts/guides/results/aggregator/samples_via_aggregator.py`
- `autolens_workspace/scripts/guides/results/workflow/csv_make.py`
- `autolens_workspace_test/scripts/imaging/convolution.py`

## Required work

1. Run each parent directory in CI order from a clean output tree under the release
   profile, then rerun each script independently to document prerequisites.
2. Determine whether failures are library output/aggregator regressions, invalid script
   assumptions about sample counts, or missing directory creation for generated files.
3. Fix PyAutoFit when valid completed searches are not discoverable. Otherwise update
   scripts minimally while preserving their teaching narrative.
4. Ensure scripts create their own output directories and do not depend on unrelated
   earlier legs or developer-local artifacts.
5. Add the narrowest appropriate tests and rerun all seven release-profile scripts.
