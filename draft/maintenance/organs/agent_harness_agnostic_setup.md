# Make agent setup Claude/Codex agnostic

Type: maintenance
Target: organs
Repos:
- @PyAutoBrain
- @PyAutoMind
- @PyAutoMemory
- @autofit_assistant
- @autogalaxy_assistant
- @autolens_assistant
- @autocti_assistant
- @autofit_workspace
- @autogalaxy_workspace
- @autolens_workspace
- @autolens_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-09-17

## Request

> Can you check that all Agent setup (skills, md files, etc) is agnostic to whether its claude or codex, been using claude for a while but gonna codex for the forseeable so worth an agnostic sweep

## Audit findings to resolve

The 2026-09-17 read-only sweep found that the shared Brain workflow is mostly
portable, but several live surfaces remain Claude-specific:

1. Generated bundle prompts hardcode Fable, Opus and
   `Agent(model="opus", ...)` instead of following the provider-aware execution
   tier in `PyAutoBrain/skills/WORKFLOW.md`.
2. Hook generation and drift tests cover `.claude/settings.json` only even
   though Codex supports project `PreToolUse` hooks. The end-at-deliverable,
   PyAuto API and shared-Mind commit guards therefore lack tracked Codex
   registration.
3. The four science assistants expose flat `skills/*.md` through
   `.claude/skills` but provide no Codex-discoverable `SKILL.md` adapters.
   Several workspace-local skills have the same asymmetry.
4. Three nested instruction bodies remain canonical `CLAUDE.md` files without
   sibling `AGENTS.md` bodies.
5. Mind ledger auto-merge recognizes only `claude/**`; resume metadata and
   assistant commit attribution are also Claude-specific.
6. Setup documentation still states that Codex has no hooks and overstates the
   evidence for end-to-end Codex assistant support.

## Preferred phasing

1. Provider-neutral bundle prompt generation and regression tests.
2. Codex safety-hook registration and drift tests, reusing the compatible
   existing hook implementations while keeping session bootstrap explicitly
   harness-aware.
3. Generated Codex skill adapters for assistant and workspace-local skills,
   retaining the flat canonical bodies initially and assigning stable
   hyphenated Codex names.
4. Nested instruction, branch namespace, resume metadata, attribution and
   documentation cleanup, plus one bounded Codex harness smoke record.

## Acceptance

- No active generated prompt names a provider model or tool syntax.
- Claude and Codex hook registrations are generated and drift-checked, with
  allow/deny fixtures for the safety gates.
- Public assistant/workspace skills are discoverable by both harnesses from a
  single canonical body and inventory parity is tested.
- Canonical shared guidance lives in `AGENTS.md`; `CLAUDE.md` is an adapter.
- Branch, resume and attribution metadata describe the active harness rather
  than assuming Claude.
- Documentation matches current, tested behavior and distinguishes intentional
  provider adapters from shared policy.

## Progress — 2026-09-18

Phases 1 and 2 are complete: see `complete/2026/09/provider-neutral-bundle-prompts.md`
and `complete/2026/09/codex-hook-parity.md` (all six hook PRs merged).
Phases 3 and 4 remain; phase 3 is planned as PyAutoBrain#386.
