# Redo the numba sparse SLaM base runs on RAL with the right thread setup

Issued: 2026-10-19

Issue: https://github.com/PyAutoLabs/autolens_inference/issues/38
@autolens_inference @PyAutoInsight

Consequence: judge

## Request (verbatim)

> ok, I think we therefore need to redo the numba sparse runs, but with the right set up to achieve
> these likelihood times. So take the _a100 out of their path name too, and lets split them into
> slam_base, slam_base_lightfixed (rename slam_based_light_fixed) but also do slam_delaunay and
> slam_delaunay_light_fixed noting that Delaunay SLaM pipelines also use AdaptSplit not Adapt
> regularization, and use the Hilbert (so therefroe you are using the standard SLaM delaunay)
>
> it should apply to old runs too, via folder renames (lightfixed)

## Why

The hst-imaging-mass-samplers numba_cpu sparse legs (RAL `ral` partition, 8 cores) ran ~35-40x
slower than profiling says they should: rectangular `source_pix[1]` 2.6 s wall/eval against an
expected ~0.06-0.08 s (8 Nautilus workers at ~0.5 s/call). September Delaunay-1250 rows were
6.6-9 s/eval against ~0.12 s expected (RAL single-thread 0.93 s/call, autolens_profiling
fixed-light numba Delaunay cells). Cause: the numba submits never set OPENBLAS/MKL/OMP/VECLIB/
NUMEXPR_NUM_THREADS=1, so each forked worker oversubscribes BLAS threads; PyAutoFit warned at every
stage. Profiling cells pin all five to 1.

## Scope

- Thread caps for the numba_cpu backend (runner env + submits).
- New config-name prefix `hpc_ral` for CPU legs; numba sparse reruns use `hpc_ral_numba_cpu_sparse_fp64`.
- Variant rename `_lightfixed` -> `_light_fixed`, applied to existing rows, run trees and prepared
  problems (laptop + RAL) via folder renames.
- Delaunay variant named `slam_delaunay` (standard SLaM Delaunay: Hilbert 1250, 30-pt edge ring, AdaptSplit).
- Four numba sparse legs: slam_base, slam_base_light_fixed, slam_delaunay, slam_delaunay_light_fixed.
