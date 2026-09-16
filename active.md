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

## simulator-from-result-linear
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/77
- issued: 2026-09-13
- prompt: active/simulator_from_result_linear_intensities.md
- session: claude --resume session_01EehLEWoRRsmnLys4aHj5W4
- status: blocked
- worktree: ~/Code/PyAutoLabs-wt/simulator-from-result-linear
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/simulator-from-result-linear
- note: "worktree_check_conflict simulator-from-result-linear euclid_strong_lens_modeling_pipeline exits 1 on three claims (sed-chain-cpu-route PR #70, sersic-variants PR #75, sersic-variants-analysis #76). No file set intersects this one: this task touches scripts/simulator.py (none of the three edits it), tests/test_simulator_from_result.py (new) and the --from-result bullet of scripts/README.md at ~line 63 — PR #75's only scripts/README.md hunk is four lines at ~line 22 in the fitting-scripts list, a different hunk that merges cleanly. Waived in a fresh parallel worktree based on origin/main, the same call sed-chain-cpu-route recorded against remove-fits-dataset-plots-yaml and sersic-variants-analysis recorded against both live tasks."
- parked: "2026-09-13. The fix is COMPLETE and pushed: feature/simulator-from-result-linear @ 85f6dfd6bf33b9f19418abbe42afb9f90fd96a21. Ship parked at the autonomous-ship gate leg 4 — pyauto-heart readiness is RED, reason verbatim 'release validation FAILED (stage integrate)'. AUTONOMY.md: Heart RED forbids PR-open at every autonomy level, and the corrective-PR exception never fires under --auto (and would not apply — that RED is organism-scope release validation, nothing in this branch is in the release chain). Legs 1-3 PASS: tests 128 fast + 6 slow, smoke 9/9, review CLEAN with the lifted claim basis-cited. Witness met: mock VIS peak/median-RMS 72.3 vs 81.1 real on tile Tile102008855RA0680593469007DECNEG0634007351862, truth.json lens intensity 0.008437 / source 8.180 (3.9 before the fix). Unblock = a human running /ship_workspace once Heart is green, or explicitly authorising the PR. The branch is usable as-is by the science clone meanwhile. Evidence on the issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/77#issuecomment-5653294402"
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
## howtofit-mode
- issue: https://github.com/PyAutoLabs/autofit_assistant/issues/42
- issued: 2026-09-14
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtofit-mode
- repos:
  - HowToFit: feature/howtofit-mode
  - autofit_workspace: feature/howtofit-mode
  - PyAutoFit: feature/howtofit-mode
- released-repo: autofit_assistant — PR #43 merged; issue #42 closed; remaining repo claims retained.
- prompt: active/howtofit_mode.md
- summary: Assistant implementation ready and reviewed; approved README prompt propagation to HowToFit, autofit_workspace and PyAutoFit in progress. Shipping held by Heart YELLOW pending human acknowledgement.
- ship-hold: |
    Workspace validation: 3 failures (cloud#34824535982).
    Manifest drift: organism-map 2; public front-door 2.
    Profiling drift: three matrix_free SLQ fp64 results — delaunay_hpc_a100,
    delaunay_nn_hpc_a100, rectangular_hpc_a100.
- next: Acknowledge these Heart YELLOW reasons before ship_workspace; source remains local and uncommitted.
- parallel-claim: |
    RESOLVED 2026-09-14: the parallel task `howtofit-tutorial-4-6-feedback`
    (HowToFit#61 / PR#62) merged and closed out, so HowToFit is no longer shared
    and this claim stands alone again. Kept as a record of a deliberate,
    human-approved override of the conflict guard, not drift. Evidence at the
    time: this task's `feature/howtofit-mode` had 0 commits of its own and 0
    changed files against origin/main (9 behind, working tree clean) — the
    HowToFit claim was registered but never used. File sets were disjoint:
    howtofit-mode is README/AGENTS assistant-prompt propagation; the other task
    touched scripts/, notebooks/ and markdown/ under chapter_1_introduction only.
    NOTE: `feature/howtofit-mode` is now 9+ commits behind origin/main and the
    merged tutorial work landed there — rebase before editing HowToFit here.

## multi-galaxy-j1011-real-data
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/549
- issued: 2026-09-15
- prompt: active/multi_galaxy_package.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/multi-galaxy-j1011-real-data
- repos:
  - autolens_workspace: feature/multi-galaxy-j1011-real-data

## jax-runtime-and-parity
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/317
- issued: 2026-09-15
- session: claude --resume c74b6b89-11fe-42df-8b16-09bb12dcedb6
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/jax-runtime-and-parity
- repos:
  - autolens_workspace_test: feature/jax-runtime-and-parity
  - autogalaxy_workspace_test: feature/jax-runtime-and-parity

## ep-release-search-internals
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1631
- issued: 2026-09-15
- prompt: active/ep_re_jit_compiles_the_vmapped_likelihood.md
- session: claude --resume 32df3fc7-e0cc-4fc7-98c7-0f160dca158c
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/ep-release-search-internals
- repos:
- parallel-claim: PyAutoFit also claimed by howtofit-mode (README propagation only; its PyAutoFit worktree clean, 0 commits ahead of origin/main on 2026-09-15); disjoint files, own worktree when started
- note: "Planned and parked by the human on 2026-09-15 — implementation not started, no worktree yet. The full two-level plan is on the issue; resume with /start_library ep-release-search-internals. Fix locus: AbstractSearch.optimise releases result._search_internal before status.result so each EP factor search's Fitness and its compiled JAX executables are collectable (slope_hierarchy_scale job 342410 retained 76 searches' executables and died in LLVM section memory at 64 GB). Follow-ups to /intake at ship: analysis-level compile cache across EP steps; vmap(jit) batch-shape churn."

## jit-visualization-outputs
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/318
- issued: 2026-09-15
- prompt: active/jit_visualization_outputs.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/jit-visualization-outputs
- repos:
- summary: |
    Prompt's defect REFUTED twice (2026-08-21, 2026-09-15): all 4
    modeling_visualization_jit scripts pass from cleared output under
    profile_release on current main (8/8 passes, libraries moved 58-186 commits
    between gates). Only residual is the stale point_source/visualization parking
    (autolens_workspace_test config/build/no_run.yaml:30, "exceeds 300s" -
    measured 168 s / 202 s locally, margin narrowing). PLAN ONLY, NOT STARTED:
    the human deferred execution on 2026-09-15; no worktree, no branch, no code
    change. Resume = /start_workspace, push the empty branch, dispatch retime.yml
    (point_source/visualization/modeling_visualization_jit.py, 5x, 300 s cap),
    then settle the marker FROM the measurement (all under cap -> unpark; any
    over -> keep parked with the measured #274-style verdict). One-line
    workspace PR; close-out record says "no defect exists to fix" like siblings
    PyAutoFit#1508 / PyAutoArray#467. Incidental: "Visualization warm-up failed
    (non-fatal)" swallowed in autofit fitness.py for ellipse + point_source -
    separate prompt draft/bug/autofit/visualization_warmup_swallowed_exception.md.

## mixed-precision-inversion-gap
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/552
- issued: 2026-09-15
- prompt: active/mixed_precision_inversion_jax_numpy_gap_small_data.md
- session: claude --resume 06b62eb4-de08-40c6-91e0-ecce790fce3d
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/mixed-precision-inversion-gap
- repos:
- parallel-claim: "autogalaxy_workspace_test is claimed by jax-runtime-and-parity (autolens_workspace_test#317, smoke_tests.txt only, zero diff vs main on 2026-09-15); this task's workspace leg is one tolerance edit in scripts/imaging/jax_likelihood/rectangular.py and is added via worktree_add_repo only after that claim clears. PyAutoArray is unclaimed."
- note: "Planned and parked by the human on 2026-09-15 — implementation not started, no worktree yet. The full two-level plan is on the issue; resume with /start_library mixed-precision-inversion-gap (PyAutoArray only, library first). Before any measurement move autogalaxy_workspace_test/dataset/imaging/jax_test aside: the on-disk copy is the stale pre-#117 180x180 dataset and should_simulate does not detect the resolution change. Key reframing: the asserted quantity is log_likelihood so the gap is pure delta-chi-squared; the NumPy reference is not fp64 (mapper_util honours use_mixed_precision on numpy); the fp32 curvature branch is inert but rounds 1/sigma inconsistently with the fp64 data vector; JAX (jaxnnls IPM) and NumPy (fnnls) run different NNLS algorithms."

## fixed-light-numba-levers
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/267
- issued: 2026-09-16
- prompt: active/fixed_light_numba_s3_regularization_logdet_levers.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/fixed-light-numba-levers
- repos:
  - PyAutoArray: feature/fixed-light-numba-levers
  - autolens_profiling: feature/fixed-light-numba-levers
- note: "LEVER 1 PR-OPEN 2026-09-16: PyAutoArray PR #553 (pending-release, bae9296e) + autolens_profiling PR #269 (7c7968c4, c899326e — note results/notes/fixed_lens_light_levers_2026_09.md). Measured RAL 343345: route b memo-ON 413.3 -> 299.7 ms (1.38x), H 110.6 -> 5.9 ms, 4/4 gates, witness bit-identical; 343346 A100 identity, #536 compaction constants inert at K=4. Heart RED (install verify testpypi F; release validation integrate) acknowledged by the human for PR-open only; merge via /prm. NEXT: lever 2 (log det H from sparsity) on feature/fixed-light-numba-levers-l2 stacked on lever 1, then lever 3 (shared Cholesky; folds draft/bug/autoarray/curvature_reg_matrix_rebuilt_every_access.md, numpy/numba only). Phase 3 of fixed-lens-light-numba-cpu; sized too-large by intake, large kept per the prompt."
- summary: |
    Lever 1 (DONE, PR-open): jit the split-regularization assembly on the
    numpy/numba path, bit-for-bit accumulation order, Python bodies retained as
    _reference (the JAX tests use them as ground truth), fixing three recorded
    defects (in-place mutation of the interpolators' cached_property tables, the
    size == 0 j-leak, the unbounded insert). Lever 2: log_det_regularization_matrix_term
    dense-factorises a ~20-nnz/row matrix; the :903 docstring claiming scipy sparse
    is stale and is fixed regardless. Lever 3: one shared Cholesky of F + lambda*H
    for the solve, the seed and the log-det (S3 only), folding in
    draft/bug/autoarray/curvature_reg_matrix_rebuilt_every_access.md. CPU leg is the
    RAL gpu partition CPUs-only (no --gres), 1 thread across numba and BLAS, A/B
    against a private merge-base PyAutoArray on PYTHONPATH — never the shared
    /mnt/ral/jnightin/PyAuto install. A100 leg is fp64, budget 7 on Delaunay, PDIP
    fallback, positivity never dropped. Pins: log evidence <= 1e-9 relative,
    regularization matrix bit-identical, log_likelihood NOT comparable across legs.

## pixelized-clumps-robust-scale
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/78
- issued: 2026-09-16
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/pixelized-clumps-robust-scale
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/pixelized-clumps-robust-scale
- prompt: active/pixelized_source_clumps_empty_on_real_dr1.md
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/79 (commit 39faca8, label pending-release; smoke euclid 9/9)
- heart-ack: "Heart RED at ship (2026-09-16), acknowledged by the human for PR-open only: 'install verification FAILED (testpypi; checks F)'; 'release validation FAILED (stage integrate)' — both unrelated to this repo; merge stays with /prm"
- next: /prm once the fast + slow CI jobs are green on PR #79; then the human reruns the dr1_sep1 wcs.json reload on RAL
- summary: wcs.json `source_clumps` is empty on every real DR1 vis_pix fit (0.5×max rule); switch the pipeline finder to a 0.5×p99 scale via the `pix_indexes` seam, add a brightest-pixel failsafe recorded as `source_clump_rule`, witness on 4 real tiles, add spike/failsafe/force_pickle_overwrite tests. Gates the euclid_dr1 wcs.json reload pass.
- parallel-claim: "euclid_strong_lens_modeling_pipeline is also claimed by sed-chain-cpu-route (PR #70), sersic-variants (PR #75), sersic-variants-analysis and simulator-from-result-linear. Human-approved own worktree on 2026-09-16 (plan approval): file sets disjoint except sersic-variants, which edits util.py at lines >= 1084 (EuclidDataset / load_vis_dataset / parse_fit_args) and catalogue/README.md line ~130; this task edits util.py 755-1055 (clump finder, wcs_dict_from), catalogue/README.md ~165, tests/test_wcs_dict.py, tests/test_latent_run_level.py. Whoever merges second rebases."
