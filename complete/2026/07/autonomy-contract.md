## autonomy-contract
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/34 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/35 (merged)
- notes: |
    Task 1 of the autonomy series. AUTONOMY.md is now the canonical autonomy
    contract: checkpoint inventory, levels x checkpoints table, per-work-type
    caps (refactor/test/maintenance -> safe; feature/bug/docs -> supervised;
    release -> human-required), explicit --auto activation, calibration-log
    spec (PyAutoMind/autonomy_log.md, seeded), hard invariants (merge always
    human; runs end at PR-open; Heart YELLOW never acknowledged
    autonomously). WORKFLOW.md model doctrine now tier-based (judgment tier
    currently Fable 5; execution tier Sonnet). Doctrine only — consumption
    lands with series tasks 2-7.
