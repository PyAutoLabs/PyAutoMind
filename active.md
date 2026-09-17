# Active Tasks

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

## jit-visualization-outputs
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/318
- issued: 2026-09-15
- prompt: active/jit_visualization_outputs.md
- session: web-github (Claude Code remote, 2026-09-17; no local worktree)
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/321
- repos:
  - autolens_workspace_test: claude/active-jit-visualization-outputs-45weg6
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
    PyAutoFit#1508 / PyAutoArray#467. SHIPPED 2026-09-17 (web session): CI
    retime run 35245806121 completed 10/10 (3.12: 73.6-98.6 s, 3.13:
    71.0-85.7 s, NEITHER both legs), parking entry deleted, PR #321 open with
    pending-release; /prm when Smoke Tests are green. Incidental: "Visualization warm-up failed
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

## grid-offset-prior
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/88
- issued: 2026-09-17
- prompt: active/datasetmodel_grid_offset_prior_0_2_clips.md
- session: claude --resume 7bff8610-4b84-413a-a994-d72484c4c14c
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/grid-offset-prior
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/grid-offset-prior
- note: "worktree_check_conflict grid-offset-prior euclid_strong_lens_modeling_pipeline exits 1 on five claims (sed-chain-cpu-route PR #70, sersic-variants PR #75, sersic-variants-analysis #76, simulator-from-result-linear #77 parked, witt-wynne-catalogue #84). Code file sets are disjoint; catalogue/README.md shares one hunk with witt-wynne-catalogue: one-hunk resolution on whichever merges second. Waived on the human's plan approval 2026-09-17; fresh parallel worktree off origin/main."
- note: "PAUSED 2026-09-17 17:10 BST, resumable. DONE on feature/grid-offset-prior (3 local commits d50eb52 prior ±0.5\" / 3563a98 prior_edge_y-x columns + header pin + tests / e58a1be README + eight producers; 208 fast tests green; NOT pushed, no PR). Witness done: sep1 Tile102008165 nir_j x 0.1906 [.., 0.2000] flagged → 0.2727 [0.167, 0.387] unflagged under ±0.5"; nir_h of that tile spins in Nautilus exploration (second case of 343381_8). RESUME: cd ~/Code/PyAutoLabs-wt/grid-offset-prior/euclid_strong_lens_modeling_pipeline; source ../activate.sh; pytest tests -q; /ship_workspace (Heart RED release-side → human ack); /prm; README one-hunk overlap with witt-wynne-catalogue #84. Full state on issue #88 comment."

## parameterization-prior-count
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1635
- issued: 2026-09-17
- prompt: active/parameterization_prior_count_blowup.md
- session: https://claude.ai/code/session_01TSJ72sveM7GrTcddMXzUkb
- status: library-shipped, awaiting-merge
- location: web-github (session clone /home/user/pyautofit, no task worktree; branch claude/parameterization-prior-count-blowup-jzsrj0)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1637
- shipped: 2026-09-17 (commit 97a92e6; full test_autofit 2813 passed / 48 skipped; pending-release label set; workspace impact none — option iii; autonomy_log row is /prm's at close-out)
- worktree: n/a — web-github session clone (/home/user/pyautofit)
- repos:
  - PyAutoFit: claude/parameterization-prior-count-blowup-jzsrj0
- note: "Autonomy: safe / Unattended: ready on the prompt; refactor cap is safe. Plan written to the issue and executed without a plan-approval hold (Fable plans, Opus executes); ends at PR-open, merge stays human via /prm. The timing witness (mge_group.py, 763,555 -> per-node calls, >= 5 s) needs autogalaxy_workspace_test and is the human's local re-run; in-session witnesses are the oracle byte-identity test and the path_instances_of_class call-count test."
- summary: |
    AbstractPriorModel.parameterization calls obj.prior_count on every prefix of
    every leaf path, and prior_count is a full subtree walk, so model.info costs
    O(leaves x subtree) (763,555 recursive calls on mge_group.py). Fix: a
    bottom-up, identity-memoised unique-prior set per node inside the single
    parameterization call; leaf listing and entry order untouched so the text
    is byte-identical. Oracle test keeps the old algorithm verbatim.

## demo-subplot-fit-interferometer-combined
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/555
- issued: 2026-09-17
- prompt: active/demo_subplot_fit_interferometer_combined.md
- session: https://claude.ai/code/session_0118fvTWLWaRT2b6eMtPdkqy
- status: awaiting-merge
- location: web-github (session clone /home/user/autolens_workspace, no task worktree)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/558
- worktree: n/a — web-github session clone; local-dev equivalent ~/Code/PyAutoLabs-wt/demo-subplot-fit-interferometer-combined
- repos:
  - autolens_workspace: claude/demo-subplot-fit-interferometer-docs-79u6vc
- note: "worktree_check_conflict demo-subplot-fit-interferometer-combined autolens_workspace exits 0 (PYAUTO_MAIN=/home/user). Docs / medium / Autonomy: safe; launched without --auto, so the plan on issue #555 awaits the human before implementation. Prompt premise corrected on the issue: the folder is scripts/multi_dataset/ (not multi/), and imaging_and_interferometer/ fits one interferometer + one imaging dataset, so the fit_list comes from the datacube reference cube (interferometer/features/datacube/), which is the case the library function was written for."
- summary: |
    Add an interferometer arc to scripts/multi_dataset/plot.py mirroring the imaging arc: load the
    datacube channels (auto-simulated by interferometer/features/datacube/simulator.py), fit each
    with its own tracer.json, and call aplt.subplot_fit_interferometer_combined(fit_list=...) on
    genuinely distinct fits; extend __Contents__ and __Visualizer__, add multi_dataset/plot.py to
    smoke_tests.txt, update the README line, regenerate the notebook.
    SHIPPED 2026-09-17 (web-github; Fable planned, Opus authored): PR #558 at b9894c7c, label
    pending-release; script exit 0 under the smoke profile (~12 s) against library mains, four
    distinct fits confirmed by a render probe; Heart CLI absent in the container so the smoke run
    stood as the gate. NEXT = /prm once CI is green.
