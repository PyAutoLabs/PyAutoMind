
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

## likelihood-lifecycle-p0-brain
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/535
- issued: 2026-10-23
- prompt: active/likelihood_lifecycle_p0_brain.md
- epic: likelihood-lifecycle (phase 0, sub-issue 0E; ledger draft/research/autolens_profiling/likelihood_lifecycle_epic.md)
- session: Claude Code CLI (Fable 5.1 orchestrator, Opus worker)
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs-wt/likelihood-lifecycle-p0-brain
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/536
- classification: library (PyAutoBrain only; Feature Agent library workflow, direct)
- tier: judge — human /prm
- validation: live `pyauto-brain profiling campaign --json` byte-identical before/after (sha be73b898…, 22/23/4/17); pytest 1268 → 1282 (conductor 48→56, samplers 17→20, template 3 new); ruff unchanged; CI pytest 3.12/3.13 in progress at ship
- heart: YELLOW at ship (workspace manifest drift; PyAutoLens release validation stale) — unrelated
- authorization: human "I authorize you to go" 2026-10-23 — claim-guard override: PyAutoBrain also claimed by github-token-p2b-writers-app (#534); separate branches, different files; rebase if #534 lands first. Heart STALE at the door (continue).
- next: human /prm PyAutoBrain#536 (no workspace impact, Brain not in the published set → no pending-release); then 0B when the autolens_profiling starting-grid claim clears
- repos:
  - PyAutoBrain: feature/likelihood-lifecycle-p0-brain
