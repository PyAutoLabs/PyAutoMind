# Remove remaining provider assumptions from agent metadata and docs

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
- @autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-09-17
Parent: draft/maintenance/organs/agent_harness_agnostic_setup.md
Blocked-by: codex_skill_discovery_parity

## Request

> Can you check that all Agent setup (skills, md files, etc) is agnostic to whether its claude or codex, been using claude for a while but gonna codex for the forseeable so worth an agnostic sweep

## Scope

Move the three remaining canonical nested `CLAUDE.md` bodies to `AGENTS.md`
with thin Claude adapters; accept both `claude/**` and `codex/**` ledger branch
names; make resume metadata provider-aware; remove mandatory false
Claude/Anthropic commit attribution; and correct stale Codex hook/support
claims. Preserve historical records verbatim.

## Acceptance

- Shared canonical guidance lives in `AGENTS.md`; `CLAUDE.md` only adapts it.
- Ledger-only session branches from either supported provider reach the same
  guarded merge path.
- New resume and attribution metadata never guesses a provider identity.
- Current setup/support documentation is backed by a bounded Codex smoke
  record and distinguishes tested behavior from intended support.
