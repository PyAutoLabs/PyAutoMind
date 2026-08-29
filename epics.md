# Epics

Long-running multi-phase programmes — work that is bigger than any one task
and outlives any single issue. Each entry names the epic's canonical
**ledger**: the file that holds its phase/gate state, wherever it lives. The
dashboard renders these under In flight with a one-tap resume prompt that
works out where the epic stands from its ledger and continues it from the
next logical point — nobody should have to hunt for the issue that pairs
with an epic's current phase.

Schema per entry: `## <slug>` then `- title:` / `- ledger:` / `- notes:`
(and optionally `- status:` for a coarse, durable state — never per-phase
detail, which belongs in the ledger).

A member prompt declares its membership in its own header: `Epic: <slug>`
(this file's slug) plus an optional `Phase: <n>`. The dashboard then keeps
members out of the pick lists and work-type sections and shows them only
grouped, phase-ordered, under their epic — worked in order through the
epic, never picked standalone.

## jax-inference-profiling
- title: JAX profiling — inference programme
- ledger: autolens_profiling/results/notes/inference/PROGRAMME.md
- notes: DECISIONS.md (append-only gate log) and phase_<NN>_*/RESULTS.md sit beside the ledger; slices ship as autolens_profiling issues/PRs, not Mind prompts.

## cluster-strong-lensing
- title: Cluster strong lensing — Source & Cluster arc
- ledger: draft/feature/autolens/source_cluster_arc.md
- notes: 12 phased prompts under draft/; issue phases ONE at a time as predecessors near shipping — no bulk issue queues.

## jax-compile-stall
- title: JAX vmap result never materialises (was: "intermittent XLA compile stall" — the name was wrong)
- ledger: draft/bug/ci/jax_vmap_jit_compile_stall.md
- status: SHIPPED 2026-08-27 — all 3 phases done; record
  complete/2026/08/jax-vmap-materialisation-hang.md. Root cause is XLA CPU's multithreaded Eigen
  thread pool; workaround XLA_FLAGS=--xla_cpu_multi_thread_eigen=false in both test workspaces'
  smoke AND release profiles (ABAB: 12 pass/0 hang with vs 2 pass/14 hang without, Fisher p~3e-6).
  All 7 quarantined entries restored, 42/42 completions. PyAutoFit#1528, PRs PyAutoFit#1529,
  PyAutoHands#269, autolens_workspace_test#281, autogalaxy_workspace_test#114.
  NOT a root-cause fix: why the pool wedges is still unknown — follow-up filed under draft/research/ci/.
- NEW EVIDENCE 2026-08-25: multi_dataset/jax_likelihood/shared_preloads.py stalled at TIMEOUT (300s) in
  PyAutoHeart Workspace Smoke run 32902243623 — one day after the 2026-08-24 retime refuted its SLOW
  marker and returned it to mega-run coverage. N=5 per leg measures the fast mode of a bimodal failure
  and says nothing about the tail, so every entry that sweep readmitted carries the same uncertainty.
  Also the epic's first occurrence via the weekly workspace-validation channel (cross-harness
  corroboration), and smoke_tests.txt vs no_run.yaml now disagree about this script. Nothing parked.
  See the ledger's "New occurrence — 2026-08-25" section; surfaced by
  complete/2026/08/weekly-smoke-timings-naming.md.
- CORRECTION (post-close-out): the captured stack shows the hang is in jax.block_until_ready, NOT in
  compilation. The epic's name and every marker calling this an "XLA compile stall" are wrong. Resume
  from "why does block_until_ready never return", not from compiler behaviour.
- notes: phase 1 (watchdog) shipped in full; phases 2/3 stopped deliberately at a measured-but-not-root-caused state. The stall is instrumented and characterised (>100x bimodality inside one compile step; vmap-of-jit contributory at p=0.070 but NOT causal; the compile-cache hypothesis never tested) and NOTHING was un-quarantined. Resumed 2026-08-27 as phase 3 (PyAutoFit#1528) — NOT via draft/research/ci/smoke_timing_and_profiling.md,
  which the 2026-08-23 close-out named as the resume door but which was never written. Superseded complete/2026/08/multi-dataset-jax-likelihood-xla-stall.md (was draft/bug/autolens_workspace_test/multi_dataset_jax_likelihood_xla_stall.md).

## graphical-ep
- title: Expectation propagation (EP) campaign
- ledger: draft/research/graphical_ep/ep_campaign.md
- notes: umbrella phase map — each phase's real content lives in its own prompt under draft/research/graphical_ep/; the campaign file itself is never issued.

## numba-cpu-likelihood
- title: Numba CPU sparse-operator likelihood — speed restoration
- ledger: complete/2026/08/numba-cpu-mge-batch-convolve-cache.md
- status: COMPLETE 2026-08-28. phase 1 SHIPPED 2026-08-27; phase 2a CLOSED as superseded (Bilinear rank-CDF is every default since PyAutoArray#462; the kernel-CDF/RTU path got its numba kernel in #458 and is GPU-only territory — complete/2026/08/numba-cpu-kernel-cdf-fast-path.md); phase 2b SHIPPED 2026-08-21 (backfilled); phase 3a SHIPPED 2026-08-28 (PyAutoArray#501, autolens_profiling#184); 3b NOT filed — only the cold path motivates it. Successor: HST-resolution speed-up (curvature matrix F), filed separately
- notes: Profiling shipped (autolens_profiling#151, complete/2026/08/numba-cpu-likelihood-profiling.md);
  first-call garbage bug shipped (complete/2026/08/numba-first-call-garbage-psf-weighted-data.md).
  Phase 1 = MGE batched convolution + operated-matrix caching + Convolver state reuse (PyAutoArray#497,
  PyAutoGalaxy#588). Phase 2a = kernel-CDF numba fast path
  (complete/2026/08/numba-cpu-kernel-cdf-fast-path.md — superseded by #462 + #458). Phase 2b = fnnls in-place Cholesky buffer (PyAutoArray#453/#463,
  complete/2026/08/numba-fnnls-inplace-cholesky-buffer.md — shipped untracked, backfilled). Phase 3 =
  active-set ITERATION reduction for the positive-only solve (the 72-78% Delaunay term is iteration-bound,
  not linear-algebra-bound): 3a = complete/2026/08/numba-cpu-nnls-iteration-reduction.md (PyAutoArray#498 → #501, autolens_profiling#184; random-walk iterations 9.9x/4.0x fewer; post-#497 the solve is 40%/17% of an eval — at hst the curvature matrix F now dominates);
  3b = batched active-set moves — 3a's matrix (autolens_profiling results/notes/nnls_warm_start_memo_matrix.md) shows it only pays on the cold / i.i.d. path (30-95 outer iterations); file only for that regime.
  NOTE the "restore the deleted numba fnnls" idea is RETIRED (#151 comment 5) — do not re-file it.
  Measurement prerequisite for every phase: draft/feature/autolens_profiling/numba_breakdown_harness_memo_blind.md.
  One issue at a time, never a bulk queue.

## euclid-dr1-prep
- title: Euclid DR1 preparation — 15k-lens modelling prep
- ledger: draft/feature/euclid/euclid_dr1_prep_epic.md
- notes: 10 phased prompts under draft/ (0, 1, 2, 3, 4, 5, 6a, 6b, 6c, 7) — issue ONE at a
  time as predecessors near shipping, no bulk issue queues. Phases 4-6b are science runs
  on RAL (HPC, human-driven, supervised) whose deliverable is a result and a written
  verdict, not a merged PR; never route them to an autonomous ship gate. Phase 6c is a
  PyAutoArray source audit that may spawn a separate bug prompt and can run alongside 6b.
  Phase 7's retroactive-update leg is explicitly allowed to conclude "no elegant solution
  — don't build it". Source of truth for all drift is /mnt/c/Users/Jammy/Science/euclid.
  Phase 0 shipped 2026-08-28; phase 1 shipped 2026-08-29 (euclid#43 closed, PR #44
  merged) — phases 2, 3 and 4 are now unblocked.
