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
