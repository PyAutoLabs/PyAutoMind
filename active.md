# Active Tasks

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

## remove-parallel-ep-optimiser
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1611
- issued: 2026-09-11
- prompt: active/remove_parallelepoptimiser_and_its_tests.md
- session: claude --resume session_01FU8EkdahFWmrL6pewkHZR3
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1612
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1612
- location: web-github (session clone /home/user/pyautofit, no task worktree)
- worktree: n/a — web-github session clone (/home/user/pyautofit)
- repos:
  - PyAutoFit: feature/remove-parallel-ep-optimiser
- summary: |
    Human decision 2026-09-11 after #1608/#1610: delete the never-used, never-exported
    ParallelEPOptimiser (EP's own fork pool across factors, subject to the same
    dead-worker hang and contradicting the 2026-09-09 ruling), its never-collected
    test helper, README §7, and the §8→§7 cross-references. PyAutoMemory F3 line
    updated in a separate ledger commit.

## matrix-free-pixelized-likelihood
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/247
- prompt: active/matrix_free_pixelized_imaging_likelihood_cg_solv.md
- issued: 2026-09-11
- session: claude --resume session_01U2JK8GSjn1WNFvFtk9LJBE
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/matrix-free-pixelized-likelihood
- repos:
  - autolens_profiling: feature/matrix-free-pixelized-likelihood
- summary: |
    Matrix-free pixelized imaging likelihood in autolens_profiling: PCG on (F+λH)x=D via the
    sparse operator's FFT apply, SLQ log-dets with fixed probes, matrix-free PDIP comparator;
    fiducial A100 legs vs the #243 reconstruction split, then the N_src 1500→12000 sweep
    (dense/sparse/matrix-free) whose crossover is the deliverable. PyAutoArray phase on go.
    Plan on the issue and in ~/.claude/plans/polished-roaming-squirrel.md.

## model-figures-renderer
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1613
- issued: 2026-09-11
- prompt: active/model_figures_2_renderer.md
- session: claude --resume session_0178yLU9v19GtACcRPFggjGa
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/model-figures-renderer
- repos:
  - PyAutoFit: feature/model-figures-renderer
- parallel-claim: "PyAutoFit is also claimed by remove-parallel-ep-optimiser (PR #1612, web session, no local worktree). File sets are disjoint (EP optimiser + its tests vs a new autofit/model_figure/ package, paths/directory.py, config/output.yaml, __init__.py, docs); the human approved a parallel worktree in the 2026-09-11 plan."
- summary: |
    Epic model-figures phase 2 of 6. Pure-matplotlib containment renderer over the
    phase-1 GraphSpec: af.ModelPlotter(model).figure(), opt-in model.png beside
    model.info behind a new strict output.yaml key model_figure (default false),
    acceptance renders committed under docs/images/model_figures/, cookbook docs
    pages; autofit_workspace follow-up adds cookbook figure calls + notebooks + config key.

## slam-base-driver
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/2
- issued: 2026-09-11
- prompt: active/slam_base_driver.md
- session: claude --resume session_01JJeCU1iLmJqQegZjB2oeA1
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/slam-base-driver
- repos:
  - autolens_inference: feature/slam-base-driver
- summary: |
    Epic autolens-inference phase 3 of 4: the backend-parameterised SLaM base-run driver,
    the one script the repo exists for. A thin leaf `scripts/imaging/slam/hst.py` over a new
    `scripts/misc/slam/_runner.py` runs the standard 5-stage HST SLaM chain under any of
    {numba_cpu, jax_cpu, jax_gpu} x {dense, sparse}, writing a schema-v1
    `results/slam/imaging/hst/<config>/stages_seed<n>.json` with one comparable row per stage
    (wall, compile split, reject-inclusive evals, log Z, posterior, truth delta/sigma,
    positions.info presence). Plus `--cores`/`--stages` on the CLI, a parity view in
    build_readme, six RAL submits with measured WALL-BASIS rates, CI smoke + dispatch witness,
    and docs. Phase 4 then files the Cortex task `slam_hst_base`.
    Plan on the issue and in ~/.claude/plans/idempotent-strolling-seahorse.md.
