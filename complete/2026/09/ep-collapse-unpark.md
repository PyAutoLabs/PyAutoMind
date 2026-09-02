## ep-collapse-unpark
- issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/94
- completed: 2026-09-02
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/95 (merge 0c5c9f8d)
- epic: graphical-ep (phase 2 close-out; ledger draft/research/graphical_ep/ep_campaign.md)
- summary: |
    Un-parked `scripts/graphical/analytic_gaussian_collapse.py` (the phase-2
    collapse configuration on the closed-form referee) and curated it into
    `smoke_tests.txt`: with PyAutoFit#1558/#1560/#1562 every seed reads RECOVER
    (5/5, inside [q05, q95]), 15 s under the smoke profile, PASS on both CI legs.
    `analytic_gaussian.py` and `analytic_gaussian_priors.py` stay parked
    NEEDS_FIX in `config/build/no_run.yaml`, their reasons now pointing at the
    Laplace-on-scatter caveat (autofit/graphical/README.md §3.5) and the cure
    prompt `draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md`.
- traps: |
    A SILENT, STALE or PATHOLOGICAL verdict from this script is now a CI
    regression of the Laplace projection. The script's STALE note still
    describes the pre-#1562 warning rule as motivation; harmless, re-read if
    the classification is revisited.
