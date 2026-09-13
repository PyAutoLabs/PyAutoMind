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
- session: claude --resume session_018oyeoiMrc8vhhahAyA1VNP
- status: awaiting-merge (PR open under Heart RED with human authorisation 2026-09-13; merge is human)
- worktree: ~/Code/PyAutoLabs-wt/fixed-lens-light-source-only
- repos:
  - autolens_profiling: feature/fixed-lens-light-source-only
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/250
- parallel-claim: "autolens_profiling claim released: matrix-free-pixelized-likelihood merged 2026-09-12 (#247); branch merged main in"
- summary: |
    Fixed lens light after SLaM light[1] (MGE → regular profiles at solved intensities,
    source-only inversion): A100 cost of positivity kept (PDIP), certified active-set solve,
    and positivity dropped, vs the 50.6 ms fiducial. Phases: kernels+CPU probe+tests →
    A100 cell + 3 legs → note + README + ship. Plan on the issue and in
    ~/.claude/plans/precious-brewing-trinket.md.
- note: all three phases shipped 2026-09-13; five A100 legs 342802-342806 harvested (gpu-2, fp64, all gates PASS) and the verdict written to autolens_profiling `results/notes/fixed_lens_light_source_only_2026_09.md` — S3 certified active-set 4.21 ms at pass 2 (Delaunay) / 11.05 ms at pass 7 (rect) vs 25.8-28.3 ms S3 PDIP, library call 26-30 % faster with no solver change. Follow-ups are the `fixed-lens-light-profiling` epic (5 phases). PR #250 awaits /prm.

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

## sersic-variants-analysis
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/76
- issued: 2026-09-12
- prompt: active/sersic_variants_analysis.md
- session: claude --resume session_01KTGhZacWuxrxYkXXWXJbBx
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/sersic-variants-analysis
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/sersic-variants-analysis
- note: "worktree_check_conflict sersic-variants-analysis euclid_strong_lens_modeling_pipeline exits 1 on three claims. remove-fits-dataset-plots-yaml is stale (PR #63 merged, issue #62 closed 2026-09-10, no close-out). sed-chain-cpu-route (PR #70) and sersic-variants (PR #75) are live, but neither file set intersects this one: this task adds only scripts/analysis/** (new tree), tests/test_sersic_variants_analysis.py (new) and one line in config/build/no_run.yaml, which neither touches. Its documentation deliberately goes in a new scripts/analysis/README.md rather than scripts/README.md or catalogue/README.md, which belong to PR #75's diff. Waived on the human's plan approval, in a fresh parallel worktree based on origin/main - the same call sed-chain-cpu-route itself recorded against remove-fits-dataset-plots-yaml."
- summary: |
    PR 2 of the euclid_sersics variants work: scripts/analysis/sersic_variants.py
    reads the four lens_sersic_<variant>.csv scrapes that PR #75's --variant
    produces and emits the per-variant comparison production needs - N, median n,
    fractions above 4.5/4.9/9.5 (and 5.0 for wide_n), paired dn and dR_eff against
    baseline with 16-84 % bands, June-vs-baseline dn from sample/lens_map.csv, and
    the four witness readings W1-W4 printed as numbers beside their pre-registered
    thresholds, never as a verdict word. Four-panel shared-bin histogram PNG plus a
    markdown report. Pure functions split from the CLI; a synthetic four-CSV
    fixture with a variant missing two tiles pins the inner join and its reporting.

## fixed-light-library-path
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/251
- issued: 2026-09-13
- prompt: active/fixed_light_unconstrained_library_path.md
- session: claude --resume session_018oyeoiMrc8vhhahAyA1VNP
- status: awaiting-merge (PR open under Heart RED with human authorisation 2026-09-13; merge is human, and stacked PR #250 merges first)
- worktree: ~/Code/PyAutoLabs-wt/fixed-light-library-path
- epic: fixed-lens-light-profiling phase 1
- repos:
  - autolens_profiling: feature/fixed-light-library-path
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/252
- parallel-claim: "worktree_check_conflict fixed-light-library-path autolens_profiling exits 1: autolens_profiling is claimed by fixed-lens-light-source-only (#248). That task is phase 0 of the same epic and is frozen at PR-open — PR #250 is open and awaiting a human merge, its branch is at 319f078, and no further edits to it are expected. This task is deliberately STACKED on that branch (base feature/fixed-lens-light-source-only, not main) because the cell and kernels it extends exist only there, so the two cannot conflict: one is the parent commit of the other. Registered as a parallel claim in a fresh worktree, the same call #248 itself recorded against #247."
- summary: |
    Phase 1 of the fixed-lens-light-profiling epic. A new cell
    scripts/imaging/likelihood_breakdown/fixed_light_library.py times the WHOLE library
    likelihood call (FitImaging/AnalysisImaging.log_likelihood_function under jit) on the
    A100 for five solver routes: S0 PDIP (library today), S3 PDIP, S3 positive-negative
    (use_positive_only_solver=False -> xp.linalg.solve, MGE subtracted beforehand so it is
    not in the matrices), S3 certified active-set at phase 0's per-mesh certifying pass
    budget with PDIP fallback, and that same route at budget 1 so the fallback always fires
    (the worst-case per-call cost). Single call and @vmap 16, HST, meshes rect / delaunay /
    delaunay_nn, RAL gpu-2 fp64. The certified scheme is injected by a scoped harness
    monkeypatch of inversion_util.reconstruction_positive_only_from — no PyAutoArray change.
    Phase 0's projection ("~24 ms/call certified") is arithmetic; this measures it.
- note: shipped 2026-09-13 — cell + injection module + 35 tests (suite 224), three A100 legs 342908-342910 harvested (gpu-2, fp64, COMPLETED 0:0, all gates PASS, five equivalence pins 1e-15..1e-11), note `results/notes/fixed_lens_light_library_path_2026_09.md` and the README prose row. Certified active set halves the library call (50.97 -> 25.10 ms rect 2.03x, 65.10 -> 25.39 ms Delaunay 2.56x, 72.95 -> 36.26 ms DelaunayNN 2.01x); phase 0's projection held. Positive-negative stays prohibited (+334.93 nats rect). Two findings for any implementation: the library subsets to solve_ids_to_keep before calling its solver, and lax.cond runs both branches under vmap. PR #252 is STACKED on #250 (base feature/fixed-lens-light-source-only) - merge #250 first, then /prm this one. Next is epic phase 2 (CPU + RTX 2060).

## model-figures-rollout-lens
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/542
- issued: 2026-09-13
- prompt: active/model_figures_6b_lens_surfaces.md
- session: claude --resume session_01DLx38vS6F1M7K5LnpVbeZ7
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/model-figures-rollout-lens
- epic: model-figures phase 6b
- release-gate: PyAutoFit
- repos:
  - autolens_workspace: feature/model-figures-rollout-lens
  - HowToLens: feature/model-figures-rollout-lens
- note: "worktree_check_conflict model-figures-rollout-lens autolens_workspace HowToLens exits 0 (2026-09-13, after the stale remove-fits-dataset-plots-yaml claim was closed out). Plan approved in Plan Mode 2026-09-13; SLaM deferred to 6b2; autolens_workspace ships as two PRs (A: guides/imaging/point_source/multi_dataset; B: interferometer/group/multi_galaxy/cluster/weak on feature/model-figures-rollout-lens-b after A merges); release-gate PyAutoFit because guides/modeling/advanced/expectation_propagation.py uses EPResult.factor_graph (merged 6a, unreleased)."

## simulator-from-result-linear
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/77
- issued: 2026-09-13
- prompt: active/simulator_from_result_linear_intensities.md
- session: claude --resume session_01EehLEWoRRsmnLys4aHj5W4
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/simulator-from-result-linear
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/simulator-from-result-linear
- note: "worktree_check_conflict simulator-from-result-linear euclid_strong_lens_modeling_pipeline exits 1 on three claims (sed-chain-cpu-route PR #70, sersic-variants PR #75, sersic-variants-analysis #76). No file set intersects this one: this task touches scripts/simulator.py (none of the three edits it), tests/test_simulator_from_result.py (new) and the --from-result bullet of scripts/README.md at ~line 63 — PR #75's only scripts/README.md hunk is four lines at ~line 22 in the fitting-scripts list, a different hunk that merges cleanly. Waived in a fresh parallel worktree based on origin/main, the same call sed-chain-cpu-route recorded against remove-fits-dataset-plots-yaml and sersic-variants-analysis recorded against both live tasks."
- autonomy: "--auto launch; effective level = min(prompt safe, bug cap supervised) = supervised, so the ship checkpoint resolves to decide-and-flag (AUTONOMY.md, extended 2026-09-07). Plan approval of record is the human's launch instruction 'im going out so autonomously get these sersic things simulated and their vis_lp runs going'; both plan levels written to issue #77. Ends at PR-open."
- summary: |
    simulator.py --from-result rebuilt the tracer from files/model.json plus the
    max-log-likelihood vector, but every profile this pipeline fits is linear
    (al.lp_linear.*), so the rebuilt profiles carry no intensity and the mock is
    noise (tile 0 of dr1_sep1_sersics: mock VIS peak SNR 3.9 vs 81 real). The
    solved-intensity tracer is already on disk as files/tracer.json, written by
    AnalysisDataset.save_results from fit.model_obj_linear_light_profiles_to_light_profiles.
    Read that instead, under the same resolve_files_path hash, guard that no
    lp_linear profile survives, and add tests/test_simulator_from_result.py —
    --from-result had no test at all.
