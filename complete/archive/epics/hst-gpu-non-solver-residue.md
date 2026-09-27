# The non-solver residue — optimise the HST GPU likelihood breakdown around the certified solve

## Retired from epics.md (2026-09-27)

## hst-gpu-non-solver-residue
- title: The non-solver residue — optimise the HST GPU likelihood breakdown around the certified solve
- ledger: complete/2026/09/hst-gpu-non-solver-residue.md
- status: COMPLETE 2026-09-27 — phases 1-4 shipped (records complete/2026/09/hst-gpu-residue-p{1,2,3,4}.md); fp64 levers exhausted; map retired to complete/2026/09/hst-gpu-non-solver-residue.md
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
  Phase 2 STEP 1 COMPLETED 2026-09-20 (#273, PR #294): current production
  `jax.jit(jax.vmap(call))` was measured against matched scalar jit. Fallback-on
  batching was slower per lane at B=4/8/16, but the required three-way `1e-9`
  numerical pin failed on distinct lanes at B=8/B=16, so the policy verdict is
  explicitly inconclusive. No batching change or batch-aware callback was authorised.
  Array 343376 remains historical evidence for retired `vmap(jit)`; array 344635 and
  provenance are in the merged profiling results. Record:
  `complete/2026/09/hst-gpu-residue-p2.md`.
