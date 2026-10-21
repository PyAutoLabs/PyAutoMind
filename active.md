
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
- status: workspace-dev
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/780
- classification: feature (PyAutoLens library → autolens_workspace → autolens_visualization → PyAutoEyes board re-render), Consequence judge, Autonomy human-required; plan approved in chat 2026-10-21; merge mode human /prm
- heart-override: Heart RED override (development only) authorized by human 2026-10-21
- worktree: ~/Code/PyAutoLabs-wt/point-source-image-overlay
- repos:
  - PyAutoLens: feature/point-source-image-overlay
  - autolens_workspace: feature/point-source-image-overlay
  - autolens_visualization: feature/point-source-image-overlay

## euclid-smoke-ordered-shard
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/317
- issued: 2026-10-21
- prompt: active/euclid_smoke_tools_shard_order.md
- session: Claude Code CLI (Opus 5.5); session 343c1fc1-4d32-42cc-a8f5-e26cf0332168
- status: library-shipped, awaiting-merge (merge Hands#318 BEFORE Heart#312)
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/318
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/312
- validation: Hands 534 passed, Heart 1277 passed; euclid ordered list 9/9 PASS locally via new path (diagnose_latent 5.8s); real Workspace Smoke dispatch only meaningful after Hands#318 merges
- next: human /prm Hands#318 then Heart#312; then dispatch Workspace Smoke; then start ci-timing-superseded-main-cancels (planned, blocked on PyAutoHeart)
- worktree: ~/Code/PyAutoLabs-wt/euclid-smoke-ordered-shard
- heart-red-override: "Heart: RED — Release RED; monitoring RED · 14/100 · 464 unresolved (updated 23h ago)"; live human "Override and proceed" 2026-10-21 (health session) — development shipping only (commit, push, PR); merge needs separate /prm with all checks green; no release; reasons verbatim on the issue
- repos:
  - PyAutoHands: feature/euclid-smoke-ordered-shard
  - PyAutoHeart: feature/euclid-smoke-ordered-shard

## matrix-zeus-smoke-install
- issue: https://github.com/PyAutoLabs/autofit_workspace/issues/172
- issued: 2026-10-21
- prompt: active/hands_matrix_zeus_missing_py313.md
- session: Claude Code CLI (Opus 5.5); session 343c1fc1-4d32-42cc-a8f5-e26cf0332168
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/173
- validation: zeus-mcmc 2.5.4 imports on 3.13.13/3.14.4; 3.13 venv per bootstrap: smoke_dependencies.py searches/mcmc.py (TEST_MODE=2) rc=0; Matrix dispatch only after merge (clones workspace main)
- next: human /prm #173, then dispatch Hands Python Version Matrix
- worktree: ~/Code/PyAutoLabs-wt/matrix-zeus-smoke-install
- heart-red-override: "Heart: RED — Release RED; monitoring RED · 14/100 · 464 unresolved (updated 23h ago)"; live human "Override and proceed" 2026-10-21 (health session) — development shipping only (commit, push, PR); merge needs separate /prm with all checks green; no release; reasons verbatim on the issue
- repos:
  - autofit_workspace: feature/matrix-zeus-smoke-install
