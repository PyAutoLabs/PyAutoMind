# Active Tasks

## scientific-workflow-language
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1595
- issued: 2026-09-09
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/scientific-workflow-language
- repos:
  - PyAutoFit: feature/scientific-workflow-language
  - autofit_workspace: feature/scientific-workflow-language
  - HowToFit: feature/scientific-workflow-language
  - PyAutoHands: feature/scientific-workflow-language
- plan: Approved by user. Tutorial rewrite plus required fixes for live notebook display retention (PyAutoFit) and prose-only notebook generation (PyAutoHands); no API signature changes.
- progress: Implemented and locally validated; generated docs/notebooks updated. See active/scientific_workflow_language.md for validation and dependency details.

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
    28 notify / 74 glance / 8 judge. Pass 1 = the `workspaces` group (15).
    Pass-by-pass counts are recorded in the prompt itself.

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

## jax-import-order-x64
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/139
- issued: 2026-09-10
- prompt: active/jax_import_order_defeats_x64.md
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/140
- session: claude --resume session_01XMA4HZYcVEzayYaRmS2uHi
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/jax-import-order-x64
- repos:
  - autolens_workspace_developer: feature/jax-import-order-x64
- summary: |
    Launched with an explicit --auto; effective autonomy `supervised`
    (min of the prompt header and the `bug` work-type cap), so the ship
    checkpoint resolves to decide-and-flag and the run ends at PR-open.
    Scope corrected at the plan gate and human-approved: 48 offenders, not
    the 33 the prompt's line-number grep reported — 6 `jax_profiling/
    simulators/*` are already guarded, and 25 `searches_minimal/` scripts
    the grep could not see are. Fix is the repo's own guard idiom
    (`from autolens import jax_wrapper`) rather than an import reorder.
    Shipped to PR-open 2026-09-10. Ship-gate leg 4 (Heart) COULD NOT RUN —
    PyAutoHeart is not in this session's repo scope and `pyauto-heart` is not
    on PATH; it is recorded as not-consulted, never as passed, so the gate is
    incomplete and the human should know that before merging. Legs 1 and 2 are
    n/a by the gate's own applicability rule (no test dir, no smoke list) with
    substitute evidence named on the PR. One `decision-taken` flag: the six
    redundant `jax.config.update` calls were kept, not deleted as the plan
    said, because three carry comments that make deletion a judgement.
