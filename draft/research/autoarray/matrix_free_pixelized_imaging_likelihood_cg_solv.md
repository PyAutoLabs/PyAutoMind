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
Witness: a results note under `autolens_profiling/results/notes/` with the prototype's per-call / VRAM / log-evidence-error table per mesh against the baseline rows, a stated go/no-go, and (on go) a PyAutoArray PR behind the same pins.
Review-minutes: 25
Unattended: ready
Parent: complete/2026/09/a100-pixelized-baseline.md
Blocked-by: draft/research/autolens_profiling/instrument_pixelized_reconstruction_row_nnls_cholesky_logdet.md   # shipped at autolens_profiling PR #244 (issue #243); the split numbers below come from it — the gate clears when #244 merges
Filed: 2026-09-10

## Why

The matrix-free line (CG for the reduced solve, never forming F + λH; log det via stochastic Lanczos quadrature / Hutchinson) was deferred on 2026-06-07 as plan-B (`autolens_profiling/results/notes/sparse_vs_dense_inversion_path.md`, recommendation #4, now superseded) because the sparse w-tilde path kept an exact Cholesky log-det and won on memory. The 2026-09-10 A100 fp64 baseline (`results/notes/a100_pixelized_baseline_2026_09.md`) re-opened it with hard numbers: dense F is 4.83 ms flat (no longer the villain), the w-tilde F is 18–20 ms, and the solve (NNLS + Cholesky) is ~37 ms = 61–71 % of every row.

The 2026-09-11 reconstruction split (same note, "Reconstruction split" section; autolens_profiling #243 / PR #244) then took that ~37 ms apart, and it changes what this prototype has to beat. **The 37 ms is not a linear solve.** It is 21–22 PDIP iterations of NNLS at ~1.7 ms each, every iteration a fresh dense KKT Cholesky inside `jaxnnls`. On the same F + λH: one Cholesky is 1.19–1.26 ms, a full *exact* unconstrained solve (that factorisation plus two triangular solves) is **1.52–1.58 ms**, and the two exact log-det Choleskys are **1.15–1.27 ms each** (~2.4 ms together). So positivity costs ~24× the exact solve it replaces, and **a CG line that only replaces the linear solve has ~1.6 ms per call to beat, not 37** — plus the ~2.4 ms SLQ actually targets. Even a free CG solve takes ~4 ms off a ~50–65 ms call and leaves the 37 ms untouched. Batching does not rescue the NNLS either: under `vmap` 16 with *identical* lanes it amortises only 1.7× (21.9 ms per call). Any matrix-free scheme must therefore win on the NNLS iteration count or on positivity itself, and it must still pay for log-det estimation noise the exact path does not have.

## What to decide, then build

1. Prototype (autolens_profiling `scripts/misc/`, JAX, A100 fp64) a matrix-free evaluation of the pixelized likelihood on the fiducial HST tier: CG on (F + λH) x = D using operator products only (w-tilde blocks for F, sparse H), preconditioned; log det(F + λH) and log det(reduced H) by SLQ with a fixed probe count. **Positivity is the decision, not a detail.** Because CG replacing the linear solve alone cannot win more than ~1.6 ms/call, the prototype must do one of two things and say which up front: (a) target the NNLS iteration count — warm starts across likelihood evaluations, a looser `solver_tol`, a lower `max_iter`, a matrix-free / preconditioned interior-point step, or a cheaper positivity treatment (projection, penalty) — and measure iterations, not only milliseconds; or (b) drop positivity and justify the drop with the reconstruction and log-evidence differences it causes on all three meshes. A prototype that keeps the shipped NNLS unchanged and swaps only the solve is not worth building.
2. Measure against the baseline's "must beat" columns per mesh (rect / Delaunay / DelaunayNN, dense 51.8 / 53.2 / 48.7 ms; sparse 64.9 / 63.3 / 65.3 ms unbatched; per-call at vmap 16 from the runtime table) **and against the reconstruction split rows**: exact unconstrained solve 1.52–1.58 ms, single Cholesky 1.19–1.26 ms, log-det Choleskys 1.15–1.27 ms each, NNLS 37.1–37.3 ms = 21–22 × ~1.7 ms. Report per-call time, PDIP/CG iteration counts, VRAM, and the log-evidence error against the exact `log_evidence_terms` values recorded on 2026-09-11 (log det F+λH 3888.258090 / 8360.401763 / 7224.568778; log det H 1692.786817 / 7756.614959 / 6690.183752), as a function of CG tolerance and SLQ probe count. DelaunayNN's 491k sparse non-zeros (8–11x the other meshes) must be measured, not extrapolated.
3. Decision gate, made explicit by the split: the ceiling on "CG instead of the direct solve" is ~1.6 ms/call (plus ~2.4 ms of log-dets for SLQ) — about 3–8 % of a call — so **beating the linear solve is not a pass**. The prototype proceeds to a PyAutoArray implementation (`InversionImagingSparse`-adjacent, opt-in, no change to the default path) only if it beats the sparse per-call cost by taking time out of the NNLS row (fewer PDIP iterations, or positivity dropped with the error budget stated and accepted), with log-evidence noise below the sampler's tolerance (state it). Otherwise close with the note recording why not — and if the measured win is confined to the ~1.6 ms solve, close it as no-go on this evidence rather than iterating on the CG.

Start from the plan-B memory and the baseline note, not from scratch; the log-det obstacle is the open question, not memory.

Witness: a results note under `autolens_profiling/results/notes/` with the prototype's per-call / VRAM / log-evidence-error table per mesh against the baseline rows, a stated go/no-go, and (on go) a PyAutoArray PR behind the same pins.

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5d8bb12c-d0c2-46fc-b5a1-544c43387c68/scratchpad/intake_b.md -->
