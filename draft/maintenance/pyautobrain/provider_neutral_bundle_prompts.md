# Make generated bundle prompts provider-neutral

Type: maintenance
Target: pyautobrain
Repos:
- @PyAutoBrain
- @PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-09-17
Parent: draft/maintenance/organs/agent_harness_agnostic_setup.md

## Request

> Can you check that all Agent setup (skills, md files, etc) is agnostic to whether its claude or codex, been using claude for a while but gonna codex for the forseeable so worth an agnostic sweep

## Scope

Replace the Fable/Opus and `Agent(model="opus", ...)` instructions emitted by
the intake bundle renderer with the provider-neutral judgment-tier /
execution-tier contract already defined in `PyAutoBrain/skills/WORKFLOW.md`.
Update the dashboard tests to reject provider model names and harness-specific
subagent syntax, then regenerate the Mind Markdown and HTML dashboards.

## Acceptance

- A generated bundle prompt tells the current session to resolve the execution
  tier from `WORKFLOW.md` and use its harness-native subagent mechanism.
- Active generator code, tests and generated dashboards contain no hardcoded
  Fable/Opus/`Agent(model=...)` bundle contract.
- Existing one-issue, one-branch and one-PR-per-member semantics are unchanged.

