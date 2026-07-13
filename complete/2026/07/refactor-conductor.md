## refactor-conductor
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/44 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/45 (merged)
- notes: |
    Autonomy series task 6. agents/conductors/refactor/ (Renewal Agent):
    RefactorDecision with behaviour-preservation invariant + witnessing test
    suites, public-API guard (suspects re-route to feature/, never safe),
    candidates miner (backlog + ideas.md; files nothing). Reuses Feature
    Agent core by import. /refactor graduated from work-type shim to real
    conductor (AGENTS.md, COMMANDS.md, skill body, ROUTING.md). First
    conductor default-safe under --auto. Guard caught a real suspect
    (latent_class_redesign.md) during validation.
