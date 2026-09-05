# `--xla_gpu_autotune_level=0` default makes the fp64 curvature-matrix GEMM 5x slower on the A100

Type: bug
Target: autonerves
Repos:
- PyAutoNerves
- autolens_profiling
Themes:
- jax-gpu
- performance
- hpc
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: an A100 Delaunay breakdown run with the library defaults (no explicit autotune flag) reports "Curvature matrix (F)" under 6 ms and the JSON's device.xla_flags carries no `--xla_gpu_autotune_level=0`; the jax_wrapper log message about autotuning is gone or corrected
Review-minutes: 10
Unattended: ready
Filed: 2026-09-05

`PyAutoNerves/autonerves/jax_wrapper.py` (lines 58-73, introduced in e8d5842 on
2026-07-17, "enable JAX persistent compilation cache by default + fix XLA_FLAGS clobber")
appends `--xla_gpu_autotune_level=0` to `XLA_FLAGS` whenever no explicit level is set,
with the rationale that autotuning "dominates cold JAX compile times on GPU (measured up
to ~7 minutes for a single fusion) while giving no measurable evaluation speed-up on
PyAuto likelihoods".

The second half of that rationale is false for the dense fp64 GEMM at the heart of every
pixelized inversion. Controlled A/B on the RAL A100, same commit, same script, same data
(autolens_profiling PR #221, `results/notes/delaunay_nn_breakdown.md`, section "XLA GPU
autotuning A/B (2026-09-05)", jobs 342277/342282 and 342281/342283):

| quantity | autotune 0 (default) | autotune 4 (XLA default) |
|---|---:|---:|
| Curvature matrix F, 15361x1560 fp64 GEMM | 25.63 ms | 4.90 ms |
| Delaunay breakdown total, unbatched | 117.4 ms | 101.1 ms |
| DelaunayNN runtime, single JIT | 250.3 ms | 229.2 ms |
| DelaunayNN runtime, vmap/16 per call | 82.2 ms | 62.9 ms |
| `curvature_matrix_jit_compile` | 0.38 s | 1.79 s |
| runtime cell one-off compile total | 48.9 s | 57.6 s |

Every Cholesky-bound row (NNLS reconstruction, log-determinants) is flat; the whole
difference is the GEMM algorithm choice. The 2026-07-10 A100 tier (before e8d5842)
already showed F at 4.82 ms, so every A100 number produced since 2026-07-17, including
the Nautilus and NSS production searches, carries roughly 20 ms per evaluation of
avoidable cost. Break-even against the extra compile is under 500 evaluations.

## Fix

1. Stop injecting `--xla_gpu_autotune_level=0` by default. Either remove the block, or
   invert it into an opt-in (`PYAUTO_XLA_AUTOTUNE_OFF=1`, or respect an explicit level
   only) for the interactive, compile-bound use case the original commit was protecting.
2. Re-measure the "7 minutes for a single fusion" claim on the current jax (0.10.2 on
   RAL) with the persistent compilation cache that the same commit enabled; if it still
   reproduces for some cell, document which cell and keep the opt-out for it, never as
   the default.
3. Update the log message and the PyAutoNerves docs that describe the default.
4. Verification: rerun `autolens_profiling/hpc/batch_gpu/submit_breakdown_imaging_delaunay_a100_hst_fp64`
   with the library defaults and confirm F under 6 ms and no autotune flag in the
   recorded `xla_flags`; a laptop-GPU spot check of compile time on one runtime cell.

## Downstream

The `hpc_a100_fp64` dashboard rows in autolens_profiling recorded between 2026-07-17 and
this fix are systematically slow on every GEMM-bound step. After the fix lands, the
Delaunay/DelaunayNN breakdown and runtime cells should be re-run so the dashboard is not
comparing across the flag change; the `_autotune4` rows from PR #221 are the reference.
