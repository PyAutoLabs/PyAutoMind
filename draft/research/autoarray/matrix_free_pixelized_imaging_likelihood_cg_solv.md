# Matrix-free pixelized imaging likelihood: CG solve + stochastic Lanczos quadrature log-det, sized against the 2026-09 A100 baseline

Type: research
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- jax-gpu
- performance
- pixelization
- inversion
Difficulty: large
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: a results note under `autolens_profiling/results/notes/` with (i) the fiducial-tier table per mesh against the reconstruction split rows, (ii) the N_src sweep table (dense / sparse / matrix-free × time / VRAM / fits) with the crossover stated, (iii) the SLQ-noise-vs-probe-count curve against the exact log-dets, a stated go/no-go, and (on go) a PyAutoArray PR behind the same pins; the reference implementation committed under `scripts/misc/` with its own README row.
Review-minutes: 25
Unattended: ready
Parent: complete/2026/09/a100-pixelized-baseline.md
Blocked-by: draft/research/autolens_profiling/instrument_pixelized_reconstruction_row_nnls_cholesky_logdet.md   # shipped at autolens_profiling PR #244 (issue #243); the split numbers below come from it — the gate clears when #244 merges
Filed: 2026-09-10

## Why

The matrix-free line (CG for the reduced solve, never forming F + λH; log det via stochastic Lanczos quadrature / Hutchinson) was deferred on 2026-06-07 as plan-B (`autolens_profiling/results/notes/sparse_vs_dense_inversion_path.md`, recommendation #4, now superseded) because the sparse w-tilde path kept an exact Cholesky log-det and won on memory. The 2026-09-10 A100 fp64 baseline (`results/notes/a100_pixelized_baseline_2026_09.md`) re-opened it with hard numbers: dense F is 4.83 ms flat (no longer the villain), the w-tilde F is 18–20 ms, and the solve (NNLS + Cholesky) is ~37 ms = 61–71 % of every row.

The 2026-09-11 reconstruction split (same note, "Reconstruction split" section; autolens_profiling #243 / PR #244) then took that ~37 ms apart, and it changes what this prototype has to beat. **The 37 ms is not a linear solve.** It is 21–22 PDIP iterations of NNLS at ~1.7 ms each, every iteration a fresh dense KKT Cholesky inside `jaxnnls`. On the same F + λH: one Cholesky is 1.19–1.26 ms, a full *exact* unconstrained solve (that factorisation plus two triangular solves) is **1.52–1.58 ms**, and the two exact log-det Choleskys are **1.15–1.27 ms each** (~2.4 ms together). So positivity costs ~24× the exact solve it replaces, and **a CG line that only replaces the linear solve has ~1.6 ms per call to beat, not 37** — plus the ~2.4 ms SLQ actually targets. Even a free CG solve takes ~4 ms off a ~50–65 ms call and leaves the 37 ms untouched. Batching does not rescue the NNLS either: under `vmap` 16 with *identical* lanes it amortises only 1.7× (21.9 ms per call). Any matrix-free scheme must therefore win on the NNLS iteration count or on positivity itself, and it must still pay for log-det estimation noise the exact path does not have.

## What to decide, then build

**Framing (2026-09-11, after the reconstruction split):** at the fiducial tier (1500 / 1521 source pixels) the exact unconstrained solve is 1.5–1.6 ms and the whole 37 ms reconstruction row is positivity (21–22 PDIP iterations × 1.7 ms, each a fresh dense KKT Cholesky). A matrix-free CG line therefore cannot be a speed play at n ≈ 1500 — say so up front and do not spend the task trying to beat 1.6 ms. Its value is elsewhere: dense factorisation grows as n³ and the dense F assembly as N_pix × N_src (35 GB at 1521 pixels → >100 GB at 5000, which no longer fits an A100), while a matrix-free matvec costs the sparse non-zero count plus an FFT and is nearly independent of N_src for bilinear / Delaunay. So the deliverable is the **reference implementation plus the source-pixel sweep that finds the crossover** — the artefact the profiling repo does not have and the thing that decides whether 5000+ source-pixel modelling is feasible on a GPU at all.

1. **Reference implementation** (autolens_profiling `scripts/misc/`, JAX, A100 fp64; the fiducial HST tier first): a matrix-free evaluation of the pixelized likelihood — CG on (F + λH) x = D using operator products only (w-tilde blocks for F, sparse H), preconditioned (Jacobi at least); log det(F + λH) and log det(reduced H) by SLQ with a configurable probe count; positivity treated explicitly and stated: (a) matrix-free / preconditioned interior-point (inner CG per PDIP step), (b) a projection or penalty scheme using only matvecs, or (c) unconstrained with the reconstruction and log-evidence differences measured on all three meshes. Bit-for-bit provenance like the baseline cells (fresh cache, same node, pins) and the same JSON conventions, so it is a row the notes can quote.
2. **Fiducial-tier measurement** against the reconstruction split rows (exact unconstrained solve 1.52–1.58 ms, single Cholesky 1.19–1.26 ms, log-det Choleskys 1.15–1.27 ms each, NNLS 37.1–37.3 ms = 21–22 × ~1.7 ms; NNLS @vmap16 identical lanes 21.9 ms) and the baseline "must beat" columns (dense 51.8 / 53.2 / 48.7 ms; sparse 64.9 / 63.3 / 65.3 ms unbatched). Report per-call time, CG iterations, PDIP iterations where applicable, VRAM, and the log-evidence error against the exact `log_evidence_terms` recorded 2026-09-11 (log det F+λH 3888.258090 / 8360.401763 / 7224.568778; log det H 1692.786817 / 7756.614959 / 6690.183752) as a function of CG tolerance and SLQ probe count. The expected result is a no-go on speed here; the table is the reference, not the verdict.
3. **Source-pixel sweep — the headline.** Sweep N_src over ~1500, 3000, 5000, 8000, 12000 (rectangular and Delaunay; DelaunayNN where its 491k-and-growing non-zeros allow — measured, never extrapolated) for dense, sparse (w-tilde) and matrix-free: per-call time (unbatched and vmap 16), device memory, and whether the leg fits at all. Report the crossover mesh size where matrix-free overtakes the exact Cholesky solve and where dense stops fitting, and the SLQ probe count needed to hold log-evidence noise below a stated sampler tolerance at each size.
4. **Decision gate.** A PyAutoArray implementation (`InversionImagingSparse`-adjacent, opt-in, no change to the default path) proceeds only if the sweep shows a size at which matrix-free is the only path that fits or is faster than sparse, with log-evidence noise below the stated tolerance and positivity handled per (1). If the crossover sits above any mesh size the science needs, close with the note recording the crossover and why — that is still the deliverable.

Start from the plan-B memory and the baseline note (both "Reconstruction split" and "What this baseline says to the matrix-free work"), not from scratch; the log-det obstacle and the positivity treatment are the open questions, not memory.


<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5d8bb12c-d0c2-46fc-b5a1-544c43387c68/scratchpad/intake_b.md -->
