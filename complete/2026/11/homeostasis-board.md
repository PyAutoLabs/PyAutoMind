Merged PyAutoBrain#748 (human /prm, 2026-11-28).

Human direction 2026-11-28: tasks spread over boards by type, each paired with its orchestrator (Physiology). Mind keeps the human's intent, the record, and work promoted to it. This is the first step: the **Homeostasis (maintenance orchestrator)** board, hosted on the Brain board (not on Heart, which is the readiness verdict).

**The board section** (`board/_homeostasis.py`, plus a `homeostasis.json` sidecar):
- Findings come from the `batch maintain` sources, each with key, source, tier, repo, witness and status.
- Status is read from Mind by the writer's marks: in progress, promoted, open, done, and a separate cleared list taken only from fresh, complete reads.
- The headline says "not all-clear" for any unread, stale or partial source.
- It fails soft: collection catches errors and SystemExit and has a 180 s bound. In the board job it reads the published Heart feed only.

**The Mind dashboard:**
- Generated glance prompts (a `Source-key:` header plus the writer's mark) leave Start here and the pick lists; one Homeostasis line replaces them.
- Generated judge prompts sit in a "Promoted from Homeostasis" group.
- `state.json` carries a yellow summary item.
- The writer caps `Priority:` at normal.

**Validation:**
- A local render matched `batch maintain` exactly (41 findings: 26 judge, 15 glance). Statuses were open 39, promoted 2, cleared 1 (`ci:PyAutoHands:Dashboard`, whose draft can be closed).
- Full suite 2844 passed.
- Independent Opus review over 3 rounds: minor findings only, the last CLEAN.
- Heart dev-ship GREEN.

**Follow-ups:**
- "done" needs Mind's close-out to carry the `Source-key:` (`draft/feature/pyautomind/close_out_carries_source_key_into_record.md`).
- Just-in-time filing comes later.

## Original prompt

# Homeostasis board on the Brain board; generated glance work leaves the Mind dashboard

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-11-28
Issued: 2026-11-28
Epic: autonomous-orchestrators
Phase: 14
Consequence: judge
Witness: (1) a local Brain board render (no publish) includes a "Homeostasis (maintenance orchestrator)" section and a `homeostasis.json` sidecar listing the live findings (key, source, tier, repo, witness, status open|promoted|in-progress|done|cleared) with the counts matching `batch maintain --dry-run`; (2) a Mind dashboard render shows no generated glance prompt (`Source-key:` + glance) in Start here or any pickable list, shows one collapsed Homeostasis line with the count and the Brain board link, and shows generated judge prompts in one "Promoted from Homeostasis" group; tests fail on the base commit
Review-minutes: 15
Lane: local-dev
Unattended: never

Human direction 2026-11-28: tasks spread over boards by type, each paired with its orchestrator (Physiology). Mind holds the human's intent and the record of work. Agent-generated work enters Mind only when promoted (it needs the human, or becomes source work). For maintenance, Homeostasis (maintenance orchestrator) gets its own board, hosted **on the Brain board for now**. It is not on Heart, which is the readiness verdict and should not hold a work queue. It moves out with Physiology when that is cut from the Brain later.

## What

1. **Brain board: Homeostasis section and `homeostasis.json` sidecar.**
   - Findings come from the same sources as `batch maintain`: the published Heart board, the census and the hygiene ledger.
   - Each finding's status is derived from Mind `main` by `Source-key:`:
     - open: no prompt;
     - promoted: a judge prompt in draft;
     - in-progress: the prompt is in active/;
     - done: a complete/ record with that key;
     - cleared: the key is no longer reported.
   - The same fail-closed and read-flag rules apply (an unread source is shown as unread, never as "all clear").
2. **Mind dashboard** (the renderer is Brain's intake):
   - Generated glance prompts leave Start here and all pickable lists; one collapsed Homeostasis line with the count and the Brain board link replaces them.
   - Generated judge prompts appear in one "Promoted from Homeostasis" group.
3. **Writer:** generated prompts no longer get `Priority: high` (use the finding's own priority, at most `normal`).

## Later (not here)

Full just-in-time filing: glance prompts stop living in Mind `draft/` at all and are filed only when a shift names them. Shift workers and claims need a prompt file today, so that change waits.
