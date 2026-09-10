# Active Tasks

## scientific-workflow-language
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1595
- issued: 2026-09-09
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/scientific-workflow-language
- repos:
  - PyAutoFit: feature/scientific-workflow-language
  - autofit_workspace: feature/scientific-workflow-language
  - HowToFit: feature/scientific-workflow-language
  - PyAutoHands: feature/scientific-workflow-language
- plan: Approved by user. Tutorial rewrite plus required fixes for live notebook display retention (PyAutoFit) and prose-only notebook generation (PyAutoHands); no API signature changes.
- progress: Implemented and locally validated; generated docs/notebooks updated. See active/scientific_workflow_language.md for validation and dependency details.

## retire-gpu1-mig-exclusion
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/220
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/222
- heart-ack: 2026-09-05 in-session, single reason "release validation FAILED (stage integrate)" — organism-scope (PyAutoHeart Release Integrate run 33951278577); nothing in this branch is in the release chain
- issued: 2026-09-05
- session: claude --resume session_0117cr7VQNhHL2HzkGwQCDun
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/retire-gpu1-mig-exclusion
- repos:
  - autolens_profiling: feature/retire-gpu1-mig-exclusion
- parallel-claim: autolens_profiling also claimed by delaunay-nn-breakdown (#219); "file sets disjoint (hpc/batch_gpu submits, hpc/README.md, activate.sh vs _profile_cli.py + scripts/imaging/likelihood_breakdown/delaunay.py); prompt out-of-scope note says merge order does not matter; own worktree taken under --auto safe"

## euclid-catalogue-rebuild-prep
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/60
- issued: 2026-09-09
- session: claude --resume session_01JsGeXEmGmSJzvxzC7GUpZo
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/61
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/euclid-catalogue-rebuild-prep
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-pipeline-disk-and-mge-ordering
- delivery: one issue, two phased PRs — phase 1 (feature/euclid-pipeline-disk-and-mge-ordering) gates the euclid_dr1_prelim reruns; phase 2 (feature/euclid-catalogue-build-and-parity) gates the catalogue build
