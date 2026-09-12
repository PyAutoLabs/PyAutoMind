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

## sed-chain-cpu-route
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/69
- issued: 2026-09-11
- prompt: active/sed_chain_cpu_route_jax_cpu_backend.md
- session: claude --resume session_01AELxUSfSPRz2SDnnVJHohi
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/sed-chain-cpu-route
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/sed-chain-cpu-route
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/70
- note: worktree_check_conflict flagged euclid_strong_lens_modeling_pipeline as claimed by remove-fits-dataset-plots-yaml, whose PR #63 merged and issue #62 closed on 2026-09-10 without a close-out. Stale claim, waived on the human's plan approval; the file sets are disjoint (hpc/ submit scripts and README here, config/visualize/plots.yaml there) and this task runs in a fresh parallel worktree.
- summary: |
    The SED chain (Sersic VIS + per-band waveband fits) gets a CPU submit script,
    hpc/batch_cpu/submit_sersic_waveband, which pins JAX to the CPU backend exactly as
    stage 1 of submit_initial_lens_model_two_stage does for vis_lp (no --use_cpu: both SED
    analyses are use_jax=True and --use_cpu would flip them to Numba). It becomes the
    documented default; the GPU script stays as the optional route. README route table,
    hpc/sync comments and usage text, the sersic_lens_model.py batch_size docstring and the
    PyAutoCortex "Where to look" line are repointed. GPU job 342648 is untouched.

## fixed-lens-light-source-only
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/248
- prompt: active/fixed_lens_light_source_only_inversion.md
- issued: 2026-09-12
- session: claude --resume session_01N2HbUU5ZzLS5nA2JSuQp1r
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/fixed-lens-light-source-only
- repos:
  - autolens_profiling: feature/fixed-lens-light-source-only
- parallel-claim: "autolens_profiling claim released: matrix-free-pixelized-likelihood merged 2026-09-12 (#247); branch merged main in"
- summary: |
    Fixed lens light after SLaM light[1] (MGE → regular profiles at solved intensities,
    source-only inversion): A100 cost of positivity kept (PDIP), certified active-set solve,
    and positivity dropped, vs the 50.6 ms fiducial. Phases: kernels+CPU probe+tests →
    A100 cell + 3 legs → note + README + ship. Plan on the issue and in
    ~/.claude/plans/precious-brewing-trinket.md.

## model-figures-ep-view
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1618
- issued: 2026-09-12
- prompt: active/model_figures_5_ep_view.md
- session: claude --resume session_01AmyBwcVQBrWE4jSTqdATY6
- status: implementation-complete, ship BLOCKED at Heart RED
- worktree: ~/Code/PyAutoLabs-wt/model-figures-ep-view
- epic: model-figures phase 5
- repos:
  - PyAutoFit: feature/model-figures-ep-view
- note: "worktree_check_conflict model-figures-ep-view PyAutoFit exits 0 — no conflict. A parallel-worktree waiver was granted against PR #1612 (remove ParallelEPOptimiser) but is moot: #1612 merged 2026-09-12 19:29 and this branch starts from a main that contains it (54f464d97)."
- summary: |
    Phase 5 of the model-figures epic: the diagnostic EP view. New package
    autofit/model_figure/ep/ (spec -> state -> presentation -> layout -> render)
    plus af.EPPlotter, drawing an explicit factor graph with plate grouping and
    the EP run's state on it — factor status, update age and confirmed reverted
    updates — and never hiding a failing plate member behind an aggregate.
    Visualise writes graph_model.png once and graph_state.png per
    visualise_interval tick behind the existing output.yaml model_figure key.
    Human decisions: layout is networkx + matplotlib only (graphviz rejected —
    no dot binary locally, on the GH runner or Colab, not pip-installable);
    optional overlays (mean +/- std, precision, KL sparklines) deferred to a
    follow-up prompt. Plan on the issue.
- resume: |
    Branch feature/model-figures-ep-view is implemented, verified and pushed
    (ba756b82d, 6 commits on 54f464d97; test_autofit 2843 passed / 2 skipped,
    sphinx 30 == baseline, black + pyflakes clean). /ship_library stopped at the
    Heart gate: RED "release validation FAILED (stage integrate)" and no human
    authorisation for a PR-open under RED. No PR opened; gate-block comment on
    PyAutoFit#1618. next: clear the integrate RED (or authorise PR-open under it),
    re-run /ship_library, then /prm once CI green; then file follow-up prompts:
    optional EP overlays (mean+/-std / precision / KL sparklines) and phase-6
    rollout of graph_state.png to autofit_workspace expectation_propagation.py +
    HowToFit optional hierarchical EP tutorial (need visualise_interval=1).

## sersic-variants
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/74
- issued: 2026-09-12
- prompt: active/sersic_variants_prior_edge.md
- session: claude --resume session_01KTGhZacWuxrxYkXXWXJbBx
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/sersic-variants
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/sersic-variants
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/75
- note: "worktree_check_conflict sersic-variants euclid_strong_lens_modeling_pipeline exits 1 on two claims. remove-fits-dataset-plots-yaml is stale (PR #63 merged, issue #62 closed 2026-09-10, no close-out). sed-chain-cpu-route is LIVE (PR #70 open) and its file set genuinely overlaps: hpc/README.md route table (both add rows to the same table — a one-line resolution expected on whichever merges second) and scripts/sersic_lens_model.py (its only hunk there is a two-line batch_size docstring edit at ~250, clear of the model block extracted here). Waived on the human's plan approval, in a fresh parallel worktree — the same call sed-chain-cpu-route itself recorded against remove-fits-dataset-plots-yaml."
- summary: |
    --variant for the Sersic stage: four variants (baseline, wide_n,
    central_noise, sersic_point) on the same 100 euclid_sersics core lenses, to
    explain the lens-light Sersic index pile-up at the n = 5 prior edge. The
    inline model block in fit_sersic is extracted into a pure sersic_model_from
    helper; variant=None stays byte-for-byte today's behaviour and any other
    variant writes to unique_tag sersic_lens_model_<variant>. util gains a pure
    Gaussian noise-inflation helper (A = 9, sigma = 0.17") plus a keyword-only
    noise_inflation on load_vis_dataset, and parse_fit_args(with_variant=True).
    New hpc/batch_cpu/submit_sersic_variants runs the four variants sequentially
    inside one array task per lens, because all four restore the same vis_lp zip
    and PyAutoFit's restore() deletes it. Science-clone submit and the analysis
    script (PR 2) are follow-ups.
