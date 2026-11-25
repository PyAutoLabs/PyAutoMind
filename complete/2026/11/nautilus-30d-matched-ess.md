# Independent 30D evidence at matched ESS — merged

Merged 2026-11-25 under the human's `/prm`: [autofit_profiling#35](https://github.com/PyAutoLabs/autofit_profiling/pull/35), CI green, head an ancestor of origin/main.

## Delivered

- Continued the three independent 30D checkpoints from #33 under one shared deadline to fresh-only ESS ≥10,000 (`experiments/nautilus_30d_matched_ess/`).
- Evidence errors for seeds 1–3: −0.24%, −1.79%, +0.58%. The large early underestimate repeats across explorations; the residual at the registered endpoint has mixed signs.
- Independent reconstruction from 3,906,700 fresh samples reproduced every final log-evidence and ESS value.

## Original prompt

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

## Execution

All three source copies passed their registered checkpoint and evidence checks before sampling. Seed 2 reached ESS 10,002.99 and reopened with signed log-evidence error −0.018021. Seeds 1 and 3 continue under the same shared deadline.

## Result

[Draft profiling PR #35](https://github.com/PyAutoLabs/autofit_profiling/pull/35), stacked on #33, completes the matched-ESS comparison for the three independently learned 30D bounds. All three continuations reached fresh-only ESS ≥10,000 with at least 100 fresh points per shell within 49 min 27 s of one shared local hour. Compared with analytic log evidence −36.7676881534, the signed log-evidence errors were −0.002393, −0.018021 and +0.005755 for seeds 1, 2 and 3. These correspond to evidence errors of −0.24%, −1.79% and +0.58%. The earlier partial estimates were +0.42%, −1.76% and −0.35%; two signs changed. The additional likelihood calls were 174,400, 7,500 and 624,100 respectively.

The large early underestimate occurred in all three independent explorations. Its residual at matched ESS has mixed signs on this analytic fixture. Three full explorations give a descriptive comparison and leave uncertainty calibration open. The seed-0 conditional repetitions remain separate. Native reopening and independent HDF5 reconstruction matched all endpoints across 3,906,700 fresh samples. The original checkpoint hashes were preserved. [Per-seed comparison and receipts](https://github.com/PyAutoLabs/autofit_profiling/blob/04ca731d1ddd244f3dca034a28d6485efcf25477/experiments/nautilus_30d_matched_ess/README.md).

All 111 tooling tests passed on rerun; one supervisor timing test initially failed and passed in isolation. Ruff and catalogue validation passed. The phase 0b independent 30D endpoint check is complete. Wider 0b remains open, native cadence is retained, and Pulse promotion is deferred.
