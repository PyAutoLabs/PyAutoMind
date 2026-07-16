## heart-testrun-wiring
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/83
- completed: 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/85 (merged)
- summary: evidence-chain audit fix 1 (campaign #155 Phase 2). test_run's server-first cloud verdict was unreachable from every real entrypoint (fetch_cloud inferred from results_dir); main() now passes fetch_cloud=True explicitly, local/cloud verdicts must both be green (AND), cloud_ready recorded, disagreements surfaced in the sidecar. Verified: real tick now source=cloud on the actual latest run.
