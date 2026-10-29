# Rectangular 28² profiling rows: size-variant rows so rectangular inference runs pair like-for-like

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/468 (closed 2026-10-29)
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/80 MERGED 2026-10-26 5474e3cb (human /prm)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/470 MERGED 2026-10-27 a1a4ccf1 (human /prm)
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/49 MERGED 2026-10-29 (head 4de9065f, merge e9962008; human "prm 49")
- epic: likelihood-lifecycle
- heart-red-override: authorized by live human 2026-10-26 "I approve of the override" (this task, including its RAL jobs); extended to the PyAutoPulse scope-add
- scope-add: HUMAN 2026-10-26 chose "Yes, small Pulse PR first". PyAutoPulse's one-current-per-key rule now includes regime (PyAutoPulse#80). Order: Pulse PR, then the profiling rows, then the inference join refresh.
- merged: 2026-10-29

## Shipped (scope: the approved plan, in full)

- **PyAutoPulse#80**: regime is now part of the `profiling-summary@3` one-current key, with a validator test and a REFERENCE update. A size-variant row can be current beside the standard row.
- **autolens_profiling#470**: adds a declared size variant (`catalogue/size_variants.json`, rectangular 784) and `--standard-size --source-pixels 784`. A `rect28_tasks()` generator writes the RAL CPU array and one A100 `--gres` job. RAL jobs 413044 and 413046 ran 8/8 legs on pin 2026.10.25.1. That produced hst rectangular runtime and breakdown rows in regime `source_pixels_784` for numba_cpu_sparse@hpc_ral_cpu (0.567 s), jax_cpu_sparse@hpc_a100 (1.279 s), jax_gpu_dense@hpc_a100 (28.1 ms) and jax_gpu_sparse@hpc_a100 (47.1 ms). All parity checks match. Coverage stays standard-only (35² cells).
- **autolens_inference#49**: refreshes `catalogue/pulse_lens_runtime_reference.json` from the Pulse lens snapshot at a1a4ccf1. `size_match` went from 4 match / 28 differ to **32 match / 0 differ**.

## Declared limitation (shipped scope, not open work)

24 inference records stay unpaired by design (`size_match` is absent for them, not false). The approved plan put these out of scope, and the gap is accepted:
- jax_cpu_dense (12): autolens_profiling has no jax_cpu_dense rectangular setup at any size.
- light_fixed (7): there are no light_fixed runtime cells at any size.
- source_lp[1] (5): this stage is parametric, with no inversion, so there is no source-pixel size to pair.

The prompt's witness listed jax_cpu_dense and light_fixed, so it is met only within the approved plan's scope. Neither the prompt nor the plan asks for a follow-up, so no remainder draft was filed. Pairing these records would need new profiling setups and cells, not an exporter change.

## Follow-ups

- Cosmetic: the autolens_profiling README version column shows v2026.8.17.1 on the `source_pixels_784` rows, but they were measured on pin 2026.10.25.1. The rows stamp the source checkout's stale `autolens_version`; the revision SHAs are the real provenance. Not fixed here.

## Original prompt

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
