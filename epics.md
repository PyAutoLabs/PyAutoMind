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

An entry whose `status:` **begins** SHIPPED or COMPLETE is retired by
`lifecycle.py epics --retire` (run by `dashboard_refresh.yml` on main): its
ledger moves to `complete/archive/epics/` if it was under `draft/` or
`active/`, the entry's text is appended there, and the entry is deleted from
this file.

A member prompt declares its membership in its own header: `Epic: <slug>`
(this file's slug) plus an optional `Phase: <n>`. The dashboard then keeps
members out of the pick lists and work-type sections and shows them only
grouped, phase-ordered, under their epic — worked in order through the
epic, never picked standalone.

## cluster-strong-lensing
- title: Cluster strong lensing — Source & Cluster arc
- ledger: draft/feature/autolens/source_cluster_arc.md
- notes: 12 phased prompts under draft/; issue phases ONE at a time as predecessors near shipping — no bulk issue queues. Science half: the PyAutoCortex project ledger of the science project it births (arc phase 11).

## graphical-ep
- title: Expectation propagation (EP) campaign
- ledger: draft/research/graphical_ep/ep_campaign.md
- notes: umbrella phase map — each phase's real content lives in its own prompt under draft/research/graphical_ep/; the campaign file itself is never issued. Science half: PyAutoCortex `projects/{analytic_gaussian,ep_toy_gaussian,slope_hierarchy_scale,ic50_workspace}.md` (campaign phases 1b, 3 and 4).

## euclid-dr1-prep
- title: Euclid DR1 preparation — 15k-lens modelling prep
- ledger: draft/feature/euclid/euclid_dr1_prep_epic.md
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
  solution — don't build it". The full renumbering table is in the ledger. Source of truth for
  all drift is /mnt/c/Users/Jammy/Science/euclid. Science half: PyAutoCortex
  `projects/euclid_dr1_prelim.md` (the former Cortex phases 4-7).
  Phase 0 shipped 2026-08-28; phase 1 shipped 2026-08-29 (euclid#43 closed, PR #44
  merged); phase 2 shipped 2026-08-29 (euclid#45 closed, PR #46 merged) — which also
  satisfies phase 4's "2 strongly preferred" gate. Phase 3a was INSERTED 2026-08-31
  (docs: restore the in-script narrative prose lost at 355b309; start_here.py back to a
  full end-to-end guide) and the old phase 3 renumbered to 3b; on 2026-09-01 the letters
  died in the Cortex split and 3a/3b became plain 3/4. Phase 3 shipped 2026-09-01
  (euclid#47 closed, PR #48 merged; record
  complete/2026/09/restore-pipeline-narrative-prose.md). Phase 4 shipped 2026-09-03
  (euclid#49 closed, PR #50 merged; record complete/2026/09/euclid-cpu-two-stage-route.md) —
  all Mind software phases 0-4 are now shipped, and both gates of the Cortex 10-lens science
  run (euclid#48, euclid#49) are closed. Phase 8 (Delaunay area audit) shipped 2026-09-04
  (PyAutoArray#522 closed, PR #523 merged, audit on the issue; record
  complete/2026/09/delaunay-area-magnification-audit.md): two defects proven and filed as follow-up
  bug prompts (autoarray Voronoi-vs-dual-area denominator; autolens magnification latent 0/0
  for pixelized sources — which also taints the vis_pix catalogue column Cortex phase 4
  witnesses). The autoarray fix shipped 2026-09-05 (PyAutoArray#524 closed, PR #525 merged,
  pending-release; record complete/2026/09/delaunay-dual-area-magnification.md); the autolens
  fix is next. Mind phase 9 remains, gated on Cortex phase 4.

## model-figures
- title: PyAutoFit model figures — structure-first model visualisation (caskade-style, scales to MGE/graphical/EP)
- ledger: draft/feature/autofit/model_figures_epic.md
- notes: phase 1 SHIPPED 2026-09-11 (complete/2026/09/model-figures-graph-spec.md, PyAutoFit#1606); phase 2 SHIPPED 2026-09-11 (complete/2026/09/model-figures-renderer.md — PyAutoFit#1614 + autofit_workspace#152 merged, pending-release PyAutoFit); phase 3 SHIPPED 2026-09-11 (complete/2026/09/model-figures-lens.md — PyAutoFit#1615 + PyAutoArray#550 + PyAutoGalaxy#616 + PyAutoLens#737 + autolens_workspace#541 + autogalaxy_workspace#240 merged, pending-release ×4; `__solved_parameters__` protocol); phase 4 SHIPPED 2026-09-12 (complete/2026/09/model-figures-graphical.md — PyAutoFit#1617 + autofit_workspace#153 + HowToFit#51 merged, pending-release PyAutoFit; plate notation, hoisted shared priors, hierarchical draws are not sharing); phase 5 SHIPPED 2026-09-13 (complete/2026/09/model-figures-ep-view.md — PyAutoFit#1619 merged, pending-release PyAutoFit; EP factor-graph view, af.EPPlotter, graph_model.png/graph_state.png); phase 6a SHIPPED 2026-09-13 (complete/2026/09/model-figures-rollout-autofit.md — PyAutoFit#1621 + autofit_workspace#154 + HowToFit#52 merged, pending-release PyAutoFit; figures beside every model.info in autofit_workspace + HowToFit, EP state figure); phase 6b SHIPPED 2026-09-14 in two waves (complete/2026/09/model-figures-rollout-lens.md — HowToLens#81 + autolens_workspace#543 wave 1, autolens_workspace#546 + HowToLens#83 wave 2; 102 scripts and 12 tutorials with their notebook twins). The per-figure reading commentary was RETIRED on the human's ruling the same day: every opener block is now two fixed paragraphs and the figure-rendering vocabulary is stripped from later-site notes, which supersedes 6b's "Pattern" section and retires its render-to-verify-vocabulary requirement. The same standard was swept across the six unclaimed repos as model-figure-prose-simplify (complete/2026/09/model-figure-prose-simplify.md — autofit_workspace#156, six PRs). Remaining cuts of phase 6: (b2) SLaM stages, (c) PyAutoGalaxy surfaces. 6 phased prompts; 1 → 2 → 3 in order, 4 after 2, 5 after 4, 6 (rollout across every workspace, HowTo chapter and sibling project) after 3 and 4; per-search figure output stays opt-in until phase-3 acceptance renders pass; sibling bug prompts under draft/bug/autofit/ are standalone.

## autolens-inference
- title: autolens_inference — inference benchmarking repo, birth to first base run
- ledger: autolens_inference/wiki/project/state.md
- notes: phase 1 SHIPPED 2026-09-10 (complete/2026/09/autolens-inference-birth.md); phase 2 SHIPPED 2026-09-11 (complete/2026/09/scrap-inference-programme.md — autolens_profiling#246 / PyAutoBrain#376 / PyAutoMind#401; archive ref `archive/condemned/autolens-profiling/inference-programme` @ `c8b60580`); 4 phases — 1 birth + registration (PyAutoMind#399), 2 Gut-archive and delete autolens_profiling's searches tier / baselines / inference notes (nothing inherited), 3 backend-parameterised SLaM driver + per-stage results + submit scripts (SHIPPED 2026-09-11, autolens_inference#3, complete/2026/09/slam-base-driver.md), 4 the first run on PyAutoCortex `projects/autolens_inference.md` (5-stage HST SLaM × {numba_cpu, jax_cpu, jax_gpu} × {dense, sparse}). Science half: that ledger. Ledger moved to autolens_inference/wiki/project/state.md when phase 3 landed 2026-09-11.

## fixed-lens-light-numba-cpu
- title: Fixed lens light on the numba CPU path — the whole programme again, off the GPU
- ledger: draft/research/autolens_profiling/fixed_light_numba_cpu_programme.md
- notes: successor to `fixed-lens-light-profiling` (COMPLETE 2026-09-14), filed the same day. Six phases mirroring that epic, worked strictly 1 → 2 → 3 → 4 → 5 → 6 — each phase's grid is chosen from the previous phase's answer; issue ONE at a time, never bulk-issued, and file each phase's own prompt when the campaign reaches it. The open question is real, not a port: phase 2 of the GPU epic found the numpy certified active set does NOT beat the library's own `fnnls`, and both run 1.9-3.6x slower at 8 BLAS threads than at 1 — and the numba production path was never measured at all. Every leg must record its thread settings (`NPROC`, BLAS, numba) and no comparison may cross them silently. Out of scope throughout, as in the GPU epic: JWST and the sparse operator (blocked on `draft/bug/autoarray/sparse_inversion_ignores_profile_subtracted_image.md`). A Fable / Astra campaign.
  Phase 1 COMPLETE 2026-09-14 (#263, PR #264 — harness shipped, timing legs carried by phase 2).
  Phase 2 COMPLETE 2026-09-16 (#265, PR #266): fixed lens light measures **2.03x** on the
  production numba CPU path (RAL job 343311, HST Delaunay N=1500, 1 thread, 932 -> 459 ms;
  405 ms with the memo on). The **NNLS speed-up round is CLOSED** — the library's memo (ON by
  default, 1.134x) already delivers what the factor-reuse kernel would (1.112x), so the
  conditional PyAutoArray `nnls_seed_factor_reuse` prompt is deliberately NOT filed. The
  residue is `regularization_matrix` 112 ms + log-det `F + lambda H` 40 ms + log-det `H`
  37.5 ms (47 % of the call).
  Phase 3 COMPLETE 2026-09-16 (#267; PyAutoArray #553/#554/#555 merged pending-release,
  autolens_profiling #272 merged carrying #269/#271; record
  complete/2026/09/fixed-light-numba-levers.md): three non-solver levers on numba CPU
  **413.3 → 230.0 ms = 1.80x** (1.38x split-reg numba kernels / 1.13x sparse log det H,
  CPU-only / 1.19x log det(F+λH) off the NNLS factor + cached curvature_reg_matrix), A100
  identity on every lever. Residue curvature_matrix 88 ms + fnnls 61 ms ≈ 65 %; lever 4
  candidates (A′ permute-active-last, edge-zeroed, covariance third factorisation) in the
  note's Next, not filed. Old phases 3-5 renumbered to 4-6 stand.

## hst-gpu-non-solver-residue
- title: The non-solver residue — optimise the HST GPU likelihood breakdown around the certified solve
- ledger: draft/research/autolens_profiling/hst_gpu_non_solver_residue_programme.md
- notes: successor to `fixed-lens-light-profiling` (COMPLETE 2026-09-14), filed the same day and named by its verdict. ~21 of the 25.4 ms certified Delaunay A100 call at HST N=1500 is NOT the solver (~13.9 ms mesh/mapper/weights, 4.92 ms the `F + lambda*H` build, 2.38 ms both log-dets); on DelaunayNN it is ~32 of 36 ms. PHASE 1 IS A MEASUREMENT, NOT AN OPTIMISATION: the 13.9 ms is attribution arithmetic across two cells, not a measured decomposition, and the campaign must first build a cell that times the real call's internals in one process and sums to the measured call within a few per cent. Levers ranked: mesh/mapper/weights, then the dense assembly (α≈1.69, overtakes the solve above N≈2500 and so sets the affordable-N ceiling), then the log-dets (re-read the matrix-free CG+SLQ verdict #247 before re-opening those). Inherits the GPU verdict's settled configuration — fp64, budget 7 on Delaunay, PDIP fallback, positivity never dropped — and may not change the answer: every optimisation carries an equivalence pin at ≤ 1e-9. A Fable / Astra campaign.
  Phase 1 MEASURED 2026-09-16 (#268, PR #270 MERGED 2026-09-16, record complete/2026/09/hst-gpu-residue-p1.md):
  trace-based one-process decomposition of the PRODUCTION jit (A100 array 343350 + RTX 2060), every kernel
  joined to source via the HLO stack-frame index, unjoined 0 ms, reconciliation ≤ 2.6 %. The "~13.9 ms
  mesh/mapper/weights" bucket is REFUTED (0.37 ms); the 25.39 ms headline was budget 2 — at production budget 7
  the Delaunay A100 call is 31.6 ms: solve 10.2, device idle 8.05 (5.44 = qhull pure_callback host round-trip),
  PSF convolution of the mapping cube 7.12, F GEMM 4.18, log-dets 2×0.89. F+λH is fused into the single GEMM
  (curvature draft: no JAX cost → #267 CPU-only); the doubled operated_mapping_matrix_list convolution is CSE'd.
  Border relocator ON is production (autogalaxy config default true), 0.10 ms. Levers ranked for phase 2:
  (1) qhull host round-trip 5.44 ms, (2) PSF convolution cube 7.12 ms (harness first), (3) second Cholesky
  for log det F+λH 0.89 ms. Note `results/notes/hst_gpu_residue_phase1_2026_09.md`.
  Phase 2 FILED 2026-09-16 as PLAN ONLY (no issue, no worktree, human said no dev yet):
  `draft/research/autolens_profiling/hst_gpu_residue_p2_vmap_vs_jit_and_batched_callback.md` — per the Codex
  review on #268: ONE matched A100 experiment (exact `Fitness._vmap` over 16 distinct draws vs 16 scalar-jitted
  evals; production is vmap, phase 1 traced single-call) decides the batching policy, then the batch-aware
  Delaunay `pure_callback` (`expand_dims`, one host call per batch) if the callback matters. Map revised with the
  phase-1 table and re-ranked levers (0 vmap/callback, 1 batch-size decoupling, 2 PSF cube, 3 log-det factor).
