# Shared orchestration panel core and standards index

- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/465
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/466

Merged shared Ears-inspired orchestration panel, visible owner-supplied GitHub links mirrored in copied prompts, optional direction, exact preview, accessible copy feedback and complete over-budget download. Brain, Mind and Cortex renderers adopt the component. Added canonical standards index and Brain instruction pointer.

Merge: 5d764f6fc6e216d4bca67563b8dcaaef2919eb26. Both workflow runs and all three jobs passed (Python 3.12, 3.13, strict docs). Local validation: 1,195 tests; 10 browser viewport/theme cases plus clipboard denial, budget, isolation and pending-edit checks.

This completes only the core dependency phase. Remaining approved scope stays in draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md: Ears/Heart and other consumers, Mind-generated repo guidance, Scientist discovery, and published verification. No claim that all boards or instructions have migrated.

## Original prompt

# Shared orchestration panel core and standards index

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Consequence: judge
Status: active
Issued: 2026-10-05
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/465

## Overview
Implement the shared dashboard orchestration panel and canonical standards index. This is the dependency phase of the approved combined task `draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md`; user approved execution with “ok go”.

## Plan
- Extract an Ears-inspired reusable panel: heading, description, visible GitHub work links, optional direction, exact selectable preview, copy button and accessible feedback.
- Keep repository context in the visible links and copied prompt, with owner-supplied destinations and safe URL validation.
- Adopt the component in the Brain-owned Brain, Mind and Cortex renderers, preserving domain prompts and existing approval boundaries.
- Add a canonical standards index and panel contract alongside the existing sizing/navigation standards; make Brain's AGENTS.md point to that index.
- Validate rendering, mobile/desktop appearance, keyboard interaction, direction/preview/copy agreement, clipboard denial, escaping, multiple panels and prompt budgets.

Tier: judge — merge mode: human /prm. Dependent consumer and generated-guidance phases follow this API merge.

## Detailed implementation plan
Affected repo: PyAutoBrain only. Survey: main, clean, no active claim. Existing unrelated worktrees are preserved. Branch: feature/orchestration-panel-core. Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/orchestration-panel-core/PyAutoBrain.

`board/_theme.py`: add orchestration_panel with owner-supplied key/title/description/prompt/work_links/copy label. Shared CSS and JS use unique IDs and component-local queries. All text is escaped; work links require safe GitHub HTTPS destinations. The work links are appended to the portable prompt once; optional direction is appended as user context. Exact complete preview is the copy source. Copy feedback and selectable fallback are accessible; over-budget prompts retain the existing complete-file download behavior, never truncate.

`board/_board.py`: general operational review prompt plus the board's configured GitHub repository. `agents/conductors/intake/_intake.py`: general task planning prompt plus the resolved Mind GitHub home. `agents/conductors/cortex/_cortex.py`: reuse checkin_payload, preserve freshness status and the existing checkin-box anchor; expose Cortex's home plus registered project repository links where available. Do not submit compute, run sync, mutate science or approve development from page clicks.

`docs/standards.md`, `docs/board-orchestration.md`, docs index and `AGENTS.md`: canonical ownership, on-demand discovery, component contract, consumer matrix and rollout stages. Later phases add Mind repos_sync distribution, Scientist discovery links, Ears/Heart pilots and the remaining board consumers; do not claim those repos here.

Tests: extend shared-theme renderer coverage, existing Brain/Mind/Cortex tests and targeted browser witness including two panels, long/Unicode direction, immutable destination context, denial fallback and budget. Full Brain suite and strict docs build. Published readiness is currently STALE; fresh vitals gate at shipping.

## Original user request

ok go

Full original requirements: draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md.

## PR handoff — 2026-10-05

PR: https://github.com/PyAutoLabs/PyAutoBrain/pull/466
Commit: f2e8975
Validation: 1,195 Brain tests pass; strict Sphinx build passes; browser witness passes 10 size/theme cases plus denial fallback, full over-budget download, isolation and pending-edit feedback. Agent-surface and organ-code tenant firewall checks pass. Evidence in `tmp/orchestration-panel-core/`.

Heart: STALE at 2026-10-05T18:00:50Z, score 85; exact reason: `release validation stale: source moved since rehearsal (PyAutoNerves)`. No RED/YELLOW reasons. Development ship permitted; release remains blocked.

Awaiting human /prm. Organ PR is recorded as library-pr per REFERENCE.md. No published rollout claimed. After merge, regenerate Brain/Mind/Cortex and verify live artifacts, then continue the approved consumer and generated-guidance phases in the parent draft.
