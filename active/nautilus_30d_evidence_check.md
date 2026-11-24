# Complete the conditional 30D Nautilus evidence check

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Consequence: judge
Autonomy: supervised
Lane: local-dev

## Original request

> ok continue with the 30D evidence accuracy check in phase 0b

## Protocol

Use the original phase 0b.2 analytic 30D target, learned seed-0 bounds, native cadence, four neural networks, 400 live points, batch 100 and single-thread numerical libraries. Run its three specified conditional streams. Continue the saved stream from a copy of the hash-pinned partial checkpoint, verify the published posterior after applying the native exploration-exclusion switch and fully persist that mode before advancing. Start resampling seeds 1 and 2 from separate copies of the original seed-0 checkpoint, retaining identical learned bounds and changing only the shared RNG state. Require ESS at least 10,000, at least 100 fresh samples per shell, exclusion of exploration points, exact posterior and evidence after native reopening, unchanged source hashes and no new bounds. Report signed evidence errors against the analytic truth, posterior-moment errors, ESS, calls and conditional spread. Keep the previous timeout as a separate outcome. The original protocol prescribed no numerical pass band; do not choose one after seeing results.

This new bounded local follow-up permits three single-process children, each capped at 1,800 seconds and 4 GiB RSS, up to three concurrently, without retries or remote compute. Report failures and partial attempts. Inspect the established [profiling task](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md) and [original protocol](https://github.com/PyAutoLabs/autofit_profiling/blob/main/experiments/nautilus_30d_diagnostics/protocol.json). Conditional replication cannot measure between-exploration uncertainty. Publish the reproducible experiment and receipts in a draft PR; update the epic and leave merge to human review.

Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/30

## Execution

All three pinned starting checkpoints passed their identity checks. The saved partial was corrected on its copy and matched the published posterior before advancing. Resampling seeds 1 and 2 began with the original 34,100-call exploration and zero fresh samples. An independent eigendecomposition gives analytic log evidence −36.76768815337412. The earlier timeout remains separate.

## Result

[Draft profiling PR #31](https://github.com/PyAutoLabs/autofit_profiling/pull/31) completes the three registered conditional 30D streams on the original seed-0 learned bounds. Each met fresh-only ESS 10,000 and the 100-per-shell minimum at native cadence. Against analytic log evidence −36.7676881534, the signed errors were −0.029026 (saved), −0.048116 (resampling seed 1) and −0.027755 (seed 2). Final fresh counts were 980,300, 636,100 and 835,600. All estimates were low by 2.74–4.70% on the evidence scale, compared with 59.67% for the original exploration-inclusive run. The earlier 120-second timeout remains incomplete.

All three native checkpoints reopened exactly. Independent reconstruction from 2,452,000 fresh rows confirmed evidence and ESS, and checksums verified the original inputs remained intact. [Report, per-stream receipts and independent checks](https://github.com/PyAutoLabs/autofit_profiling/blob/10c951cae4c875321048c6ab7841bca10e85896c/experiments/nautilus_30d_evidence_check/README.md). All 111 tooling tests, Ruff and the catalogue check passed. The draft PR awaits human review.

The conditional 30D evidence check is complete. The original protocol set no numerical pass band. All three streams share one exploration, and both sample selection and sample count changed from the original fit. The remaining 30D accuracy question is sensitivity across independently learned bounds. Wider phase 0b remains open, native cadence is retained and Pulse promotion stays deferred.
