# Make assistant and workspace skills discoverable in Codex

Type: maintenance
Target: assistants
Repos:
- @PyAutoBrain
- @autofit_assistant
- @autogalaxy_assistant
- @autolens_assistant
- @autocti_assistant
- @autofit_workspace
- @autogalaxy_workspace
- @autolens_workspace
Difficulty: large
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-09-17
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/386
Filed: 2026-09-17
Parent: draft/maintenance/organs/agent_harness_agnostic_setup.md
Unblocked: 2026-09-19 — mass-field workspace PRs #560/#562 and workspace_test #322 merged; complete/2026/09/mass-field-flat-sweep.md

## Request

> Can you check that all Agent setup (skills, md files, etc) is agnostic to whether its claude or codex, been using claude for a while but gonna codex for the forseeable so worth an agnostic sweep

## Scope

Keep the existing flat assistant skill Markdown as canonical for this phase and
generate Codex-discoverable `<hyphenated-name>/SKILL.md` adapters for every
public assistant skill and the workspace-local skills. Drive discovery from
the repository/body map rather than another hardcoded installer list. Update
bootstrap instructions so new skills acquire both Claude and Codex adapters.

## Acceptance

- Public skill inventories have tested Claude/Codex parity.
- Every Codex adapter has a stable valid name, description and single
  canonical body; helper/internal Markdown is not exposed as a public skill.
- Name normalization is collision-checked across installed assistants.
- Existing Claude skill names and links continue to work.

## Resume request — 2026-09-19

> Find and finish the work to make the agentic AI ecosystem agent agnostic, we should be on phase 4

## Implementation — 2026-09-19

21 discovery regression tests passed; all 105 generated skills passed local validation and actual Codex runtime discovery. Existing Claude links resolve. Independent review: CLEAN. All PRs are open and labeled pending-release; awaiting human merge. Heart STALE: `release validation incomplete: no rehearsal for current source`; no release approval.

- https://github.com/PyAutoLabs/PyAutoBrain/pull/401
- https://github.com/PyAutoLabs/autofit_assistant/pull/48
- https://github.com/PyAutoLabs/autogalaxy_assistant/pull/27
- https://github.com/PyAutoLabs/autolens_assistant/pull/129
- https://github.com/PyAutoLabs/autocti_assistant/pull/30
- https://github.com/PyAutoLabs/autofit_workspace/pull/160
- https://github.com/PyAutoLabs/autogalaxy_workspace/pull/246
- https://github.com/PyAutoLabs/autolens_workspace/pull/568

Phase 4 shared-repository PRs stack on phase 3. Merge phase 3 first; Memory before running the updated Mind template generator, Brain smoke documentation before assistant documentation links. Worktrees retained until merge.
