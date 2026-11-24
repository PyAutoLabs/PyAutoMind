# Resume three independently explored 30D checkpoints to matched ESS

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Consequence: judge
Autonomy: supervised
Lane: local-dev

## Original request

> ok continue the three 30D runs from their saved checkpoints for up to another hour locally and see how the evidence compares once each seed reaches ESS 10,000
>
> We have tokens to burn can you run autonomously for like an hour and see how far you get we are doing good investigations I dont think this needs much over sight

## Protocol

Resume copies of the three SHA-256-pinned terminal checkpoints in PR #33. Preserve each saved random stream, geometry, exploration cutoffs, native 400-point cadence, four networks and likelihood. Keep discarding exploration samples. Launch the three single-process CPU continuations concurrently in one shared wall-clock window of at most 3,600 seconds, retaining the existing 4 GiB sampled RSS limit per child. Stop each seed at its first native ESS ≥10,000 with at least 100 fresh samples per shell. Allow a short graceful-shutdown margin. Report a capped or failed seed separately. No new seed, restart from scratch, HPC submission or additional time window.

Verify starting hashes and prior estimates, native reopening, geometry and fresh counts, and independently reconstruct log evidence and ESS from raw shell likelihoods and volumes. Compare individually with analytic log evidence −36.76768815337412, each seed's earlier partial, and the separate seed-0 conditional study. Report the signs, magnitudes and limitations without a post-hoc tolerance or precision claim. Publish the measurements, keep original attempts recoverable and update the epic. [Predecessor PR](https://github.com/PyAutoLabs/autofit_profiling/pull/33) · [Canonical profiling producer task](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md).

Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/34
