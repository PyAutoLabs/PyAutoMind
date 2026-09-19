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

## Resume request — 2026-09-19

> Find and finish the work to make the agentic AI ecosystem agent agnostic, we should be on phase 4

Phase 3 is still PyAutoBrain#386 (approved 2026-09-17, resumed 2026-09-19).
This phase remains gated on that work; plan approval was requested in the Codex
session on 2026-09-19 and has not yet been received.

## Proposed implementation plan

Branch: `feature/provider-agnostic-metadata` across the listed repositories.
Classification: workspace/infrastructure. Use task worktrees inside the workspace.

1. Move `PyAutoMemory/wiki/CLAUDE.md`,
   `autolens_workspace_test/scripts/CLAUDE.md`, and
   `autolens_workspace_test/scripts/misc/database/scrape/CLAUDE.md` to sibling
   `AGENTS.md` bodies. Replace the old files with thin imports; fix current
   links and references without rewriting historical records.
2. Extend `PyAutoMind/.github/workflows/mind_ledger_merge.yml` to trigger for
   `codex/**` as well as `claude/**`. Preserve the existing default-deny path
   classifier, permissions, conflict resolver, and review boundary. Extend
   `tests/test_ledger_merge.py` with both branch namespaces and a workflow
   trigger assertion; verify code/hook/workflow edits remain ineligible.
3. Replace assumed Claude resume commands in Brain start-dev/start-workspace
   registry templates and Mind REFERENCE with explicit harness/session fields.
   Record a resume command only when the active harness actually supplies it;
   unknown IDs stay unknown. Audit current consumers for assumptions before
   changing the schema. Preserve historical session records.
4. Update the four assistant AGENTS commit-attribution rules to identify the
   actual harness/model when known, never fabricate an Anthropic identity.
   Update active setup/support prose in Brain, Mind, Memory and assistants to
   distinguish shared instructions, generated adapters, and harness-specific
   mechanisms. Verify current product claims against local installed evidence
   and official documentation where needed.
5. Record a bounded Codex smoke: discover representative generated skills,
   resolve their canonical instructions, exercise a harmless workflow/read-only
   command, and test the applicable hook fixtures. State explicitly which
   checks exercised a real harness and which only tested adapter code. Do not
   claim full scientific-workflow or every-harness support from this smoke.
6. Run targeted Mind ledger/hook tests, Brain discovery/template tests, adapter
   drift checks, and instruction-link checks; obtain an independent review and
   Heart verdict, then prepare one PR per affected repo. Merge is a separate
   human action. Update the parent task only against observed completion.

## Branch survey — 2026-09-19

All eight phase-4 main checkouts are on `main`. Brain and the four assistants
are now claimed by phase 3, so phase 4 must follow it. Memory and
`autolens_workspace_test` are clean. Mind has an unrelated local deletion of
`draft/maintenance/pyautobrain/workspace_resolver_fanout.md`; preserve it.
The two assistant personal scripts noted in phase 3 also remain out of scope.
