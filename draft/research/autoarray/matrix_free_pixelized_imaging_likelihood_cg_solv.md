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
Blocked-by: draft/research/autolens_profiling/instrument_pixelized_reconstruction_row_nnls_cholesky_logdet.md   # the reconstruction-row split + log-det emission this prototype is sized against
Filed: 2026-09-10

## Why

The matrix-free line (CG for the reduced solve, never forming F + λH; log det via stochastic Lanczos quadrature / Hutchinson) was deferred on 2026-06-07 as plan-B (`autolens_profiling/results/notes/sparse_vs_dense_inversion_path.md`, recommendation #4, now superseded) because the sparse w-tilde path kept an exact Cholesky log-det and won on memory. The 2026-09-10 A100 fp64 baseline (`results/notes/a100_pixelized_baseline_2026_09.md`) re-opens it with hard numbers: dense F is 4.83 ms flat (no longer the villain), the w-tilde F is 18–20 ms, and the solve (NNLS + Cholesky) is ~37 ms = 61–71 % of every row. Any matrix-free scheme wins only what it takes out of that solve, and it must pay for log-det estimation noise the exact path does not have.

## What to decide, then build

1. Prototype (autolens_profiling `scripts/misc/`, JAX, A100 fp64) a matrix-free evaluation of the pixelized likelihood on the fiducial HST tier: CG on (F + λH) x = D using operator products only (w-tilde blocks for F, sparse H), preconditioned; log det(F + λH) and log det(reduced H) by SLQ with a fixed probe count; NNLS positivity handled the same way as the shipped path or explicitly dropped with the consequence stated.
2. Measure against the baseline's "must beat" columns per mesh (rect / Delaunay / DelaunayNN, dense 51.8 / 53.2 / 48.7 ms; sparse 64.9 / 63.3 / 65.3 ms unbatched; per-call at vmap 16 from the runtime table) and against the reconstruction sub-row split from the blocking task; report per-call time, VRAM, and the log-evidence error vs the exact Cholesky values as a function of CG tolerance and SLQ probe count. DelaunayNN's 491k sparse non-zeros (8–11x the other meshes) must be measured, not extrapolated.
3. Decision gate: only if the prototype beats the sparse per-call cost with log-evidence noise below the sampler's tolerance (state it) does the task proceed to a PyAutoArray implementation (`InversionImagingSparse`-adjacent, opt-in, no change to the default path); otherwise close with the note recording why not.

Start from the plan-B memory and the baseline note, not from scratch; the log-det obstacle is the open question, not memory.

Witness: a results note under `autolens_profiling/results/notes/` with the prototype's per-call / VRAM / log-evidence-error table per mesh against the baseline rows, a stated go/no-go, and (on go) a PyAutoArray PR behind the same pins.

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5d8bb12c-d0c2-46fc-b5a1-544c43387c68/scratchpad/intake_b.md -->
