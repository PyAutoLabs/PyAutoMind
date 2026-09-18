## provider-neutral-bundle-prompts
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/383 (closed 2026-09-17)
- completed: 2026-09-17
- library-pr: PyAutoBrain#384 (merged `49d064d64e1078b2f56c68f5e9401b13269e50d9`)
- library-pr: PyAutoMind#406 (merged `a7a3473c8fba92314a43163a88f1ed36ff0c75fe`)
- pending-release: PyAutoBrain@https://github.com/PyAutoLabs/PyAutoBrain/pull/384
- pending-release: PyAutoMind@https://github.com/PyAutoLabs/PyAutoMind/pull/406
- heart-ack: 2026-09-17 — the human explicitly authorized this task to ship and merge despite the exact live RED reasons `install verification FAILED (testpypi; checks F)` and `release validation FAILED (stage integrate)`. The override was development-only and task-scoped; it did not authorize a release, waive required GitHub checks, or claim that this branch repaired Heart.
- what shipped: the intake bundle renderer now describes judgment and execution tiers provider-neutrally, resolves the execution tier from `PyAutoBrain/skills/WORKFLOW.md`, and tells the active harness to use its native subagent mechanism with a direct-execution fallback. Regression tests reject Fable, Opus and `Agent(model=...)` in generated bundle prompts; the Mind Markdown and HTML dashboards were regenerated.
- policy amendment: `AUTONOMY.md`, `skills/WORKFLOW.md`, both ship skills and `skills/prm/prm.md` now define the narrow live-human Heart-RED development override used here, including issue/PR/active-ledger recording, green-CI requirements, same-turn merge expiry, and explicit bans on release authorization, force merge and protection bypass. Focused policy tests cover the contract.
- validation: PyAutoBrain 901 tests passed; PyAutoMind 456 tests passed; focused override tests 19 passed; independent review CLEAN; smoke n/a; dashboard and lifecycle checks current. On the final Mind head, Dashboard Refresh passed, Spawn Drift privacy passed and its conditional drift job skipped. Both PR heads were proven ancestors of `origin/main` after merge.
- trap: PyAutoMind's first dashboard check ran before PyAutoBrain #384 reached `main`, so it used the old renderer and failed. The library-first merge made the new renderer available; after merging current Mind `main`, regenerating the dashboards and pushing normally, all checks passed. No CI or branch-protection bypass was used.
- follow-up: phase 2 remains `draft/maintenance/organs/codex_hook_parity.md`; the larger agent-harness-agnostic sweep remains deliberately phased in `draft/maintenance/organs/agent_harness_agnostic_setup.md`.

## Original prompt

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
Issued: 2026-09-17
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
