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
- plan: Approved by user. Tutorial/docs changes only; no library API changes. Brain's keyword-derived API phases do not apply to this scope.

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
- prompt: active/prepare_the_euclid_pipeline_for_an_ordered.md
- issued: 2026-09-09
- session: claude --resume session_01JsGeXEmGmSJzvxzC7GUpZo
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/61
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/euclid-catalogue-rebuild-prep
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-pipeline-disk-and-mge-ordering
- delivery: one issue, two phased PRs — phase 1 (feature/euclid-pipeline-disk-and-mge-ordering) gates the euclid_dr1_prelim reruns; phase 2 (feature/euclid-catalogue-build-and-parity) gates the catalogue build

## jax-import-order-x64
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/139
- issued: 2026-09-10
- prompt: active/jax_import_order_defeats_x64.md
- session: claude --resume session_01XMA4HZYcVEzayYaRmS2uHi
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/jax-import-order-x64
- repos:
  - autolens_workspace_developer: feature/jax-import-order-x64
- summary: |
    Launched with an explicit --auto; effective autonomy `supervised`
    (min of the prompt header and the `bug` work-type cap), so the ship
    checkpoint resolves to decide-and-flag and the run ends at PR-open.
    Scope corrected at the plan gate and human-approved: 48 offenders, not
    the 33 the prompt's line-number grep reported — 6 `jax_profiling/
    simulators/*` are already guarded, and 25 `searches_minimal/` scripts
    the grep could not see are. Fix is the repo's own guard idiom
    (`from autolens import jax_wrapper`) rather than an import reorder.
