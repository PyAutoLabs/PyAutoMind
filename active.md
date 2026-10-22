
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
- status: workspace-shipped, awaiting-merge (human /prm; Consequence judge → no tiered merge; decision 2026-10-22 (human, chat): DEFERRED — default stays 1.0″ until the starting-grid draft + A2744 pull; no default changed)
- classification: research (autolens_profiling only; Pulse campaign cluster-pointsolver phase 1), Consequence judge, Autonomy supervised; plan approved in chat 2026-10-17; compute per-job human authorization; no laptop timing
- decision 2026-10-17 (human, chat): A2744 rows use a labelled synthetic prior-median 191-component model (no Bergamini+23 best fit exists in the workspace); the independent oracle supplies ground truth; representativeness caveat stated in the note
- worktree: ~/Code/PyAutoLabs-wt/cluster-pointsolver-robust-settings
- repos:
  - autolens_profiling: feature/cluster-pointsolver-robust-settings
- prs:
  - autolens_profiling: https://github.com/PyAutoLabs/autolens_profiling/pull/438
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/438
- heart-ack: YELLOW 2026-10-22 (manifest drift 1 workspace checkout; release validation stale PyAutoArray) — unrelated to this repo; human to acknowledge at /prm
- follow-up: A2744 pilot leg job 412573 NOT pulled (RAL login unavailable 2026-10-22) — pull JSON/.out/memory trace + RSS attribution; no resubmission without human authorization
- follow-up: starting-grid question → draft/research/autolens_profiling/cluster_pointsolver_starting_grid_close_member_image.md; Pulse PR (campaigns.yaml, check-in, Knowledge block from the ledger appendix, board) after merge
- claim releases at /prm → planned.md `likelihood-lifecycle-p0-profiling` (queued behind this autolens_profiling claim) can start

## point-plots-yaml-keys
- issue: https://github.com/PyAutoLabs/HowToLens/issues/98
- issued: 2026-10-22
- prompt: active/point_plots_yaml_keys_howtolens_assistant.md
- session: Claude Code (Opus 5.5), laptop CLI
- status: workspace-shipped, awaiting-merge (human /prm; glance but no Witness: line → no tiered merge)
- classification: docs/config (workspace only), Consequence glance, Autonomy safe-capped; plan approved in chat 2026-10-22; library half PyAutoLens#794 MERGED
- worktree: ~/Code/PyAutoLabs-wt/point-plots-yaml-keys
- split 2026-10-22: autolens_assistant half blocked by cosmos-web-ring-notebook claim → planned.md `point-plots-yaml-keys-assistant`
- prs:
  - HowToLens: https://github.com/PyAutoLabs/HowToLens/pull/99
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/99
- heart-ack: YELLOW 2026-10-22 (manifest drift 1 workspace checkout; release validation stale PyAutoArray)
- repos:
  - HowToLens: feature/point-plots-yaml-keys

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
