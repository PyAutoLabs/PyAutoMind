# Active Tasks

## einstein-radius-jit-seed-finder
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/614
- issued: 2026-09-11
- prompt: active/einstein_radius_jit_native_seed_finder.md
- session: claude --resume session_014JqpPWfk6nUAqnyv4P5oNM
- status: library-shipped, awaiting-merge — merge order PyAutoGalaxy#615 → PyAutoLens#735 (library-first; the Lens leg needs #615 at release). Human /prm.
- location: web-github (session clones, no task worktree)
- worktree: n/a — web-github session clone (/home/user/pyautogalaxy)
- repos:
  - PyAutoGalaxy: feature/einstein-radius-jit-seed-finder
  - PyAutoLens: feature/einstein-radius-jit-seed-finder
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/615
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/735
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/615
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/735
- summary: |
    Make `init_guess` optional on `LensCalc.einstein_radius_jit_from`: a
    JAX-native argmin-on-coarse-grid seed finder runs inside the trace when
    no seed is passed (`seed_grid_shape` / `seed_grid_extent` exposed for
    clusters). Two sequenced library PRs: PyAutoGalaxy (helper + signature +
    tests), then PyAutoLens (`autolens/analysis/latent.py::
    effective_einstein_radius` drops its hardcoded 4-seed fan). The prompt's
    euclid `util.py` workspace leg is obsolete — that fan already moved into
    PyAutoLens. Feature Agent's 4-phase split overridden: change is ~40 lines
    + tests; re-size the header to `medium` at retirement.
- plan: On issue #614; approved by the user 2026-09-11 ("go"). Both legs shipped as PRs the same day; JAX verification numbers in #615's body.

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
- status: awaiting-merge — merge order Mind#401 (firewall allowlist, code) → re-run Brain#376 Brain Tests → Brain#376 → autolens_profiling#246 (lint green, clean; 555 files deleted). Human /prm.
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/246
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/376
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/401
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

## ep-no-multiprocessing-pool
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1608
- issued: 2026-09-11
- prompt: active/ep_must_never_drive_nautilus_through_a.md
- session: claude --resume session_01FU8EkdahFWmrL6pewkHZR3
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1610
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1610
- location: web-github (session clone /home/user/pyautofit, no task worktree; Mind branch claude/autofit-ep-nautilus-bug-ftngha)
- worktree: n/a — web-github session clone (/home/user/pyautofit)
- repos:
  - PyAutoFit: feature/ep-no-multiprocessing-pool
- summary: |
    Human ruling 2026-09-09: EP never runs a factor search through a Python
    multiprocessing pool (RAL 342351_0 hung 27 h after two forked workers
    segfaulted and Pool.map never returned). One PyAutoFit PR: (1)
    `AbstractSearch.optimise` refuses `number_of_cores>1` with a clear
    SearchException naming `number_of_cores=1` / `use_jax=True` as the fixes;
    (2) `_LikelihoodWorkerPool.map` gains a dead-worker watchdog (map_async +
    poll, construction-time PID set) so any multi-core Nautilus fit fails
    within seconds instead of hanging. Phase 2 (the science script's
    `--use_cpu` => `use_jax=False` conflation) filed separately.
