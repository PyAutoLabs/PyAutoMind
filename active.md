# Active Tasks

## reconstruction-row-split
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/243
- prompt: active/instrument_pixelized_reconstruction_row_nnls_cholesky_logdet.md
- issued: 2026-09-10
- session: claude --resume session_014MpFvj3ZeAHLBTYo2mkGRQ
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/244
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/reconstruction-row-split
- repos:
  - autolens_profiling: feature/reconstruction-row-split

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
- note: worktree_check_conflict flagged euclid_strong_lens_modeling_pipeline as claimed by euclid-catalogue-rebuild-prep (PR #61). Waived by the user — that guard protects a local worktree this session does not use, and #61 does not touch config/visualize/plots.yaml. The conflicting claim was released on 2026-09-10 when euclid-catalogue-rebuild-prep closed out (PRs #61 + #68 merged), so the guard no longer fires.

## scrap-inference-programme
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/245
- issued: 2026-09-10
- prompt: active/scrap_inference_programme.md
- session: claude --resume session_01S3mSjckpJgKufHFTYVmjmC
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/scrap-inference-programme
- parallel-claim: reconstruction-row-split (autolens_profiling) — approved 2026-09-10 on plan approval; file sets disjoint (this task deletes the searches tier, results/searches, baselines, notes, search submits and edits build_readme/workflows/wall/docs; #243 edits likelihood_breakdown scripts and recon_split submits). COMMIT DISCIPLINE: never git add -A in either worktree.
- repos:
  - autolens_profiling: feature/scrap-inference-programme
  - PyAutoBrain: feature/scrap-inference-programme
- summary: |
    Phase 2 of the autolens-inference epic: Gut-archive origin/main of autolens_profiling
    as archive/condemned/autolens-profiling/inference-programme, then delete the retired
    inference programme (searches framework + leaves, results/searches, InferenceRefs_v1,
    notes/inference + gradient_slam, CORTEX.md, 58 search submits, 8 search tests), repair
    build_readme/lint/profile/wall/docs, repoint Brain samplers mature tier at
    autolens_inference, condemned.md entry, close #218/#205, reframe #166. Plan on #245.
