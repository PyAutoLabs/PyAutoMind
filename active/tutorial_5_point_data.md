# Tutorial 5 point-source data

Type: docs
Target: @HowToLens
Consequence: judge
Issue: https://github.com/PyAutoLabs/HowToLens/issues/109
Issued: 2026-10-31

## Overview
Add a brief Point Source Data section to Chapter 1 Tutorial 5 after Output. Connect Tutorial 4's predictions to observational datasets, including positions, fluxes, time delays and their uncertainties. Point readers to the workspace for detailed use.

## Approved plan
- Insert the reviewed narrative and `PointDataset` example in scripts/chapter_1_introduction/tutorial_5_data.py.
- Include illustrative fluxes/time delays, with uncertainties, as explicitly requested after review. Explain units, image ordering, dataset name, and example-vs-observed provenance briefly.
- Link to the point_source workspace entry point; retain interferometer guidance and add a weak-lensing workspace link alongside Chapter 4.
- Update overview, contents and wrap-up; regenerate notebook, executed Markdown and catalogue.
- Execute the complete tutorial and validate dataset arrays, notebook parity, links and full HowToLens smoke checks.

Repository: HowToLens, clean main base ebb5b43. Branch: feature/howtolens-point-data. Tier: judge — merge mode: human /prm.

## Original request and approval
"prm 108 if all checks are green and then go on to tutorial 5 where: add point data to tutorial_5_data.py explaining how point stuf fecomes a dataset brielfy"

"approve, apply the point source data section to tutorial 5 and run the checks. prm 108 if all checks are green now after pointing out the point dataset, point readers to point_source part of workspace for more use on them (which I assume interferometer and weak lensing examples do too?) but the block itself is good. Also include fluxes and time delays in the example dataset"

## Development authorization
Continuing the explicitly approved HowToLens development in this session; the human previously approved development on Heart RED and now explicitly approved applying and checking this follow-on section. Current recorded readiness reason: `release validation FAILED (stage integrate)`. Development only; no release or failed-check bypass. Merge requires human /prm after CI passes.


Checkpoint: approved section applied, including fluxes/time delays and workspace pointers; generating notebook/Markdown and validating.

## Applied and validated — 2026-10-31
- Added approved PointDataset section with positions, fluxes, delays and uncertainties; illustrative values labelled, units and order explained.
- Point-source workspace link added; interferometer pointer retained; weak workspace link added beside Chapter 4 reference.
- Notebook, executed Markdown/16 figures and catalogue regenerated.
- Official Heart smoke: 49 passed, 0 failed. Full notebook execution, dataset consistency, notebook parity, contents, figure references, navigator, 38 tutorial completion checks and whitespace checks pass.
- Commit: 9c06246c84807733072e0c6c66132a5f3baa7cdc
- PR: https://github.com/PyAutoLabs/HowToLens/pull/110
- Current exact Heart reason: `release validation FAILED (stage integrate)`; existing development-only approval applies, no release or failed-check bypass.
- Review copy: /mnt/c/Users/Jammy/Workspace/Science/scratch/howtolens_point_data_2026-10-31/tutorial_5_data.ipynb.
- Logs: scratch/tutorial5_dataset_check.log, scratch/tutorial5_render.log, scratch/tutorial5_heart_smoke.log.
- Next: human /prm after required GitHub checks pass. PR #108 merged and its worktree cleaned up; canonical HowToLens main fast-forwarded to ebb5b43.
