
## howtofit-runtime-guidance
- issue: https://github.com/PyAutoLabs/HowToFit/issues/72
- issued: 2026-10-17
- prompt: active/tutorial_4_runtime_claim.md
- session: Codex Work; current chat
- location: /workspace/scratch/a05dd794807b/HowToFit
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/74
- head: 01fea776af72ff9a84e492fabce27f74423e8bb3
- validation: Script/notebook prose-only diff verified; notebook regeneration succeeded. CI smoke failed because BlackJAX is absent in the install epilogue; fixed in HowToFit#75. Re-run after #75 merges.
- heart: STALE; release validation source moved since rehearsal; no release readiness claimed.
- next: Review PR and required CI; human /prm required.
- authorization: Four linked HowToFit teaching tasks; human Go on 2026-10-17; stop at PR review. HowToFit members coordinated sequentially on separate branches.
- repos:
  - HowToFit: feature/howtofit-runtime-guidance

## howtofit-ep-shared-centre
- issue: https://github.com/PyAutoLabs/HowToFit/issues/73
- issued: 2026-10-17
- prompt: active/tutorial_5_ep_shared_centre_never_assigned.md
- session: Codex Work; current chat
- location: /workspace/scratch/a05dd794807b/HowToFit
- status: workspace-shipped, blocked-CI
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/75
- head: 297b3e9eb2b170329daa9fd871cd7c91e91e46d8
- validation: Real sampling passes; shared x3 centre; each dataset and regression factor updated 5/5 sweeps, zero stale. One rejected marginal projection, no convergence claim. All 19 smoke scripts passed across initial run and missing-BlackJAX retry; final EP guard passed. Notebook/catalogue regenerated.
- heart: STALE; release validation source moved since rehearsal; no release readiness claimed.
- next: Fix smoke_install.sh to install the declared Nautilus dependency, then revalidate Python 3.12/3.13 and rerun /prm. No merge or rerun on this red-CI pass.
- decision: Review the explicit FWHM_i ~ Normal(m*i+c, 5 pixels) teaching assumption and m/c priors before merging. Also installs BlackJAX for existing gradient smoke scripts; #74 depends on this CI prerequisite.
- authorization: Four linked HowToFit teaching tasks; human Go on 2026-10-17; stop at PR review. HowToFit members coordinated sequentially on separate branches.
- repos:
  - HowToFit: feature/howtofit-ep-shared-centre

- ci-blocker: HowToFit run 39055282617; both 3.12 and 3.13 fail tutorial_6_gradients.py because nautilus is absent. Logs captured in PR #75 comment. Navigator and Tutorials Complete pass.
## cluster-pointsolver-robust-settings
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/436
- issued: 2026-10-17
- prompt: active/cluster_pointsolver_robust_settings_p1.md
- session: Claude Code (Fable 5.1); https://claude.ai/code/session_01MJFczsaH2vYuhFWLneD7F5
- status: workspace-dev
- classification: research (autolens_profiling only; Pulse campaign cluster-pointsolver phase 1), Consequence judge, Autonomy supervised; plan approved in chat 2026-10-17; compute per-job human authorization; no laptop timing
- worktree: ~/Code/PyAutoLabs-wt/cluster-pointsolver-robust-settings
- repos:
  - autolens_profiling: feature/cluster-pointsolver-robust-settings


## smoke-preserve-tracked
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/302
- issued: 2026-10-17
- prompt: active/heart_smoke_runner_deletes_the_tracked_output.md
- session: Codex Work; current chat
- location: /workspace/scratch/949dc837bafc/heart-smoke
- status: workspace-shipped, awaiting-merge
- authorization: User requested four linked dashboard tasks on 2026-10-17; coordinated sequentially; stop at PR review.
- repos:
  - PyAutoHeart: feature/smoke-preserve-tracked

- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/306
- head: 76fde191cfd5199b367e85b7f3e0927cbe692d4c
- validation: 1,259 Heart tests passed; final clean-git fixture passed in 32 focused tests.
- ci: Heart Tests running on this head at last check 2026-10-17.
- heart: Published 2026-10-17T09:00:24Z STALE; release validation stale: source moved since rehearsal (PyAutoFit, PyAutoGalaxy, PyAutoLens).
- next: Human /prm after CI. Live weekly sweep unverified for workflow changes.

## result-provenance-guards
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/303
- issued: 2026-10-17
- prompt: active/release_integrate_analyze_path_filter_and_workspace_lint.md
- session: Codex Work; current chat
- location: /workspace/scratch/949dc837bafc/heart-results
- status: workspace-shipped, awaiting-merge
- authorization: User requested four linked dashboard tasks; coordinated sequentially by this session; stop at PR review.
- repos:
  - PyAutoHeart: feature/result-provenance-guards

- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/307
- head: 99a089fb2d5f7432042c50eb74ac7534626fc2e4
- validation: Full CI-environment suite: 1,265 pass and one local-fixture failure; fixture corrected, all 55 affected tests pass. Tenant firewall passes.
- ci: Heart Tests running on this head at last check 2026-10-17.
- heart: Published 2026-10-17T09:00:24Z STALE; release validation stale: source moved since rehearsal (PyAutoFit, PyAutoGalaxy, PyAutoLens).
- next: Human /prm after CI. Live weekly sweep unverified for workflow changes.

## unit-timing-robust-baseline
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/304
- issued: 2026-10-17
- prompt: active/unit_timing_regression_median_baseline.md
- session: Codex Work; current chat
- location: /workspace/scratch/949dc837bafc/heart-timing
- status: workspace-shipped, awaiting-merge
- authorization: User requested four linked dashboard tasks; coordinated sequentially by this session; stop at PR review.
- repos:
  - PyAutoHeart: feature/unit-timing-robust-baseline

- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/308
- head: 09e0284c55169f8786e2de475e32f52cf5026f57
- validation: 1,259 tests and tenant firewall pass. Oct16 replay clears NSS/3.12 EP false flags; synthetic isolated 4x slowdown remains red.
- ci: Heart Tests running on this head at last check 2026-10-17.
- heart: Published 2026-10-17T09:00:24Z STALE; release validation stale: source moved since rehearsal (PyAutoFit, PyAutoGalaxy, PyAutoLens).
- next: Human /prm after CI. Live weekly sweep unverified for workflow changes.

## euclid-smoke-release-gate
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/305
- issued: 2026-10-17
- prompt: active/euclid_pipeline_release_blocking_gate.md
- session: Codex Work; current chat
- location: /workspace/scratch/949dc837bafc/heart-euclid
- status: workspace-shipped, awaiting-merge
- authorization: User requested four linked dashboard tasks; coordinated sequentially by this session; stop at PR review.
- repos:
  - PyAutoHeart: feature/euclid-smoke-release-gate

- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/309
- head: 4891a53c5c8e787066e63b8021f3a7dde6a1aff9
- validation: 1,260 tests and tenant firewall pass; updated workflow test passes (21 tests). Main Euclid smoke prerequisite run37627512732 success.
- ci: Heart Tests running on this head at last check 2026-10-17.
- heart: Published 2026-10-17T09:00:24Z STALE; release validation stale: source moved since rehearsal (PyAutoFit, PyAutoGalaxy, PyAutoLens).
- next: Human /prm after CI. Live weekly sweep unverified for workflow changes.
