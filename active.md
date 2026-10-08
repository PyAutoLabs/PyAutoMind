# Active Tasks

## timing-noise-audit-p4-ab-rule-semantics
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
- issued: 2026-10-02
- prompt: active/timing_noise_audit_phase4_ab_rule_semantics.md
- session: Claude Code CLI (Opus 5.5 worker under --auto, supervised), session 016CCA6BtzDgw16aUaVuzzL9
- status: workspace-dev
- autonomy: --auto launch 2026-10-08 ("do next phase auto and the one after"); effective supervised (bug, Consequence judge); decide-and-flag at ship
- worktree: ~/Code/PyAutoLabs-wt/timing-noise-audit-p4-ab-rule-semantics
- repos:
  - autolens_profiling: feature/timing-noise-audit-p4-ab-rule-semantics
- tier: judge (human /prm)
- heart-ack: none for this PR (the 2026-10-08 YELLOW ack covered #405 only)

## organ-banner-task-labels
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/organ-banner-task-labels
- repos:
  - PyAutoBrain: feature/organ-banner-task-labels
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/513
- issued: 2026-10-08
- prompt: active/organ_banner_task_labels.md
- session: Codex CLI, session ID unavailable
- status: library-shipped, awaiting-merge
- approval: corrected label plan approved; user explicitly authorized merge and publication and parking board-one-click-update
- tier: judge (explicit human merge authorization in current session)
- heart-ack:
  - manifest drift: end-at-deliverable blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - manifest drift: generated hooks (session-start + end-at-deliverable) — 3 mismatch(es) vs PyAutoMind/repos.yaml
  - manifest drift: hub organism blurb (organs present) — 2 mismatch(es) vs PyAutoMind/repos.yaml
  - manifest drift: organism-map blocks (generated) — 7 mismatch(es) vs PyAutoMind/repos.yaml
  - manifest drift: public front-door organ tables (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml
  - manifest drift: root AGENTS.md routing table (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - manifest drift: shared-standards blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - manifest drift: where-to-file blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - release validation incomplete: no rehearsal for current source
- heart-ack-authorization: user explicitly answered “Acknowledge; ship, merge and publish”
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/514
- validation: 1252 tests passed; tenant firewall passed; all 15 banners preserve artwork and styling; five browser widths passed
- next: await exact-head GitHub checks, merge under explicit user authorization, regenerate and verify all 15 published dashboards
