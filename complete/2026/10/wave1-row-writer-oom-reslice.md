## wave1-row-writer-oom-reslice
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/33
- completed: 2026-10-17
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/34
- summary: Wave 1 attempt 1 (RAL 412543) lost every Nautilus/Emcee row because run.py keyed max_likelihood_parameters by `dict(zip(result.samples.names, ...))` and PyAutoFit's samples.names is model.all_names (tuples of dotted aliases); keys now go through slam._runner.posterior_path and post-fit diagnostics/serialisation failures are recorded in the row, never lose it. wave.py gained --attempt (_a<N>), --sampler-filter and multi-attempt accounting; NUTS (385 GiB) and SMC (48 GiB) A100 OOM -> deferred in wave 1. GPU submit runs attempt 2 over the 12 Nautilus+Emcee arms (brief said 16; table has 12). Witnessed on the euclid test-mode problem (repro + fixed rows). Follow-ups: memory-feasible NUTS/SMC formulation; prepared.complete_baseline str(tuple) keys.

## Original prompt

# `@autolens_inference` wave 1: experiment row writer crashes on tuple keys after a completed fit; re-slice NUTS/SMC after A100 OOM

Type: bug
Target: autolens_inference
Repos:
- autolens_inference
- PyAutoInsight
- PyAutoCortex
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-10-17
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/33
Consequence: judge
Witness: `experiments/run.py` writes a complete JSON row for a nautilus and an emcee cold fit on a euclid test-mode prepared problem under the installed PyAutoFit (keys all strings, `posterior` and `max_likelihood_parameters` keyed by dotted parameter paths), a unit test feeds a samples object whose `names` are tuples and asserts the row serialises; `wave.py` gains an attempt suffix so re-runs of the same arm get a new run id while the wave accounting shows attempt 1 as `failed` with its reason and attempt 2 as the live row; the GPU wave submit for attempt 2 runs only the 16 nautilus+emcee arms; NUTS/SMC arms are `deferred` in the wave table with the OOM evidence; CI green.
Review-minutes: 20
Unattended: needs-slicing

Why: RAL array 412543 (GPU sampler wave 1, 2026-10-17) failed on every arm. (1) nautilus and emcee arms (0, 1, 4, 5, 8, 12, and the rest) completed their `mass_total[1]` fits ("Search complete, returning result"), then died in the `finally` row write at `scripts/misc/experiments/run.py` line 350 with `TypeError: keys must be str, int, float, bool or None, not tuple` from `json_bytes(row)`: under the pinned PyAutoFit 2026.10.17.1, `result.samples.names` (used for `max_likelihood_parameters`) and/or `posterior_from_result` produce tuple keys. The row is lost although the PyAutoFit output tree is complete; `run.py` refuses to reuse a run id. The failed-status rows for NUTS/SMC were written fine because they never reached the posterior section. (2) NUTS arms (2, 6, 10, 14) failed with `JaxRuntimeError: RESOURCE_EXHAUSTED: Out of memory while trying to allocate 385.32GiB [jit_log_l]` and SMC arms (3, 7, 11, 15) with `48.45GiB [jit_scan]` on an 80 GB A100: the gradient of the pixelized-inversion likelihood on the 15,361-pixel HST cell and SMC's 256-particle batched evaluation do not fit. Arms 18-23 were cancelled by the architect at 19:40Z to free the GPUs; arms 9, 13, 17 were left to finish.

Shape (autolens_inference, no library change):
1. `run.py`: serialise parameter names as dotted strings (`".".join(name)` for tuple names, else `str`), in both `max_likelihood_parameters` and `posterior_from_result` (the SLaM runner's own rows are fine: check how `_runner.posterior_from_result` names keys and reuse it); never let the row write itself raise after a completed fit: wrap the diagnostics extraction so a failure there is recorded in the row as `status: "complete; diagnostics failed: ..."` with the output path, rather than losing the row.
2. `wave.py`: `--attempt N` (default 1) appended to run ids as `_a<N>` for N > 1; accounting lists every attempt per arm; `--arms nautilus,emcee` (or a `--samplers` filter) so a submit can run a subset; NUTS and SMC arms marked `deferred` in wave 1 with the reason "A100 OOM 2026-10-17 (385 GiB NUTS, 48 GiB SMC)"; the accounting counts them as `deferred`, never `missing`.
3. GPU submit: `submit_hst_cleanslate_mass_samplers_jax_gpu_dense` takes the attempt and sampler filter from env (`PYAUTO_WAVE_ATTEMPT`, `PYAUTO_WAVE_SAMPLERS`) or a sibling submit for attempt 2 over the 16 nautilus+emcee arms (`--array` over their indices, `%4`, 6 h); no dependency needed now (the problems exist). CPU wave submit gets the same filter (not submitted).
4. Docs: searches README and `wiki/setups/rectangular.md` record the attempt-1 outcome and the deferral; `hpc/README.md` the attempt env.
5. Tests for the serialisation, the attempt suffix, the filter and the accounting.
6. After merge (authorised by the human's "get some runs going"): submit attempt 2 on RAL; record in Cortex and Insight (`hst_mass_samplers_wave1`: attempt 1 failed with reasons; attempt 2 job id; NUTS/SMC deferred pending a memory-feasible formulation, e.g. the sparse operator problem `hpc_a100_jax_gpu_sparse_fp64`, fewer particles, or a CPU problem with host memory).

Out of scope: making NUTS/SMC fit (that is a research task on the likelihood's gradient memory; file as a follow-up idea); recovering attempt-1 rows from the completed output trees (rerun instead; note the trees exist under `output/experiments/cs1017_*`).

Witness: `experiments/run.py` writes a complete JSON row for a nautilus and an emcee cold fit on a euclid test-mode prepared problem under the installed PyAutoFit (keys all strings, `posterior` and `max_likelihood_parameters` keyed by dotted parameter paths), a unit test feeds a samples object whose `names` are tuples and asserts the row serialises; `wave.py` gains an attempt suffix so re-runs of the same arm get a new run id while the wave accounting shows attempt 1 as `failed` with its reason and attempt 2 as the live row; the GPU wave submit for attempt 2 runs only the 16 nautilus+emcee arms; NUTS/SMC arms are `deferred` in the wave table with the OOM evidence; CI green.

Review-minutes: 20
Unattended: needs-slicing
