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

## fixed-light-hardware
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/253
- issued: 2026-09-13
- prompt: active/fixed_light_cpu_and_consumer_gpu.md
- session: claude --resume session_018oyeoiMrc8vhhahAyA1VNP
- status: awaiting-merge (PR open under Heart RED with human authorisation 2026-09-13; merge is human, and stacked PRs #250 then #252 merge first)
- worktree: ~/Code/PyAutoLabs-wt/fixed-light-hardware
- epic: fixed-lens-light-profiling phase 2
- repos:
  - autolens_profiling: feature/fixed-light-hardware
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/254
- parallel-claim: "worktree_check_conflict fixed-light-hardware autolens_profiling exits 1 on two claims, both of them earlier phases of this same epic and both frozen at PR-open: fixed-lens-light-source-only (#248, PR #250 against main, branch at 319f078) and fixed-light-library-path (#251, PR #252 against #250s branch, at b8fac8a). Neither expects further edits. This task is deliberately STACKED on the second of them (base feature/fixed-light-library-path, not main) because the cell, the injection module and the S3 builder it runs exist only there - a stack of three, each branch the parent commit of the next, so they cannot conflict. Registered as a parallel claim in a fresh worktree, the same call #251 itself recorded against #248."
- summary: |
    Phase 2 of the fixed-lens-light-profiling epic. Phase 1s cell
    scripts/imaging/likelihood_breakdown/fixed_light_library.py is run on three more
    hardware legs - JAX-CPU at two thread settings (1 and 8), RTX 2060 fp64, RTX 2060
    mixed precision - on the same six routes, three meshes and HST dataset as the A100
    legs, so the tables stack into one per-hardware comparison. Adds a CPU-appropriate
    kernel row set (the librarys own numpy fnnls NNLS, scipy cho_factor/cho_solve
    unconstrained, and the numpy certified active set) as the CPU production candidate.
    Pins are re-derived per precision: the fp64 legs assert, the mixed-precision leg
    asserts nothing calibrated in fp64 and records the fp32 evidence delta, the pass
    counts and the negative-pixel counts instead. Thread counts (both the XLA NPROC pool
    and the BLAS knobs) recorded on every CPU timing. No PyAutoArray change.

- note: shipped 2026-09-13 — cell gains --pins {fp64,none} + a machine block + tau_rel re-derived per precision, new fixed_light_cpu_kernels module and cell, 22 tests (suite 246). 19 local legs on the laptop (i9-10885H/WSL2/16 GB; RTX 2060 6 GB), one at a time, fresh JAX cache each. Certified active set wins everywhere and the prize shrinks with the hardware: a -> d is 2.03x/2.56x/2.01x on the A100, 1.28x/1.48x/1.46x on the RTX 2060, 1.83x/1.74x/1.35x on 8 CPU threads, 1.16-1.22x on one. The GeForce fp64 penalty never bit - mixed precision buys 5-8 % for <= 2.5e-3 nats and 16 % more VRAM, so fp64 stays the consumer path. MEMORY is the consumer wall and it invalidates the batched design: @vmap 16 needs 11.88 GiB, batch 4 OOMs, batch 2 is slower than a single call, and the same shape OOM-killed the 16 GB host. On the CPU the A100 kernel result does not transfer - the numpy certified active set does not beat the library's own fnnls NNLS, and both are 1.9-3.6x slower at 8 BLAS threads than at 1. Note results/notes/fixed_lens_light_hardware_2026_09.md. PR #254 is STACKED (base feature/fixed-light-library-path) - merge #250, then #252, then /prm this one. Next is epic phase 3 (low-likelihood draws).

## fixed-light-draws
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/255
- issued: 2026-09-13
- prompt: active/fixed_light_certified_low_likelihood_draws.md
- session: claude --resume session_018oyeoiMrc8vhhahAyA1VNP
- status: awaiting-merge (PR open under Heart RED with human authorisation 2026-09-13; merge is human, and stacked PRs #250, #252 then #254 merge first)
- worktree: ~/Code/PyAutoLabs-wt/fixed-light-draws
- epic: fixed-lens-light-profiling phase 3
- repos:
  - autolens_profiling: feature/fixed-light-draws
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/256
- parallel-claim: "worktree_check_conflict fixed-light-draws autolens_profiling exits 1 on three claims, all of them earlier phases of this same epic and all frozen at PR-open: fixed-lens-light-source-only (#248, PR #250 against main, at 319f078), fixed-light-library-path (#251, PR #252 against #250s branch, at b8fac8a) and fixed-light-hardware (#253, PR #254 against #252s branch, at 86af7d7). None expects further edits. This task is deliberately STACKED on the third of them (base feature/fixed-light-hardware, not main) because the draw-set cell reuses the S3 builder, the certified kernels and the cell conventions that exist only there - a stack of four, each branch the parent commit of the next, so they cannot conflict. Registered as a parallel claim in a fresh worktree, the same call #251 recorded against #248 and #253 recorded against both."
- summary: |
    Phase 3 of the fixed-lens-light-profiling epic. Every certified active-set timing so
    far (4.2 ms Delaunay at pass 2, 11 ms rect at pass 7) was measured at the fiducial
    model, essentially the truth after SLaM light[1]. The certified scheme's cost IS its
    pass count, so a good model may simply have an easy active set. This phase builds a
    graded draw set of deliberately poor models - one-parameter walks in einstein_radius,
    ell_comps_0, centre_x and the mass slope (PowerLaw promotion at slope 2.0, since the
    fiducial mass is Isothermal), each bisected to land at delta log L about -10, -100,
    -1000 and -1e4, plus 24 seeded random draws from SLaM-like priors at 5x the prior
    sigma - and measures, per draw per mesh, certified pass count and ms, PDIP iterations
    and ms, seed-set size, and the unconstrained solve's delta log-evidence. The
    deliverable is the FALLBACK RATE at fixed pass budgets 2 / 4 / 6 (and 7 for rect):
    the number that decides whether a fixed budget is safe in production. New cell
    scripts/imaging/likelihood_breakdown/fixed_light_draws.py plus an importable
    fixed_light_draws_steps module and its tests; a CPU leg locally and two A100 legs
    (rect, Delaunay) on gpu-2. No PyAutoArray change.

- note: shipped 2026-09-13 — new cell scripts/imaging/likelihood_breakdown/fixed_light_draws.py plus an importable fixed_light_draws_steps module and 30 numpy tests (suite 286). Four legs on the same seeded 41-model draw set: A100 343011 (rect, 00:07:49) and 343012 (Delaunay, 00:08:51) on gpu-2 with every fiducial pin PASS, plus two local JAX-CPU legs at 8 threads. THE PHASE-0 PASS BUDGETS DO NOT HOLD: Delaunay's pass 2 falls back on 67.5 % of the draw set (95.8 % of the random draws) and rectangular's pass 7 on 27.5 %; the smallest zero-fallback budgets are 7 (Delaunay) and 11 (rectangular), so phase 4 must sweep those, not 2 and 7. The two meshes fail oppositely - the pass count GROWS with model error on Delaunay (Spearman +0.698) and FALLS on rectangular (-0.535), because a worse model has a bigger active set that pass 0's 152-pixel edge-zero seed already mostly finds. The lever survives at about half its fiducial headline (median 2.6x / 5.4x over PDIP on the A100; the worst certified draw still beats the best PDIP call) and PDIP's own cost barely moves with the model (15->17, 17->21 iterations), so budget-plus-fallback stays a bounded worst case. Pass counts, PDIP iterations and seed-set sizes are IDENTICAL on the A100 and the CPU for all 41 draws, so the fallback rate is a property of the problem. Dropping positivity is now unambiguously out: the A2 error grows to +4.07e4 nats (rect) / +6339 (Delaunay). Note results/notes/fixed_lens_light_low_likelihood_draws_2026_09.md. PR #256 is STACKED (base feature/fixed-light-hardware) - merge #250, then #252, then #254, then /prm this one. Next is epic phase 4 (source-pixel scaling).

## fixed-light-scaling
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/257
- issued: 2026-09-13
- prompt: active/fixed_light_source_pixel_scaling.md
- session: claude --resume session_018oyeoiMrc8vhhahAyA1VNP
- status: awaiting-merge (PR open under Heart RED with human authorisation 2026-09-13; merge is human, and stacked PRs #250, #252, #254 then #256 merge first)
- worktree: ~/Code/PyAutoLabs-wt/fixed-light-scaling
- epic: fixed-lens-light-profiling phase 4
- repos:
  - autolens_profiling: feature/fixed-light-scaling
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/258
- parallel-claim: "worktree_check_conflict fixed-light-scaling autolens_profiling exits 1 on four claims, all of them earlier phases of this same epic and all frozen at PR-open: fixed-lens-light-source-only (#248, PR #250 against main), fixed-light-library-path (#251, PR #252 against #250s branch), fixed-light-hardware (#253, PR #254 against #252s branch) and fixed-light-draws (#255, PR #256 against #254s branch, at cf9f95e). None expects further edits. This task is deliberately STACKED on the fourth of them (base feature/fixed-light-draws, not main) because the kernel cell, the S3 builder, the certified kernels and the phase-2 precision switches it ports exist only there - a stack of five, each branch the parent commit of the next, so they cannot conflict. Registered as a parallel claim in a fresh worktree, the same call #251 recorded against #248, #253 against both and #255 against all three."
- summary: |
    Phase 4 of the fixed-lens-light-profiling epic. Every fixed-lens-light number so far
    is at ONE source-pixel count (1521 rect / 1500 Delaunay), and the three solvers scale
    differently - the unconstrained Cholesky is one factorisation, the certified active
    set is a masked full-size Cholesky PER PASS, and PDIP is an iteration count times a
    solve. This phase sweeps N in {500, 1000, 1500, 2500, 4000} on rect and Delaunay, HST,
    over four hardware legs (A100 fp64 with vmap 16, RTX 2060 fp64, RTX 2060 mixed
    precision, JAX-CPU at NPROC 8 with BLAS pinned to 1), with the phase-0 kernel cell
    fixed_light.py gaining the phase-2 switches (--pins, the machine block, the re-derived
    tau_rel). Per phase 3 the certified row is timed at the SAFE budgets 11 (rect) and
    7 (Delaunay) as well as at whatever budget certifies at that N. A leg that OOMs or
    times out is a result, not a gap. Deliverable: ms-vs-N tables and a log-log figure per
    hardware, fitted scaling exponents, the memory ceiling per hardware, and the
    affordable N per hardware that feeds phase 5.

- note: shipped 2026-09-13 — cell fixed_light.py gains --pins {fp64,none}, --safe-budget, a machine block and tau_rel re-derived per precision (defaults byte-identical to phase 0, asserted by a test); new scripts/misc/likelihood_breakdown/fixed_light_scaling_table.py and 62 tests (suite 348); two five-arm A100 arrays and their launcher. 40 legs at --source-pixels 500/1000/1500/2500/4000 on rect and Delaunay: A100 arrays 343023/343024 on gpu-2 (10/10 COMPLETED 0:0, autotune 0, both fiducial arms' pins PASS) plus 30 local legs (RTX 2060 fp64, RTX 2060 mp, JAX-CPU at NPROC 8 / BLAS 1). None OOMed, none timed out. THE CERTIFYING PASS BUDGET DOES NOT SCALE WITH N: rect certifies at 5/8/7/10/6 and Delaunay at 1/1/2/1/2 with no trend over a factor eight in pixels, worst case 10, inside phase 3's safe budget of 11 — so phase 5 can fix 11/7 and sweep N freely (phase 0's '6 at 3025 vs 7 at 1521' was noise). The certified active set leads at every N on every hardware: 1.44-1.62x over S3 PDIP on rect and 2.21-3.00x on Delaunay (A100), and on Delaunay the lever GROWS with N because PDIP climbs 14->20 iterations while the budget stays at 7. PHASE 1'S BATCHED ROW HAS AN N CEILING: @vmap 16 amortises 3.64x at N~500, 1.14x at 2500 and 0.68x — a penalty — at 4000, on an 80 GB A100 at 7.8 GB, so batch size must be chosen from N rather than inherited from n_batch. Memory is not the wall: the 6 GB card fits the single call at ~4000 pixels (3.13 GB fp64 / 3.63 GB mp, ~2.9 GB spare) and the A100 uses 7.8 of 80 GB with 16 lanes — phase 2's consumer wall is specific to the batched shape. Time ends every curve: affordable N is 4000 (A100) / 1500 (RTX 2060) / 1000 (JAX-CPU); the S3 call crosses 1 s at N~1846 (RTX rect) and ~912 (CPU rect) and 100 ms on the A100 at N~3261/2645. New for the next epic: on the A100 every solver row fits alpha~1 (launch/bandwidth-bound) while the dense F+lambdaH build fits alpha~1.69 and OVERTAKES the certified solve between 2500 and 4000 pixels — the next GPU lever is the assembly, not the solver. Positivity gets more necessary with resolution (+318->+368 nats, 62->252 negatives on rect). Note results/notes/fixed_lens_light_source_pixel_scaling_2026_09.md. PR #258 is STACKED (base feature/fixed-light-draws) - merge #250, then #252, then #254, then #256, then /prm this one. Next is epic phase 5 (HST + Euclid verdict).

## fixed-light-verdict
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/259
- issued: 2026-09-13
- prompt: active/fixed_light_likelihood_assessment_hst_euclid.md
- session: claude --resume session_018oyeoiMrc8vhhahAyA1VNP
- status: awaiting-merge (PR open under Heart RED with human authorisation 2026-09-13; merge is human, and stacked PRs #250, #252, #254, #256 then #258 merge first)
- worktree: ~/Code/PyAutoLabs-wt/fixed-light-verdict
- epic: fixed-lens-light-profiling phase 5 (the last)
- repos:
  - autolens_profiling: feature/fixed-light-verdict
- parallel-claim: "worktree_check_conflict fixed-light-verdict autolens_profiling exits 1 on five claims, all of them earlier phases of this same epic and all frozen at PR-open: fixed-lens-light-source-only (#248, PR #250 against main), fixed-light-library-path (#251, PR #252 against #250s branch), fixed-light-hardware (#253, PR #254 against #252s branch), fixed-light-draws (#255, PR #256 against #254s branch) and fixed-light-scaling (#257, PR #258 against #256s branch, at efdfb13). None expects further edits. This task is deliberately STACKED on the fifth of them (base feature/fixed-light-scaling, not main) because the library-path cell, the solver injection, the S3 builder and the phase-3/4 safe budgets it runs exist only there - a stack of six, each branch the parent commit of the next, so they cannot conflict. Registered as a parallel claim in a fresh worktree, the same call #251 recorded against #248, #253 against both, #255 against all three and #257 against all four."
- summary: |
    Phase 5 of the fixed-lens-light-profiling epic, and the verdict the human asked for:
    for each hardware type, what the WHOLE likelihood function costs on real survey data
    with the lens light fixed, and which configuration production should use. The grid is
    the library path (AnalysisImaging.log_likelihood_function under jit) on HST (0.05")
    and Euclid (0.1") at 500 / 1250 / 2500 source pixels, over A100 fp64, RTX 2060 fp64,
    RTX 2060 mixed precision and JAX-CPU at 8 threads, for routes a (S0 today), b (S3
    PDIP reference), c (S3 unconstrained) and d (S3 certified active set at phase 3's
    production-safe budget 11 rect / 7 Delaunay with PDIP fallback). Euclid has no pins,
    so its log-dets and evidences are RECORDED as the first Euclid reference, never
    asserted. Deliverable: results/notes/fixed_lens_light_verdict_2026_09.md - the
    2 x 3 x hardware table per solver and a written production configuration per hardware
    (solver, budget + fallback, precision, affordable N) with every shortcut's cost in
    nats; the follow-ups it implies go to ideas.md as bullets, not new prompts.

- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/260
- note: shipped 2026-09-13 — the epic's VERDICT. Cell fixed_light_library.py gains --dataset {hst,euclid} (default hst byte-identical; it selects the INSTRUMENTS preset and nothing else and refuses a disagreeing --instrument), --pass-budget auto (route d at phase 3's PRODUCTION budget while the sweep records the budget that certifies at this dataset/mesh/N), --routes a,b,c,d, and a reference_recorded block for every configuration no pin covers; 30 tests (suite 398). 24 local legs, all rc=0, no timeouts, 45 min: Delaunay x {hst,euclid} x {500,1250,2500} on RTX 2060 fp64, RTX 2060 mp and JAX-CPU (NPROC 8 / BLAS 1), plus 6 rectangular RTX fp64 legs added when the A100 could not be reached. THE 12 A100 LEGS WERE NOT RUN — the RAL jump host refused publickey all session and the direct route times out; the four arrays are written, validated and committed and resume with one command (hpc/batch_gpu/submit_fixed_light_verdict.sh --node euclid-ral-gpu-2). EUCLID IS WHERE POSITIVITY EARNS ITS KEEP: dropping it costs +3.5 -> +24.3 -> +109.1 nats as N goes 500 -> 2500 on Euclid against a FLAT +8.4 -> +6.4 on HST (129 negative source pixels vs 6), because at N=2500 Euclid has 1.5 image pixels per source pixel where HST has 6.1 — the trend with N reverses between the datasets and every earlier phase measured this shortcut on HST alone. The certified active set is the production solver on every hardware and both datasets (1.20-1.59x over the library today on HST, 1.43-2.28x on Euclid where the lead GROWS with N) and returns the library's own answer (every equivalence pin PASS, max 5.6e-10), so its cost in nats is ZERO. THE PASS BUDGET IS DATASET-DEPENDENT: rectangular certifies at 6/9/11 passes on Euclid against 5/7/10 on HST, exhausting phase 3's safe budget of 11 exactly at N=2500 from a single model — Delaunay keeps its margin (Euclid 2/4/4, HST 1/2/1, budget 7) and stays the production mesh. Memory is not a wall (2.70 GB of 6 GB worst) and mixed precision buys 4-9 % for <= 1.3e-4 nats with an identical certifying budget on Delaunay, so fp64 stays the path. Production configuration stated per hardware with affordable N: 4000 HST (A100, carried from phase 4) / 1500 HST + 2500 Euclid (RTX 2060) / 1000 HST + 1250 Euclid (8 CPU threads). Two independent ties back to phase 4 (2241 vs 2225 ms; +318.00/+347.11 vs +318.0/+347.1 nats). Note results/notes/fixed_lens_light_verdict_2026_09.md. Five follow-ups filed as ideas.md bullets (library implementation of the certified solver, the matched-injection witness, the Delaunay assembly as the next GPU lever, re-deriving the rectangular budget on Euclid, and the unrun A100 legs). PR #260 is STACKED (base feature/fixed-light-scaling) - merge #250, #252, #254, #256, #258, then /prm this one. This is the LAST phase: the fixed-lens-light-profiling epic is COMPLETE pending merge of the stack.

## model-figures-rollout-lens
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/542
- issued: 2026-09-13
- prompt: active/model_figures_6b_lens_surfaces.md
- session: claude --resume session_01DLx38vS6F1M7K5LnpVbeZ7
- status: wave 1 MERGED (HowToLens#81, autolens_workspace#543); wave 2 (autolens_workspace PR B) in flight on feature/model-figures-rollout-lens-b
- worktree: ~/Code/PyAutoLabs-wt/model-figures-rollout-lens
- epic: model-figures phase 6b
- release-gate: PyAutoFit
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/81 (merged 635ee49ab155537dcc91dea09237c955408d9431)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/543 (merged c8b7254830da5f4a0908b561296a30654b884ae4)
- repos:
  - autolens_workspace: feature/model-figures-rollout-lens-b
  - HowToLens: feature/model-figures-rollout-lens
- note: "worktree_check_conflict model-figures-rollout-lens autolens_workspace HowToLens exits 0 (2026-09-13, after the stale remove-fits-dataset-plots-yaml claim was closed out). Plan approved in Plan Mode 2026-09-13; SLaM deferred to 6b2; autolens_workspace ships as two PRs (A: guides/imaging/point_source/multi_dataset; B: interferometer/group/multi_galaxy/cluster/weak on feature/model-figures-rollout-lens-b after A merges); release-gate PyAutoFit because guides/modeling/advanced/expectation_propagation.py uses EPResult.factor_graph (merged 6a, unreleased)."

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
  - autofit_assistant: feature/howtofit-mode
  - HowToFit: feature/howtofit-mode
  - autofit_workspace: feature/howtofit-mode
  - PyAutoFit: feature/howtofit-mode
- prompt: active/howtofit_mode.md
- summary: Assistant implementation ready and reviewed; approved README prompt propagation to HowToFit, autofit_workspace and PyAutoFit in progress. Shipping held by Heart YELLOW pending human acknowledgement.
- ship-hold: |
    Workspace validation: 3 failures (cloud#34824535982).
    Manifest drift: organism-map 2; public front-door 2.
    Profiling drift: three matrix_free SLQ fp64 results — delaunay_hpc_a100,
    delaunay_nn_hpc_a100, rectangular_hpc_a100.
- next: Acknowledge these Heart YELLOW reasons before ship_workspace; source remains local and uncommitted.
