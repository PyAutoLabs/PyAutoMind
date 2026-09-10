# Active Tasks

## vis-lp-latent-jit-assertions
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/732
- prompt: active/vis_lp_mge_stage_writes_no_latents.md
- issued: 2026-09-10
- session: claude --resume session_01FFSFgEBiZc7kTRutfK1RsN
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/734
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1600
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/734
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1600
- status: library-shipped, awaiting-merge
- location: web-github (session clones, no task worktree)
- worktree: n/a — web-github session clones (/home/user/PyAutoLens, /home/user/PyAutoFit)
- repos:
  - PyAutoLens: feature/vis-lp-latent-jit-assertions
  - PyAutoFit: feature/vis-lp-latent-jit-assertions
- summary: |
    Root cause is not the global NaN mask (it already drops all-NaN columns and
    salvages greedily): `LatentLens.variables` builds its instance with the
    default assertion check, which cannot be traced under the engine's per-sample
    `jax.jit`, so the ordered-MGE `vis_lp` model raised on every sample and the
    engine swallowed the raise into NaN rows. Fix: PyAutoLens builds the latent
    instance the way `Fitness` does under JAX; PyAutoFit logs the swallowed
    exception (count + first traceback) and names the every-sample case. The
    pipeline's own two trace failures are filed as
    draft/bug/euclid/vis_lp_latent_euclid_jit_trace.md (gated on #732).

## a100-pixelized-baseline
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/241
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/242
- heart-ack: 2026-09-10 in-session, YELLOW, four reasons: "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)" and three "profiling drift: runtime/imaging/{mge,mge_mass_jax,pixelization_numba_mge_mass}/…" rows — organism-scope, none touched by this branch
- prompt: active/a100_pixelized_likelihood_baseline_for_matrix_free.md
- issued: 2026-09-10
- session: claude --resume session_01GqnrYLZw26f29M8w5sXz2j
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/a100-pixelized-baseline
- repos:
  - autolens_profiling: feature/a100-pixelized-baseline

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
