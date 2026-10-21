
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
- decision 2026-10-17 (human, chat): A2744 rows use a labelled synthetic prior-median 191-component model (no Bergamini+23 best fit exists in the workspace); the independent oracle supplies ground truth; representativeness caveat stated in the note
- worktree: ~/Code/PyAutoLabs-wt/cluster-pointsolver-robust-settings
- repos:
  - autolens_profiling: feature/cluster-pointsolver-robust-settings

## cosmos-web-ring-notebook
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/160
- issued: 2026-10-20
- prompt: active/cosmos_web_ring_guided_walkthrough_p1_notebook.md
- session: Claude Code (Fable 5.1), laptop CLI; session ID unavailable
- status: workspace-shipped, awaiting-merge (7 commits incl. maintainer copy-edit; F150W/F444W; Explore The Model)
- prs:
  - autolens_assistant: https://github.com/PyAutoLabs/autolens_assistant/pull/161
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/161
- worktree: ~/Code/PyAutoLabs-wt/cosmos-web-ring-notebook
- heart-override: Heart RED override (development only) authorized by human 2026-10-20
- repos:
  - autolens_assistant: feature/cosmos-web-ring-notebook

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## point-source-image-overlay
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/779
- issued: 2026-10-21
- prompt: active/point_source_image_overlay.md
- session: Claude Code (Opus 5.5), laptop CLI
- status: workspace-shipped, awaiting-merge (judge tier → human /prm, library first)
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/780
- prs:
  - PyAutoLens: https://github.com/PyAutoLabs/PyAutoLens/pull/780
  - autolens_workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/591
  - autolens_visualization: https://github.com/PyAutoLabs/autolens_visualization/pull/6
- release-gate: PyAutoLens
- next: after viz PR #6 merges, re-render the PyAutoEyes board (step 9) so image_with_points.png appears; follow-up: critical curve renders as 4 disconnected arcs (pre-existing)
- classification: feature (PyAutoLens library → autolens_workspace → autolens_visualization → PyAutoEyes board re-render), Consequence judge, Autonomy human-required; plan approved in chat 2026-10-21; merge mode human /prm
- heart-override: Heart RED override (development only) authorized by human 2026-10-21
- worktree: ~/Code/PyAutoLabs-wt/point-source-image-overlay
- repos:
  - PyAutoLens: feature/point-source-image-overlay
  - autolens_workspace: feature/point-source-image-overlay
  - autolens_visualization: feature/point-source-image-overlay

## ci-timing-superseded-main-cancels
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/311
- issued: 2026-10-21
- prompt: active/heart_ci_timing_concurrency_cancels_as_kills.md
- session: Claude Code CLI (Opus 5.5); session 343c1fc1-4d32-42cc-a8f5-e26cf0332168
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/313
- validation: test_ci_timing 43 passed, full suite 1281 passed; scratch collector 8 → 2 hang events (2 kept: PR runs cancelled after PR close, no successor — separate decision)
- next: human /prm #313; then re-run heart/checks/ci_timing.sh + tick
- worktree: ~/Code/PyAutoLabs-wt/ci-timing-superseded-main-cancels
- heart-red-override: "Heart: RED — Release RED; monitoring RED · 14/100 · 464 unresolved (updated 23h ago)"; live human "Override and proceed" 2026-10-21 (health session, covering the three health-fix bugs incl. this one) — development shipping only (commit, push, PR); merge needs separate /prm with all checks green; no release; reasons verbatim on the issue
- repos:
  - PyAutoHeart: feature/ci-timing-superseded-main-cancels

## sparse-mapped-reconstructed-image
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/639
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/40 (@HRSAstro)
- prompt: active/sparse_mapped_reconstructed_image.md
- session: Claude Code (Fable 5.1), laptop CLI
- status: library-dev
- classification: feature (PyAutoArray library; PyAutoGalaxy verify-only), Consequence glance, Autonomy safe; plan approved in chat 2026-10-21; merge mode auto-merge on green if Witness passes
- worktree: ~/Code/PyAutoLabs-wt/sparse-mapped-reconstructed-image
- repos:
  - PyAutoArray: feature/sparse-mapped-reconstructed-image
