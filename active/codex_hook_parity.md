# Register safety hooks for Claude and Codex

Type: maintenance
Target: organs
Repos:
- @PyAutoMind
- @PyAutoBrain
- @autofit_assistant
- @autogalaxy_assistant
- @autolens_assistant
- @autocti_assistant
Difficulty: large
Autonomy: supervised
Priority: high
Status: issued
Filed: 2026-09-17
Issued: 2026-09-17
Parent: draft/maintenance/organs/agent_harness_agnostic_setup.md

## Request

> Can you check that all Agent setup (skills, md files, etc) is agnostic to whether its claude or codex, been using claude for a while but gonna codex for the forseeable so worth an agnostic sweep

## Scope

Extend the manifest-driven hook generator and drift tests to create tracked
Codex project-hook registration alongside Claude registration. Use generated
`.codex/hooks.json` as the Codex adapter. Reuse the compatible
end-at-deliverable, shared-Mind commit and assistant API-gate implementations;
test them with representative Codex hook payloads. Do not register the current
Claude-remote session bootstrap unchanged: either give it an explicitly
harness-aware entry point or document it as a separate follow-up.

## Acceptance

- Expected Claude and Codex safety-hook registrations are generated and
  drift-checked from one manifest/source.
- Allow, deny and malformed-input fixtures cover Codex `PreToolUse` payloads.
- Project trust and any remaining session-bootstrap asymmetry are stated
  accurately in setup documentation.
