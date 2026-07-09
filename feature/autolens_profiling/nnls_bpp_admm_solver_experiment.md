# Prototype BPP and ADMM as alternatives to the PDIP positive-only solver

Type: feature
Target: autolens_profiling
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: captured

Follow-up to PyAutoArray#369 (NNLS solver controls). That task established the
interior-point ledger is complete: tolerance knob ships (~15-20% of solve),
warm starts hurt (un-center the start), fp32/iterative refinement diverges
(cond(Q)~1e10, eps32 x cond ~ 600), Gondzio multiple centrality corrections
cut iterations ~15% but wall-time is a wash (extra solves eat it; worse under
vmap). Every PDIP iteration is a fresh dense Cholesky of the (n, n) KKT
system and ~15-20 iterations is what Mehrotra costs here — further speedups
need a different algorithm, not a better-tuned PDIP.

Prototype the two candidates that fit JAX fixed-shape/vmap constraints,
against the REAL extracted production systems in
`autolens_profiling/scratch/nnls_speedup/system_{rectangular,delaunay}_hst.npz`
(pixelization + MGE-60, the production combo), using the probe harness
pattern already in that dir (`probe_pdip.py` / `probe_gondzio.py`):

1. **Block principal pivoting (BPP)** — guess the active set from the sign
   pattern of the unconstrained solve (the CPU fnnls path's `P_initial`
   trick already proves prediction quality on these systems), solve the
   reduced system via a masked full-size Cholesky (active rows/cols set to
   identity — fixed shapes, vmappable), swap misclassified blocks, repeat.
   Expected ~3-5 factorizations vs PDIP's ~20 (ceiling ~4x). Known risk:
   cycling on degenerate active sets — the rect outskirts ARE degenerate
   (0.27 fnnls-vs-PDIP solution drift at equal objective on the rect
   system), so implement the Kim-Park backup exchange rule and a PDIP
   fallback on non-convergence.
2. **ADMM** — factorize (Q + rho*I) ONCE, then iterations are triangular
   solves + non-negativity clip (~2ms vs ~14ms per PDIP iteration on the
   RTX 2060). Needs more iterations but only ~1e-6 objective accuracy is
   required (log-evidence tolerance measured in #369). Perfectly
   vmap-uniform. Tune rho on the real systems; check iteration count
   scaling with the Jacobi-preconditioned conditioning.

Benchmark on the laptop GPU (PyAutoGPU venv; set BOTH JAX_PLATFORM_NAME and
JAX_PLATFORMS) and, when available, the A100 (hpc/batch_gpu pattern from
#369). Gates for promoting either into PyAutoArray:

- >= 2x solve speedup over the shipped PDIP-with-knobs baseline, single-JIT
  AND vmap-batched, on both rect and Delaunay real systems;
- objective/evidence parity: |delta objective| within the tol-1e-6 envelope
  measured in #369; gradient path preserved or wrapped (the relaxed-KKT
  custom-vjp backward can wrap any primal solver — the backward pass only
  needs the primal solution);
- PDIP fallback wired for non-convergence; no vmap lane divergence traps.

If neither clears the gates, write the negative result into the #369 dead-end
ledger and close. Original request (2026-07-09): "ok, so theres no way to
speed up the positive only solve? or would we need to research other linear
algebra techniques altogether" -> assessment identified BPP + ADMM as the
two candidates worth prototyping; user asked to file this follow-up.
