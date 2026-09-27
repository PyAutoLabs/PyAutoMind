# Load-balance the `prange` direct_conv interferometer kernel (Delaunay stalls at 2 threads, autolens_profiling#332)

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- interferometer
- numba-cpu
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: glance
Witness: on an idle RAL CPU node, the parallel kernel's F-alone speed-up at 2 / 4 threads on alma Delaunay-1500 (AdaptSplit Hilbert) is within 15 % of the rectangular mesh's (1.96× / 2.53× in #332), bit-identical F (max |Δ| = 0) and unchanged serial path.
Review-minutes: 6
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-27

## Context

`direct_conv_parallel_kernel` (PyAutoArray
`autoarray/inversion/inversion/interferometer_numba/inversion_interferometer_numba_util.py:109-160`)
runs `prange(pix_pixels)` over source columns (`:157`). It is selected when `general.yaml`
`numba.parallel` is true (`autoarray/config/general.yaml:26`, default false) via
`autoarray/inversion/inversion/interferometer_numba/sparse.py:202-203`.

autolens_profiling#332 `levers.threads`
(`results/breakdown/interferometer/{delaunay,pixelization}_numba_hpc_ral_cpu_fp64_levers.json`,
RAL gpu-2 idle, BLAS 1, pool 4):

| Mesh | serial | 1 thread | 2 threads | 4 threads |
|---|---|---|---|---|
| Delaunay-1500 | 895 ms | 914 ms | 874 ms (**1.02×**) | 466 ms (1.92×) |
| rect 39² | 1248 ms | 1182 ms | 637 ms (1.96×) | 493 ms (2.53×) |

The Hilbert Delaunay mesh orders columns along the adapt image, and column cost is its nnz. A static
split hands one thread the dense half; rect columns are near-uniform. #226's synthetic bake-off got
4.63× at 8 threads on uniform columns.

## What

1. In `direct_conv_parallel_kernel`, permute (or chunk) the column loop by nnz from `cscptr` so each
   thread gets equal work, e.g. round-robin over nnz-sorted columns. Each column still writes only
   its own row of F, so no reduction is needed.
2. Re-run the #332 lever job (`hpc/batch_cpu/submit_breakdown_interferometer_numba_levers_ral_alma_fp64`,
   `--nodelist` an idle node).

## Scope caveat

Production fits run one single-threaded likelihood per Nautilus pool worker. This lever is for
interactive / single-process runs; `numba.parallel` stays default false.
