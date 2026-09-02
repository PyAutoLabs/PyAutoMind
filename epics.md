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
- cortex-half: PyAutoCortex/epics.md#jax-inference-profiling
- status: science half → Cortex 2026-09-01 (the whole programme's runs and rulings now live in
  PyAutoCortex `phases/inference_programme/`; the ledger stays at PROGRAMME.md and this entry
  stays the Mind's half — REWOUND to Phase 1, the InferenceRefs_v1 refs redo awaiting ruling)
- notes: DECISIONS.md (append-only gate log) and phase_<NN>_*/RESULTS.md sit beside the ledger; slices ship as autolens_profiling issues/PRs, not Mind prompts.
  REWOUND 2026-08-31 to Phase 1 (InferenceRefs_v1); mesh-pix runs quarantined to output/legacy_wrong, MGE to output/legacy (reusable pending batch review); redo runs step-by-step under batch-and-review; gates A/B1/B2 provisional; queue anchor autolens_profiling#200.

## cluster-strong-lensing
- title: Cluster strong lensing — Source & Cluster arc
- ledger: draft/feature/autolens/source_cluster_arc.md
- cortex-half: PyAutoCortex/epics.md#cluster-strong-lensing
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
  NOT a root-cause fix: why the pool wedges is still unknown — follow-up never filed (the resume
  door was never written).
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
- cortex-half: PyAutoCortex/epics.md#graphical-ep
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
- cortex-half: PyAutoCortex/epics.md#euclid-dr1-prep
- status: science half → Cortex 2026-09-01 (old phases 4, 5, 6a, 6b are now PyAutoCortex
  `phases/euclid/` 4, 5, 6, 7); the Mind keeps the software phases, renumbered 3a→3, 3b→4,
  6c→8, 7→9 — the renumbering table is in the ledger
- notes: 7 Mind phases (0, 1, 2, 3, 4, 8, 9) — issue ONE at a time as predecessors near
  shipping, no bulk issue queues. The four science phases moved to PyAutoCortex on
  2026-09-01 as `phases/euclid/` 4, 5, 6, 7 (were Mind 4, 5, 6a, 6b): RAL runs, human-driven
  and supervised, whose deliverable is a result and a written verdict, not a merged PR;
  never route them to an autonomous ship gate. Mind phase 8 (was 6c) is a PyAutoArray source
  audit that may spawn a separate bug prompt and can run alongside Cortex phase 7. Mind
  phase 9's (was 7) retroactive-update leg is explicitly allowed to conclude "no elegant
  solution — don't build it". The full renumbering table is in the ledger. Source of truth for all drift is /mnt/c/Users/Jammy/Science/euclid.
  Phase 0 shipped 2026-08-28; phase 1 shipped 2026-08-29 (euclid#43 closed, PR #44
  merged); phase 2 shipped 2026-08-29 (euclid#45 closed, PR #46 merged) — which also
  satisfies phase 4's "2 strongly preferred" gate. Phase 3a was INSERTED 2026-08-31
  (docs: restore the in-script narrative prose lost at 355b309; start_here.py back to a
  full end-to-end guide) and the old phase 3 renumbered to 3b; on 2026-09-01 the letters
  died in the Cortex split and 3a/3b became plain 3/4. Next is phase 3
  (draft/docs/euclid/restore_pipeline_narrative_prose.md).

## two-slot-batching
- title: Two slots a day — the batch workflow
- ledger: draft/feature/pyautomind/two_slot_batching_epic.md
- status: phase 2 `collect` SHIPPED 2026-09-02 (PyAutoBrain#332, complete/2026/09/batch-collect.md); `plan` shipped 2026-08-30; `slice` re-filed as draft/feature/pyautobrain/batch_slice.md
- notes: 11 phased prompts (0a/0b/0c, then 1-8) across draft/feature/pyautomind/,
  draft/feature/pyautobrain/ and draft/research/euclid/ — issue ONE at a time, no
  bulk issue queues. Ordered by value, not build dependency: the DISPATCHER
  (phase 5) is the least important part and is deliberately late, because phases
  0-4 can all be driven by hand in the slot using the chips the dashboard already
  renders. Phase 0 (the review-cost model: consequence tier, witness,
  review-minutes) is the foundation everything else is sized against, and was
  split into 0a/0b/0c on 2026-08-30 after the Feature Agent derived too-large
  (score 11) and recommended phasing — the epic's own slicing rule firing on its
  own prompt. 0b's distribution is a dry run so the infer_autonomy change is
  reviewable on its numbers before 0c touches 137 files. Phases 3
  and 4 are doctrine edits marked human-required — phase 3 fixes the ship gate
  for unattended conditions (Heart at 3am, what a batch launch is, an
  independent-model adversarial leg, capped decide-and-flag, a
  `rejected-at-review` outcome); phase 4 is the tier-A auto-merge decision — the
  human chose 2026-08-30 to SHADOW it for four weeks (window closes 2026-09-27)
  against a pre-registered rule, and stage-1 rows are already being appended to
  autonomy_log.md, so the window runs in parallel and is not on the critical
  path. It is the ONLY phase that reduces total attention rather than re-timing
  it, and its ceiling is ~17% of throughput (56 of 332 August records touch organ
  repos only; 125 name no PR at all and are judgement-shaped by nature). Supersedes/absorbs
  draft/feature/pyautomind/bundle_nightly_claude_pass.md (parked 2026-08-27 for
  want of a driver — this epic is the driver).

## ci-timing-fast-tests
- title: CI test timing — finish the board, fast physical tests
- ledger: draft/feature/pyautoheart/ci_timing_fast_tests_epic.md
- notes: 9 phased prompts (1-9) — finish the timing board (smoke-timings ingester, permanent history in PyAutoHeart, dead unit-test/import/testmode legs live), snapshot a LEGACY timing round, then the _test physical+fast rebuilds (autogalaxy rehearses, autolens follows; one pin-regeneration wave each), CI caches, user-workspace/HowTo pass, and a source hot-spot census. ALL other source/workspace development is paused while this epic runs (stable state of truth; pin changes validated by unit tests + developer/profiling workspaces). Issue ONE phase at a time — no bulk issue queues. Design doc: docs/pyautoheart/test_performance_board_assessment.md (Planes B/C are phases 1-2).

## cortex-birth
- title: PyAutoCortex — the science organ: split science runs out of the Mind
- ledger: complete/archive/epics/cortex_birth_epic.md
- status: SHIPPED 2026-09-02 — all seven phases (0–6) complete. Records: complete/2026/09/cortex-birth-organ-row.md, cortex-schema-skeleton.md, cortex-conductor.md, cortex-registration.md, cortex-migration.md (phases 0–4, 2026-09-01: #377, #379, #380, #382, #383), cortex-batch-member-kind.md (phase 5, PyAutoBrain#334), cortex-public-surfaces.md (phase 6, PyAutoMind#385). The retrospective is a stub in the ledger until the first Cortex batch closes with a review through the phase-5 door; the deferred list is recorded there.
- notes: 7 phased prompts (0-6) under draft/feature/pyautocortex/ — issue ONE at a
  time, no bulk issue queues. Phase 0 is human-gated (the repo is created by hand;
  no birth path exists). Decided 2026-09-01: new organ PyAutoCortex, a run/ruling
  registry NOT a second Mind; rulings of record live in the Cortex (Option A);
  gates are GitHub refs declared Cortex-side; Science-folder projects get private
  PyAutoLabs remotes (code/config/wiki/witness only, no Euclid data). Migration
  (phase 4) moves euclid-dr1-prep 4/5/6a/6b, jax-inference-profiling whole,
  graphical-ep 3/4 science halves, cluster arc phase 11 and the subhalo active
  entry across, with reciprocal links by slug. Supersedes two-slot-batching
  phase 8 (batch_science_lane) and absorbs queue.md #2 on the science side;
  phase 5 is gated on two-slot-batching's `collect` verb.
