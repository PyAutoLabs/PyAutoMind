# Profile rectangular imaging at 28² (the production preset) so inference rows link like-for-like

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Epic: likelihood-lifecycle
Status: formalised
Consequence: judge
Witness: every rectangular imaging setup that has an inference wall-time record (hst; numba_cpu_sparse, jax_cpu_sparse, jax_cpu_dense, jax_gpu_sparse, jax_gpu_dense on their host classes; default + light_fixed variants where inference ran) has a current 28x28 runtime row on pin 2026.10.25.1, and the autolens_inference exporter's size_match is true for those rows
Filed: 2026-10-26
Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/468

## Request
HUMAN 2026-10-26, choosing "Profile 28² too": the SLaM inference runs use the rectangular production preset 28x28
(784 px, `mesh_shape`) while the profiling standard size is 35x35 (1225 px, human size rule 2026-10-23), so the
inference table's "Profiling runtime" link compares different likelihood sizes (autolens_inference#47:
size_match false on every rectangular match). Add 28² rectangular runtime rows (a size variant beside the
standard, not replacing it — the 35² standard stays the coverage cell) for the setups/instruments that have
inference records, measured on RAL at pin 2026.10.25.1 (private checkout /mnt/ral/jnightin/profiling/PyAuto_2026.10.25.1),
and make the exporter prefer the exact-size current record (#47 already tie-breaks on size_match).
Delaunay needs nothing: runs use 1250 = profiling standard.

## Plan (approved in chat "go", 2026-10-26)
1. RAL: verify /mnt/ral/jnightin/profiling/PyAuto_2026.10.25.1 has all 5 libs at tag 2026.10.25.1 (fill Lens from the shared mirror if its GitHub clone failed); 28² submits point at it — first rows measured ON 2026.10.25.1.
2. Generator: declared 28² size-variant batch in scripts/misc/campaigns (imaging_p2a.py or a sibling): hst rectangular runtime + breakdown legs for numba_cpu_sparse@hpc_ral_cpu, jax_cpu_sparse@hpc_a100, jax_gpu_sparse@hpc_a100, jax_gpu_dense@hpc_a100 with --source-pixels 784; numba + jax_cpu_sparse legs → RAL CPU array (--partition=ral only), GPU legs → one A100 --gres job (8 legs, ~20 min on 2a walls).
3. Submit (human go given with this approval), pull, commit as current rows in regime source_pixels_784 beside the 35² standard; regenerate catalogue → dashboard → coverage (coverage stays standard-only).
4. autolens_inference: refresh catalogue/pulse_lens_runtime_reference.json so the exact-size tie-break picks the 784 rows (size_match true for default rectangular runs).
Out of scope: jax_cpu_dense (no profiling setup), light_fixed (no profiling cells at any size).
Heart RED override: live human 2026-10-26 "I approve of the override" for this task (incl. its RAL jobs).

## Scope addition (2026-10-26)
PyAutoPulse rejects a second current record differing only by regime (key = likelihood, instrument, setup_id, host_class, model_variant, measurement). HUMAN chose "Yes, small Pulse PR first": PyAutoPulse key adds regime; validator test + REFERENCE; RED override extended to it; order Pulse PR → profiling rows → inference join refresh.
