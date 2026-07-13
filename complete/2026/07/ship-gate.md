## ship-gate
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/38 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/39 (merged)
- notes: |
    Autonomy series task 3. Audited the unattended-ship surface and firmed
    AUTONOMY.md's gate: tests (shipped + downstream dependents on public-API
    change), smoke where a script surface exists, review CLEAN, Heart GREEN
    or launch-acknowledged YELLOW (exact reason set, per launch). Key audit
    findings: shipped-repos-only pytest relied on the human PR reviewer;
    chronic YELLOW would dead-end autonomy without launch acknowledgement.
