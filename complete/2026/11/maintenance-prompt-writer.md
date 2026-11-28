Merged PyAutoBrain#734 (human /prm, 2026-11-27). Phase 14.2 of the maintenance orchestrator.

`batch maintain --file --mind <path>` (`agents/conductors/batch/_maintain_write.py`) turns 14.1's findings into sized, tiered prompts at `draft/maintenance/<target>/maint_<key>.md`, with no human writing them.

- **Prompt:** a `Source-key:` header and key mark, the evidence, a re-check-first step and the witness. Intake gives the type, target and lane; sizing gives the difficulty. The tier floor sets Consequence, and judge means `Unattended: never`. Glance prompts carry the surface rule: `no_run.yaml`, or a `ci:` row that excludes workflows, dependency pins and public names.
- **Read gating:** never files from, and never clears keys for, an unread, stale or partial read. Keys clear only when missing from a fresh read of their source. The CLI uses the union of fresh-source keys from before the dedupe.
- **Dedupe:** by key marks and whole-token mentions. State in `maintain.json`, migrated once from `heart_green.json`; a per-run cap.
- **Human-only, never filed:** release-execution workflows, and unit-test timing lines (when the board was read, its subjects decide; otherwise the roll-up does). Timing belongs to 14.5.
- **Write safety:** only into a linked-worktree or non-git Mind. The guard fails closed on git errors (`_mind_guard.py`). New files only.
- **One filing path:** `_green`'s file/pick modes go through the writer with the CLI's release adapter. A GREEN verdict keeps still-listed keys. `pick` names only existing ready drafts.

Live replay of the published feed and board into a throwaway Mind: 22 prompts filed, all passing `lifecycle.py check`. The Hands release run and the PyAutoGalaxy timing tests were held back for a human. The green lane kept all keys, and a re-run filed 0. Full suite 2692 passed. Independent Opus review, 4 rounds: majors fixed in each, the last CLEAN after a minor fixed in 1d8e324. Heart dev-ship GREEN.

## Original prompt

# Phase 14.2 Maintenance prompt writer: findings become sized prompts with no human writing them

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-27
Issued: 2026-11-27
Epic: autonomous-orchestrators
Phase: 14
Consequence: judge
Witness: `batch maintain --file` run twice on fixture findings writes each `draft/maintenance/<target>/maint_<key>.md` exactly once (Source-key header + state file dedupe), each passes `lifecycle.py check` and is graded by sizing; a finding that clears releases its key; writes go through the Mind writer, never the shared checkout; tests fail on the base commit
Review-minutes: 10
Lane: local-dev
Unattended: never

Slice 14.2 of `draft/feature/pyautobrain/maintenance_orchestrator.md`. Depends on 14.1. Buildable before the M3 gate
(human decision 1, 2026-11-27): it files drafts only, as `_green.py` already does.

## What

Generalise `_green.py`'s filing into the one maintenance writer (human decision 3: `_green` becomes an adapter):

- **Classify:** intake `analyse()` gives type, target and lane; sizing (`parse_prompt`, `effective_*`) gives difficulty and unattended.
- **Tier:** Consequence is the source's **tier floor** (human decision 2): glance for census marker removals, hygiene fixes and organ-CI reds; judge for public names, workflow files and dependency caps.
- **Header:** a `Source-key:` header and a body with the finding's evidence and its re-check-first step.
- **Dedupe:** by key mark, the state file and `queue.md`, carried over from `_green`. There is a per-brief cap.
- **Lifecycle:** a fixed finding clears its key, as `_green` does today.

## From 14.1 (merged 2026-11-27, PyAutoBrain#732)

- **Read flags:** honour every read's `ok`/`stale`/`partial`. Never file from, or clear keys for, an unread, stale or partial read.
- **Tier:** raise the tier above the finding's floor when the fix's diff touches anything beyond the finding's own surface (for a census row, anything other than `no_run.yaml`).
- **Keys:** use `Finding.key` as the `Source-key:` header.
