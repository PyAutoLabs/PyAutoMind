# Can CPU sampler workers feed GPU likelihood batches faster?

Type: research
Target: @autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Consequence: judge
Lane: local-dev

## Original request

> ok keep native serial training and move on to testing CPU workers feeding GPU likelihood batches. See if that speeds up the whole fit with the native sampler settings.

## Phase 4 local engineering pilot

Keep the native Gaussian-profile search.fit configuration (200 live points, 4 serial networks, update 200, logical batches of 100, normal output and stopping). Use a single persistent device owner, bounded sub-batches and ordered admission within each logical batch. Keep RNG, adaptation, checkpoint writes and training in the controller. Compare JAX CPU with serial host, one GPU with serial host at full width, one GPU with serial host at half width, and one GPU with two CPU threads for preparing half batches and evaluating independent read-only bound membership. Check which path runs on which device. No extra GPU context or likelihood per worker.

Use two paired seeds, reversed orders, an application-style 100-point Gaussian-profile likelihood and a more expensive replicated-data version with the same mathematical target. Measure complete fits including compile and pool lifecycle, first and warm batch timings, host work, transfers/dispatch to host-visible completion, and the number of objective executable shapes. Reuse PyAutoFit's chunk_slices/evaluate_in_chunks and link [variable-batch task](https://github.com/PyAutoLabs/PyAutoMind/blob/main/draft/bug/autofit/vmap_jit_recompiles_per_nautilus_batch_length.md). Validate fixed-width output masking on uneven tails, FP64 likelihood parity against NumPy on common points including high-likelihood points, ordered proposal accounting, evidence, posterior and ESS. Record fails or divergence. Advance only if the worker arm improves whole-fit wall by at least 5% on both seeds of a workload versus serial GPU at full width and beats its serial split control, with correctness intact. Compare CPU-only independently. Leave production native. [Canonical profiling producer task](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md). Draft PR, human merge.

Use 64 copies for the heavier case, average the repeated log likelihood, and use seeds 1 and 2. Compare common log likelihoods at rtol 5e-12 / atol 1e-8. For full fits require valid native stopping, absolute paired log-evidence difference <= 0.1, marginal means within 0.1 serial posterior standard deviations and relative ESS within 10%. Report trajectory equality separately.

Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/42

## Outcome

[Draft profiling PR #43](https://github.com/PyAutoLabs/autofit_profiling/pull/43) awaits human review. Neither workload met the registered speed criterion. Retain native defaults. [All paired timings and correctness checks](https://github.com/PyAutoLabs/autofit_profiling/blob/7db263c56cddd3c177aab815cce467b0393ed537/experiments/nautilus_gpu_feed/README.md).
