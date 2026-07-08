# Checkpoint-and-continue — supervised runs batch questions instead of blocking

Type: feature
Target: autonomy
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

## Why

The proven pattern already exists: `register_and_iterate`'s autonomy contract
runs unattended except at named judgment gates, where it "writes a clear
question and stops" and auto-advances between tasks. Generalising it changes
the human's interaction model from answering interrupts live to reviewing a
batch of questions and PRs — the single biggest reduction in required input
for `supervised` (i.e. most) tasks.

## What

For `--auto` runs on tasks whose effective level is `supervised`:

1. At a judgment gate (per the `AUTONOMY.md` checkpoint table), write the
   question — with enough context to answer cold — to the task's GitHub issue,
   set the task's `active.md` status to `awaiting-input`, and **continue**: to
   the next independent step if one exists, else to the next queued task.
2. Keep questions **conversational and infrequent** — one batched comment per
   pause, not a trickle (consistent with the user-facing-issue update style).
3. On resume (human answers on the issue / relaunches), the run picks up from
   the recorded state — `active.md` is already the shared cross-environment
   task state, so no new state store.

## Boundaries

- Ship sign-off and merge remain checkpoints that *stop* the task (they park
  it as `awaiting-input`); checkpoint-and-continue never bypasses the gate,
  it only stops the human's *session* from being held hostage.
- No new registry or daemon — the issue + `active.md` are the whole mechanism.
- Genuine hard blockers still write up the blocker and park, exactly as
  `register_and_iterate` does today.

Blocked-by: 1_autonomy_contract.md. Pairs with 4_auto_dev_mode.md; consumed
wholesale by 7_queue_runner.md.
