## intake-census-dashboard
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/30 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/31 (merged)
- notes: |
    Added the planned census/dashboard follow-up modes to the Intake Agent.
    `intake census` inventories every filed prompt (WORK_TYPES folders +
    triage/), parsing the light header back out — taxonomy folder authoritative
    for work-type/target, headerless legacy prompts flagged as hygiene (77 of
    83), issued/ counted not itemised. `intake dashboard` renders it as the
    Mind *backlog* page; --apply wrote the first PyAutoMind/dashboard.md
    (317feb3). Backlog only — health stays the Heart's. Also fixed the intake
    --help sed range leaking shell lines. `repair` mode remains the planned
    follow-up. Shipped without pending-release (label absent on infra repo);
    Heart YELLOW on unrelated science-stack items, user-acknowledged.
