# Active Tasks

## witness-campaign
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/398
- issued: 2026-09-10
- prompt: active/witness_campaign.md
- session: claude --resume session_01LRRECsu9gfMvjb8F5aXMHu
- status: library-dev
- location: web-github (session clones, no task worktree; branch claude/active-witness-campaign-0g8phk)
- worktree: n/a — web-github session clone (/home/user/PyAutoMind)
- repos:
  - PyAutoMind: claude/active-witness-campaign-0g8phk
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
    Pass 2 (`autoarray`, 11) SHIPPED 2026-09-17: 10 judge / 1 glance ->
    1 notify / 9 glance / 1 judge, 173 seed review-minutes -> 47; first
    `Witness: none —` (multiwavelength_inversion). Backlog now 157 ready,
    72 witnessed + 1 none, derived 18 notify / 44 glance / 95 judge.
    Follow-up for the Brain: the sizing faculty has no `none` rule (reads
    `Witness: none —` as a witness). Next: autofit (14), autolens (11),
    autolens_workspace (7), euclid (6), autogalaxy (5), autolens_profiling
    (5), tail (~30 singletons).
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
- session: https://claude.ai/code/session_01LfJojDFow4pxPzuwRHqMt2 (web-github resume 2026-09-17; planned 2026-09-12 in session_01KTGhZacWuxrxYkXXWXJbBx)
- status: workspace-dev
- worktree: n/a — web-github session clone (/home/user/euclid_strong_lens_modeling_pipeline); the local ~/Code/PyAutoLabs-wt/sersic-variants-analysis worktree named on 2026-09-12 never pushed feature/sersic-variants-analysis, so the branch of record is the session's
- repos:
  - euclid_strong_lens_modeling_pipeline: claude/sersic-variants-analysis-3iqibr
- resume: "IMPLEMENTED 2026-09-17 (web-github; Fable planned, Opus executed): claude/sersic-variants-analysis-3iqibr pushed at 480c107 — scripts/analysis/{sersic_variants.py,README.md,__init__.py}, tests/test_sersic_variants_analysis.py (8 tests), one config/build/no_run.yaml entry. Verified locally: the new tests + test_repo_invariants + test_compare_catalogues, 26 passed; the rest of the fast suite needs astropy/autolens (absent in the container) — CI runs it. FLAGGED on issue #76 comment 5715176814: the W1-W4 thresholds are transcribed into the module's WITNESSES constant (plan page rev 3 unreachable from the session) and need the human's confirmation. NEXT = /ship_workspace (PR) then /prm; nothing here imports --variant, so PR #75's merge order is not a gate."
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

## multi-galaxy-j1011-real-data
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/549
- issued: 2026-09-15
- prompt: active/multi_galaxy_package.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/multi-galaxy-j1011-real-data
- repos:
  - autolens_workspace: feature/multi-galaxy-j1011-real-data
- note: "2026-09-17 /start_dev resume from a cloud session: blocked — every HST/SDSS archive host is 403 through the session proxy and the feature branch is not on the autolens_workspace remote (local-only or never created). Needs a local CLI session; nothing to do from the web."

## jax-runtime-and-parity
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/317
- issued: 2026-09-15
- session: claude --resume c74b6b89-11fe-42df-8b16-09bb12dcedb6
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/jax-runtime-and-parity
- repos:
  - autolens_workspace_test: feature/jax-runtime-and-parity
  - autogalaxy_workspace_test: feature/jax-runtime-and-parity

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

## hst-gpu-residue-p2
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/273
- issued: 2026-09-16
- prompt: active/hst_gpu_residue_p2_vmap_vs_jit_and_batched_callback.md
- session: claude --resume 51243072-d1a4-437b-b5a6-edf3bff12db4
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/hst-gpu-residue-p2
- repos:
  - autolens_profiling: feature/hst-gpu-residue-p2
- parallel-claim: "autolens_profiling was also claimed by fixed-light-numba-levers (#267, COMPLETE 2026-09-16, merged and closed out; worktree removed): its files are fixed_light_numba*, fixed_light_numpy_solvers.py, the lever submits/results and fixed_lens_light_levers_2026_09.md; this task touches fixed_light_trace.py, a new host_callback_probe.py, library_solver_injection.py, a new vmap submit + results + note — disjoint, own worktree beside it exactly as phase 1 (#268) did."
- note: "Phase 2 of hst-gpu-non-solver-residue, STEP 1 ONLY (matched vmap-vs-jit A100 experiment + policy; PyAutoArray batch-aware callback deferred to phase 2b via /intake if the numbers warrant). Fable session plans, Opus executes. A100 submit -> wait -> harvest is a human resume point. Heart RED (install verify testpypi F; release integrate) at start; PR-open needs the human's ack. Phase-1 worktree ~/Code/PyAutoLabs-wt/hst-gpu-residue-p1 still awaits the human's cleanup (3 untracked .err -> worktree_remove -> branch -d)."
- hpc: "A100 array 343376 tasks 0-4 SUBMITTED 2026-09-17 00:10 BST from RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/hst-gpu-residue-p2 @ bf52147 (B16 distinct fb-on / B16 fb-off / B8 / B4 / B16 identical control); all 5 RUNNING on euclid-ral-gpu-1/2 at submit. HUMAN RESUME POINT: when done, harvest = commit the 5 results/breakdown/imaging/fixed_light_trace_delaunay_vmap*_hpc_a100_fp64_*.{json,png} in the RAL worktree, fetch locally (git fetch euclid_jump:/mnt/ral/jnightin/autolens_profiling_wt/hst-gpu-residue-p2 feature/hst-gpu-residue-p2), check AUTOTUNE_ENTRIES count=0 + unjoined 0 + lane pins PASS in hpc/batch_gpu/output/output.343376_*.out, then Phase C (note + errata + README + ship). Phase A on the issue: #273 comment 2026-09-17."

## fixed-light-numba-s4
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/274
- issued: 2026-09-17
- prompt: active/fixed_light_numba_s4_curvature_kernel_ab_and_permute_active_last.md
- session: claude --resume 3f1053cc-606f-4477-bef4-abe3a68cd02b
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/fixed-light-numba-s4
- repos:
  - autolens_profiling: feature/fixed-light-numba-s4
- parallel-claim: "worktree_check_conflict fixed-light-numba-s4 autolens_profiling PyAutoArray exits 1 on hst-gpu-residue-p2 (#273, feature/hst-gpu-residue-p2, LIVE). Its branch touches fixed_light_trace.py, host_callback_probe.py, library_solver_injection.py, test_fixed_light_cell.py, test_fixed_light_vmap_submit.py and a vmap A100 submit; this task touches fixed_light_numba.py, a new fixed_light_numpy_kernels.py, a new s4 witness, a new batch_cpu s4 submit, new test_fixed_light_s4.py, test_fixed_light_numba.py (overhead gate) and a new note — disjoint. Shared generated surfaces only: README.md (regenerate after whichever merges second) and one hpc/README.md route row. Waived on the human's plan approval 2026-09-17, fresh parallel worktree off origin/main — the same call p2 recorded against #267."
- note: "Phase 4 of fixed-lens-light-numba-cpu. Two waves, sequential PRs, never stacked (#267 lesson). WAVE A IN FLIGHT 2026-09-17 00:25 (human asleep; Opus finishing locally, NOTHING pushed, NO RAL job): DONE on feature/fixed-light-numba-s4 — e0ca612 ms-budget overhead gate (MAX_INSTRUMENTATION_OVERHEAD_MS=12), f88b9e0 fixed_light_numpy_kernels.py seam (two_stage/direct/two_stage_touched, touched bit-identical), 8998ec9 routes b_direct/b_touched; in progress — s4 witness, batch_cpu s4 submit (+WALL-BASIS), test_fixed_light_s4.py, local end-to-end run. RESUME: cd ~/Code/PyAutoLabs-wt/fixed-light-numba-s4/autolens_profiling; git log --oneline origin/main..HEAD; run the issue's Verification block; then plan step 6 (push branch, RAL worktree, hpc/sync submit --cpu, harvest), note results/notes/fixed_lens_light_s4_2026_09.md, /ship_workspace (Heart RED install-verify/integrate -> human ack), conditional PyAutoArray PR (docstring fix always), /prm; wave B (A-prime) only after wave A merges. Plan on the issue."

## witt-wynne-catalogue
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/84
- issued: 2026-09-17
- prompt: active/witt_wynne_catalogue_output.md
- session: claude --resume 29f963ca-d96d-4b96-8f8c-a6aa699fcba4
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/witt-wynne-catalogue
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/witt-wynne-catalogue
- note: "worktree_check_conflict witt-wynne-catalogue euclid_strong_lens_modeling_pipeline exits 1 on five claims (sed-chain-cpu-route PR #70, sersic-variants PR #75, sersic-variants-analysis #76, simulator-from-result-linear #77 parked, astrometric-offsets-catalogue #83 unpushed). Code file sets are disjoint. astrometric-offsets-catalogue also adds a producer and edits the same wiring files (scripts/build_inspection_bundle.sh stage echoes, config/build/no_run.yaml, README.md, scripts/README.md, catalogue/README.md): one-hunk resolution on whichever merges second. Waived on the human's plan approval 2026-09-17; fresh parallel worktree off origin/main."
- sibling: witt-wynne-guide-fixes (same review, autolens_workspace guide)

## witt-wynne-guide-fixes
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/552
- issued: 2026-09-17
- prompt: active/witt_wynne_guide_fixes.md
- session: claude --resume 29f963ca-d96d-4b96-8f8c-a6aa699fcba4
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/witt-wynne-guide-fixes
- repos:
  - autolens_workspace: feature/witt-wynne-guide-fixes
- note: "worktree_check_conflict witt-wynne-guide-fixes autolens_workspace exits 1 on multi-galaxy-j1011-real-data (#549); file-disjoint (this task touches only scripts/guides/misc/witt_wynne.py, its notebook and README). Waived on the human's plan approval 2026-09-17; fresh parallel worktree."
- sibling: witt-wynne-catalogue (pipeline producer copying the fixed span)
