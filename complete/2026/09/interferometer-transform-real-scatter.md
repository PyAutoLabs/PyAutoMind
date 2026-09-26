## interferometer-transform-real-scatter
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/577 (closed 2026-09-26)
- completed: 2026-09-26
- library-pr: PyAutoArray https://github.com/PyAutoLabs/PyAutoArray/pull/578 (head `f9d3bc67`, merged 2026-09-26T18:26:18Z)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/319 (head `c11c8f81`, merged 2026-09-26T18:26:21Z)
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/578
- pending-release: autolens_profiling@https://github.com/PyAutoLabs/autolens_profiling/pull/319
- merge-order: library-first — PyAutoArray#578 → autolens_profiling#319, both by the human's /prm on 2026-09-26.
- heart-ack: "2026-09-26 YELLOW acknowledged by human: manifest drift hub blurb 7; organism-map blocks 1; workspace checkouts 1; release validation stale (source moved since rehearsal)"

- summary: `TransformerNUFFT.transform_mapping_matrix` now scatters the real mapping matrix, flips, then casts to complex128 (the complex128 scatter was the bottleneck). Output is bit-identical; an exact-equality test covers NumPy and `jax.jit`.
- results: RAL job 356364, same node, main control vs branch, sma MGE dense path: step 3 851.5 → 0.51 ms; full pipeline 868.5 → 3.39 ms; vmap4 225 → 1.34 ms/call; log L identical.
- validation: no CPU regression (ABBA); unit suite 1707 passed; smoke 21/21; Heart YELLOW acknowledged.
- gotcha: the shared RAL mirror is stale (pre-#575) — `HPCPullPyAuto` is due.
- limit: the alma chunked arm uses the cell's own transform, so it was not re-run.
- follow-ups (still-open epic drafts): `interferometer_chunked_transform_mapping_matrix`, `ral_venv_dependency_floor_drift`.
- ral-leftovers (not touched at close-out): `/mnt/ral/jnightin/PyAuto_branch/interferometer-transform-real-scatter/`; `/mnt/ral/jnightin/autolens_profiling_wt/interferometer-transform-real-scatter` (+ the `feature/interferometer-transform-real-scatter` branch in the RAL autolens_profiling checkout); still from the earlier task: `/mnt/ral/jnightin/PyAuto_branch/interferometer-mge-w-tilde-route/`, `/mnt/ral/jnightin/autolens_profiling_wt/interferometer-mge-w-tilde-route`.
- worktree: `~/Code/PyAutoLabs-wt/interferometer-transform-real-scatter` removed at close-out.

## Original prompt

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
