# Queue runner — generalize register_and_iterate into a work-type-agnostic loop

Type: feature
Target: autonomy
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft

## Why

The organism already has a working autonomous orchestrator:
`register_and_iterate` takes a queue of Mind prompts, drives
`start_dev → ship_*` per prompt, pauses only at named judgment gates, and
auto-advances — but it is welded to the pytree PoC (scaffold pattern,
classification heuristic, registration loop). Extracting the loop gives the
"orchestrator of multiple agents" capability generically, at low risk, because
the pattern is production-proven.

## What

1. Extract the generic loop into a new skill (working name `/run_queue`):
   read a queue file (default `PyAutoMind/queue.md`, or an explicit prompt
   list), and per entry run the dev lifecycle **at that task's effective
   autonomy level** — `safe` tasks straight to PR-open, `supervised` tasks via
   checkpoint-and-continue, `human-required` tasks skipped with a note.
2. Keep the blessed queue conventions: processed in order, done entries
   prepended `# DONE <date>`, never deleted.
3. **Batch report** at the end of a run: per task — outcome (PR URL / parked
   question / blocker), test+review verdicts, calibration-log rows appended.
4. Re-base `register_and_iterate` on the generic loop (its pytree-specific
   scaffold/classification becomes the task-type plugin), so there is one loop
   implementation, not two.

## Boundary decision (adversarial finding — settled)

The queue runner is a **skill**, not a new conductor. ORGANISM.md's consult
DAG forbids a conductor consulting conductors, and the precedent
(`register_and_iterate`) is a skill that drives the same lifecycle the human
would. Filing it as a conductor would force an amendment to the organism
doctrine for no gain. If during planning a genuine conductor-shaped need
emerges (a human-meaningful verb with its own decision object), stop and
re-plan rather than quietly promoting it.

## Boundaries

- Worktree conflicts: the runner must respect `active.md` claims
  (`worktree_check_conflict`) and run tasks serially unless claims are
  provably disjoint.
- Context/cost: one task per session-scale unit of work; the runner is a loop
  over sessions' worth of work, not one monster context.

Blocked-by: 4_auto_dev_mode.md, 5_checkpoint_and_continue.md.
