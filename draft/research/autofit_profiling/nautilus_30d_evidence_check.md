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
