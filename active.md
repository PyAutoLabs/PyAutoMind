
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

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## cluster-pointsolver-starting-grid
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/439
- issued: 2026-10-23
- prompt: active/cluster_pointsolver_starting_grid_close_member_image.md
- epic: cluster-pointsolver-speed (ledger PyAutoPulse tasks/cluster_pointsolver_speed.md; Pulse PR #72 check-in)
- session: Claude Code CLI (Fable 5.1)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/cluster-pointsolver-starting-grid
- tier: judge — merge mode: human /prm
- authorization: plan approved by the human in chat 2026-10-23 ("go"); research only, no library/workspace edits; laptop CPU fp64 sweep OK, any RAL leg and any A2744 compute need explicit human authorization in chat.
- repos:
  - autolens_profiling: feature/cluster-pointsolver-starting-grid

## ep-evidence-nonfinite
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1713
- issued: 2026-10-23
- prompt: active/nan_in_ep_evidence_accumulation_invalid_value.md
- epic: graphical-ep (ledger PyAutoInsight tasks/ep_campaign.md + tasks/ep_campaign_state_2026-10-23.md)
- session: Claude Code CLI (Fable 5.1); session e889c72e
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/ep-evidence-nonfinite
- tier: glance — auto-merge on green if the Witness passes
- repos:
  - PyAutoFit: feature/ep-evidence-nonfinite
  - autofit_workspace_test: feature/ep-evidence-nonfinite

## github-token-p2b-writers-app
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/534
- issued: 2026-10-23
- prompt: active/github_token_phase2b_owner_wide_writers_app_token.md
- session: Claude Code CLI (Fable 5.1); session c837f591
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/github-token-p2b-writers-app
- authorization: human approved 2b as one task 2026-10-23 and pre-acknowledged Heart YELLOW (manifest drift on one workspace checkout; PyAutoLens release validation stale) for its ship; judge tier, human /prm
- repos:
  - PyAutoBrain: feature/github-token-p2b-writers-app
  - PyAutoGut: feature/github-token-p2b-writers-app
  - PyAutoMind: feature/github-token-p2b-writers-app
