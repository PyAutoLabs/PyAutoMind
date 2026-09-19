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
Status: planned — blocked behind active repository claims
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
