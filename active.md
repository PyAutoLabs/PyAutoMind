# Active Tasks

## timing-noise-audit-p4-ab-rule-semantics
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
- issued: 2026-10-02
- prompt: active/timing_noise_audit_phase4_ab_rule_semantics.md
- session: Claude Code CLI (Opus 5.5 worker under --auto, supervised), session 016CCA6BtzDgw16aUaVuzzL9
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/406
- autonomy: --auto launch 2026-10-08 ("do next phase auto and the one after"); effective supervised (bug, Consequence judge); decide-and-flag at ship
- worktree: ~/Code/PyAutoLabs-wt/timing-noise-audit-p4-ab-rule-semantics
- repos:
  - autolens_profiling: feature/timing-noise-audit-p4-ab-rule-semantics
- tier: judge (human /prm)
- heart-ack: YELLOW reason set (8 manifest drift + no rehearsal for current source) human-acknowledged 2026-10-08 for the remaining timing-noise phase PRs (same set as #405)
- decision-taken: C10 vmap rows/uncapped counts follow the tie set's point leader (flagged in PR)
- follow-up: phase 3b (C1/C3/C4/C5 intervals); Holm/Bonferroni policy
