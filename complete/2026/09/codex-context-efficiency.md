## codex-context-efficiency
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/403
- completed: 2026-09-19
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/404
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/425
- pending-release: PyAutoBrain@https://github.com/PyAutoLabs/PyAutoBrain/pull/404
- pending-release: PyAutoMind@https://github.com/PyAutoLabs/PyAutoMind/pull/425

Delivered all five approved efficiency changes: slimmer entry instructions, conditional reference reads, bounded tool output, grouped/flat path resolution, and compact completed-phase handoffs. Added deterministic instruction-budget reporting. Safety and approval gates remain intact.

Both PRs merged after every applicable exact-head CI job passed. Merge receipts: Brain e0a0a10e5130eaa9efce7c82c19b79381319c2ac; Mind f6d43712a295a3c28e23445b253ff523b8e517e7. Git ancestry confirms both feature tips are merged.

Validation: Brain 982 tests and Mind 582 tests passed; Sphinx warnings-as-errors passed; independent Sol review CLEAN including CI fixes. Root instructions activated locally after merge; section and token-budget checks pass. Maintained root/Brain/Mind AGENTS total fell from 43,365 to 25,731 bytes (40.7%). These are static measurements, not measured billing savings. Local HPC/custom instructions preserved.

The broader draft maintenance/organs/reduce_session_token_load.md remains open: Cortex/Memory instruction work and completion-record redesign are outside this task. The pre-existing local deletion of workspace_resolver_fanout.md was preserved and excluded from this commit.

## Original prompt

# Reduce repeated Codex context after workspace regrouping

Type: maintenance
Target: organs
Repos:
- @PyAutoBrain
- @PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issued: 2026-09-19
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/403
Filed: 2026-09-19

## Original request

> Can you do another review of codex token usage, is there anything we can do to be more efficient? We did one recently and it helped, but theres more tasks with astra you can review to assess and we did the reorg of PyAutoLabs

Approval of the resulting five recommendations:

> ok do all of that

## Approved scope

1. Slim root, Brain and Mind instructions; preserve mandatory policies and provider-specific delegation.
2. Make workflow reference reads conditional on the environment and current step; reuse unchanged loaded instructions.
3. Bound tool output: targeted reads, summaries, failure excerpts and external full logs.
4. Correct grouped-layout path guidance using the existing repository resolver, preserving flat task-bundle/remote layouts.
5. Define compact handoffs at completed phase boundaries without interrupting authorized work or weakening independent review.

Keep Astra Medium unchanged, retain concise folder routing guides, and preserve every safety, approval, review, Heart and release gate. Related broader backlog: reduce_session_token_load.md; Cortex/Memory prose and completion-record redesign are outside this task.

## Implementation and validation

Use feature/codex-context-efficiency in isolated Brain and Mind worktrees. Move explanatory AGENTS prose to references, update authoritative generators rather than generated copies, shorten and index start/close workflow instructions, and add a deterministic context-size report/budget check for maintained surfaces. Validate generated blocks, grouped/flat path examples, existing installer/workflow tests and independent review. Record before/after bytes and lines; do not claim measured runtime savings from static size reductions.
