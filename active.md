# Active Tasks

## cron-delivery-headroom
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/396
- prompt: active/scheduled_runs_delivered_hours_late.md
- issued: 2026-09-09
- session: claude --resume session_01Qr64vy2ZcjjxaS7jSpH5eM
- status: library-dev
- worktree: /home/user-wt/cron-delivery-headroom
- repos:
  - PyAutoMind: feature/cron-delivery-headroom
  - PyAutoMemory: feature/cron-delivery-headroom
- bundle: ci-smoke (member 2 of 4; members 1 and 4 dropped as already shipped and retired to complete/)
- plan: Items 1-2 of the prompt's suggested shape only - measure, then offset the crons. Item 3 (a catch-up leg for the morning post) is a separate design and is out of scope. Under --auto safe; no plan-mode hold.

## smoke-relevance-gate
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/219
- prompt: active/smoke_relevance_gate.md
- issued: 2026-09-09
- session: claude --resume session_01Qr64vy2ZcjjxaS7jSpH5eM
- status: library-dev
- worktree: /home/user-wt/smoke-relevance-gate
- repos:
  - PyAutoHeart: feature/smoke-relevance-gate
- bundle: ci-smoke (member 3 of 4)
- plan: Tier 1 only - one more reason to skip in the existing `changes` job, fail-closed, pull_request-gated. Tier 2 (package-level narrowing) needs each workspace's vendored run_smoke.py and is deferred to its own prompt. Under --auto safe; no plan-mode hold.

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

## mge-jit-regression-rebaseline
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/137
- prompt: active/mge_jit_regression_rebaseline.md
- issued: 2026-09-09
- session: claude --resume session_01JFqrvTzZMs4sEJauxfcpRz
- status: workspace-dev
- worktree: /home/user/autolens_workspace_developer (remote web session; flat clone, no worktree root)
- bundle: mge (2 members; sibling markdown_regeneration_sigma_min dropped before issue — needs real fits and a warm output/, left in draft/)
- repos:
  - autolens_workspace_developer: feature/mge-jit-regression-rebaseline
- plan: |
    Re-measure, do not copy. The prompt's premise is obsolete: its 27542.08
    "drift" was refuted on 2026-05-16 by jit-regression-constant-drift
    (_developer#67) as an artefact of locally-modified HST FITS; clean main
    passed at 27379.388907. The live reason to re-measure is commit 9e0e351
    (2026-09-08) changing the lp over-sampling bins [4,2,1] -> [4,2,2] and
    leaving the constant un-re-measured by its own admission. Either outcome
    ships: re-pin if outside rtol=1e-4, or record "re-measured and confirmed"
    if within it. Both delete the misleading comment.

## howtolens-ch3-mask-overlay
- issue: https://github.com/PyAutoLabs/HowToLens/issues/78
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/79
- prompt: active/ch4_mask_overlay_never_drawn.md
- issued: 2026-09-09
- session: claude --resume session_0119sx8hEa8cDa8c2q55FtmM
- status: awaiting-merge
- worktree: /home/user/howtolens (remote web session — attached clone, not ~/Code/PyAutoLabs-wt)
- repos:
  - HowToLens: feature/howtolens-ch3-mask-overlay
- bundle: notebooks (auto bundle, 2026-09-09) — sole implementation member; multi_galaxy_package dropped (MAST unreachable from cloud), notebook_setup_notebook_drift_siblings retired as already-shipped
