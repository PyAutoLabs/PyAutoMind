# Active Tasks

## reconstruction-row-split
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/243
- prompt: active/instrument_pixelized_reconstruction_row_nnls_cholesky_logdet.md
- issued: 2026-09-10
- session: claude --resume session_014MpFvj3ZeAHLBTYo2mkGRQ
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/reconstruction-row-split
- repos:
  - autolens_profiling: feature/reconstruction-row-split

## euclid-catalogue-rebuild-prep
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/60
- prompt: active/prepare_the_euclid_pipeline_for_an_ordered.md
- issued: 2026-09-09
- session: claude --resume session_01JsGeXEmGmSJzvxzC7GUpZo
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/61
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/68
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/euclid-catalogue-rebuild-prep
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-catalogue-build-and-parity
- delivery: one issue, two phased PRs — phase 1 (feature/euclid-pipeline-disk-and-mge-ordering) gates the euclid_dr1_prelim reruns; phase 2 (feature/euclid-catalogue-build-and-parity) gates the catalogue build

## witness-campaign
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/398
- issued: 2026-09-10
- prompt: active/witness_campaign.md
- session: claude --resume session_018ip88yepHJjM1VjjFMMmuP
- status: library-dev
- location: web-github (session clones, no task worktree; branch claude/witness-campaign-feature-h21cq4)
- worktree: n/a — web-github session clone (/home/user/PyAutoMind)
- repos:
  - PyAutoMind: claude/witness-campaign-feature-h21cq4
- summary: |
    Campaign, not a one-shot: ~6 passes of ~15 prompts over the 89 unwitnessed
    `Unattended: ready` drafts. Each pass proposes candidate witnesses for the
    human to accept/edit/strike, then writes three header fields per accepted
    prompt — `Witness:`, `Consequence:`, `Review-minutes:`. The three-field
    rewrite is load-bearing: 74 of the 89 already declare `Consequence: judge`
    (a cached derivation from intake's hygiene set), and the precedence rule
    lets that stale value beat the witness, so a witness written alone moves
    nothing. Baseline 2026-09-10, derived over the 110 ready prompts:
    5 notify / 12 glance / 93 judge; fully witnessed the same set grades
    28 notify / 74 glance / 8 judge.
    Pass 1 (`workspaces`, 15) SHIPPED 2026-09-10: 15 judge -> 7 notify /
    8 glance / 0 judge, 300 seed review-minutes -> 24. Backlog now 109 ready,
    36 witnessed, derived 12 notify / 19 glance / 78 judge.
    Next: `autoarray` (10), then autolens (9), autofit (8),
    autolens_workspace (6), autolens_profiling (5), tail pass (~26 singletons).
    Pass-by-pass counts are in the prompt's `## Campaign log`.

## remove-fits-dataset-plots-yaml
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/62
- prompt: active/remove_fits_dataset_from_remaining_plots_yaml_copies.md
- issued: 2026-09-10
- session: claude --resume session_01PLBfxi4vtBX9zogYAPHmLj
- status: awaiting-merge
- worktree: n/a (remote web session — branches pushed via the GitHub API, no local worktree claimed)
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/remove-fits-dataset-plots-yaml
  - autolens_assistant: feature/remove-fits-dataset-plots-yaml
  - autogalaxy_assistant: feature/remove-fits-dataset-plots-yaml
  - HowToLens: feature/remove-fits-dataset-plots-yaml
  - HowToGalaxy: feature/remove-fits-dataset-plots-yaml
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/63
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/124
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/24
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/80
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/74
- plan: Approved by user. Config-only parity hygiene; identical two-hunk patch in all five repos, one PR each.
- note: worktree_check_conflict flags euclid_strong_lens_modeling_pipeline as claimed by euclid-catalogue-rebuild-prep (PR #61). Waived by the user — that guard protects a local worktree this session does not use, and #61 does not touch config/visualize/plots.yaml.

## autolens-inference-birth
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/399
- issued: 2026-09-10
- prompt: active/autolens_inference_birth.md
- session: claude --resume session_01S3mSjckpJgKufHFTYVmjmC
- status: awaiting-merge — 6 PRs open; merge order Mind → Cortex → Heart → Brain → .github → autolens_inference; RAL clone verified
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/400
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/28
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/224
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/375
- library-pr: https://github.com/PyAutoLabs/.github/pull/9
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/1
- worktree: ~/Code/PyAutoLabs-wt/autolens-inference-birth
- parallel-claim: witness-campaign (PyAutoMind) — approved 2026-09-10 on plan approval; file sets disjoint (this task touches repos.yaml, ROUTING.md, epics.md; witness-campaign rewrites draft/ prompt headers). COMMIT DISCIPLINE: never git add -A in either worktree.
- repos:
  - PyAutoMind: feature/autolens-inference-birth
  - PyAutoCortex: feature/autolens-inference-birth
  - PyAutoHeart: feature/autolens-inference-birth
  - PyAutoBrain: feature/autolens-inference-birth
  - .github: feature/autolens-inference-birth
  - autolens_inference: feature/autolens-inference-birth (workspace-root clone, no worktree)
- summary: |
    Phase 1 of the autolens-inference epic: birth PyAutoLabs/autolens_inference (created
    on github.com 2026-09-10, public, empty) — workspace-root checkout, autolens_profiling
    skeleton with no searches tier and nothing inherited from the retired
    inference_programme, rows in repos.yaml / projects.yaml / Heart excluded /
    Brain clean_slate / org profile README, RAL clone + hpc/sync check. Plan on #399.
