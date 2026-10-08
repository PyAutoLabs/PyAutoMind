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

## search-ext-a2-objective-bridge
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1676
- issued: 2026-10-08
- prompt: active/search_extensibility_a2_objective_bridge.md
- epic: search-extensibility (phase A2; A3 runs in parallel in this worktree's second checkout `PyAutoFit_a3` on `feature/search-ext-a3-samples-checkpointer`; A3b stacks on both)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: library-shipped, awaiting-merge — PyAutoFit#1679 opened 2026-10-08 under --auto (decision-taken); A3 (#1677) integrating onto this branch, A3b (#1678) after both
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1679
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1679
- validation: 3453 passed / 1 skipped / 9 xfailed; nojax 1178; downstream suites green; Emcee+JAX 0.26 ms/call (eager 14.3 ms); BFGS-JAX exact gradients; one Fitness( site besides NSS
- decision-taken: docs/design/run_ctx.md Revision 1 (six member-level clarifications, signature unchanged); JAX fork rule forces 1 core with one INFO line + search.summary record instead of raising (D11 reading flagged)
- autonomy: --auto launch 2026-10-08 ("A2, A3, A3b and B3 in auto mode"); effective safe (refactor); Consequence judge → human /prm
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a2-objective-bridge
- repos:
  - PyAutoFit: feature/search-ext-a2-objective-bridge (+ feature/search-ext-a3-samples-checkpointer in PyAutoFit_a3; + feature/search-ext-a3b-nss-preflight stacked later)
- tier: judge (human /prm)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source)

## search-ext-b3-pilot
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/4
- issued: 2026-10-08
- prompt: active/search_extensibility_b3_wave1_pilot.md
- epic: search-extensibility (phase B3)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: workspace-dev
- autonomy: --auto launch 2026-10-08; effective supervised (feature@large); decide-and-flag at ship; Consequence judge → human /prm
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b3-pilot
- repos:
  - autofit_inference: feature/search-ext-b3-pilot
  - PyAutoInsight: feature/search-ext-b3-pilot
  - PyAutoCortex: feature/search-ext-b3-pilot
  - autofit_assistant: feature/search-ext-b3-pilot
- tier: judge (human /prm)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source)

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
