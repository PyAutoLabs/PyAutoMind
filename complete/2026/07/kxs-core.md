## kxs-core
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/362 (open — series tracker; phases 3 + refactor pending)
- completed: 2026-07-08 (phase 2 + phase-4 docs leg)
- prs: PyAutoArray#363, PyAutoGalaxy#486, autolens_workspace#236 (all merged)
- notes: |
    k x s coupling core: divisibility rule, partial pre-bin util, direct-
    scatter mapper (exact by linearity, k-independent memory), call sites,
    padded simulation inherits adaptive sizes. Adaptive ground truth exact;
    863/946/336. Phase-4 fork resolved (c): executed simulators stay s=1;
    option (a) filed as feature/autolens_workspace/
    oversampled_psf_dataset_adoption.md. Phase 3 blocked by
    dpie-lenstool-param claim on autolens_workspace_test. Known gap for
    follow-up: segment ids not cached on OverSampler (per-eval cost).
