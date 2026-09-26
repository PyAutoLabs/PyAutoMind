# Interferometer likelihood campaign: scatter the real mapping matrix then cast in transform_mapping_matrix (GPU complex128 scatter floor)

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- interferometer
- mge
- jax-gpu
Difficulty: easy
Autonomy: supervised
Priority: high
Status: draft
Consequence: glance
Witness: on the RAL A100, step 3 ("Transformed mapping matrix (NUFFT)") of `results/breakdown/interferometer/sma/mge_hpc_a100_fp64.json` drops from 852.7 ms to under 50 ms, with the log_likelihood unchanged to 1e-9 nats.
Review-minutes: 5
Epic: interferometer-likelihood-campaign
Issued: 2026-09-26

Source: `autolens_profiling/results/notes/interferometer_mge_breakdown_2026_09.md`, lever 3
(autolens_profiling#308); probe numbers in
`results/breakdown/interferometer/mge_a100_diagnostics_probes_2026_09.json`.

## Why

`TransformerNUFFT.transform_mapping_matrix` casts the mapping matrix to complex128 and
scatters it slim->native into a `(n_src, N_y, N_x)` complex128 stack
(`autoarray/operators/transformer.py:525-527`) before the NUFFT. On the A100 a complex128
scatter of 20 columns takes 3422 ms (one column 224 ms), while scattering float64 and casting
takes 0.57 ms (~6000x); `unique_indices` / `indices_are_sorted` do not help. A bare
`nufft2d2` of 20 columns on 800x800 is 6.0 ms. The scatter is N_vis-independent: A100 sma
step 3 is 852.7 ms (vs 82.0 ms on the laptop CPU) and alma 915 ms. It is the whole reason
the A100 is ~10x slower than the CPU at sma.

## What

- In the JAX branch: scatter the real mapping matrix into a float64 native stack, then
  `.astype(complex128)` (or pass real input if nufftax accepts it).
- Audit the other slim->native complex scatters in `transformer.py` (e.g. `:417`) and the
  DFT transformer for the same pattern.
- Re-run the sma A100 breakdown leg and the imaging/interferometer pixelized dense cells
  that share the method.

## Watch

- CPU is unaffected (82 ms is NUFFT-bound); verify no CPU regression.

<!-- filed from autolens_profiling#308 phase C (PR #312), 2026-09-26 -->
