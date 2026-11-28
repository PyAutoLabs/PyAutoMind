## parked-claim-not-a-claim
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/742
- completed: 2026-11-28
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/744
- Both claim readers (`worktree_list_claimed` in `bin/worktree.sh`, `claim_sections` in the batch planner) skip a `repos:` entry whose branch says `(no branch …)` and a branchless entry in an `awaiting-input` row with no worktree; real-branch and bare-with-worktree entries still claim.
- `worker_template.md`: a park before the first edit writes no `repos:` block. The observed row was free text in a shift worker's ledger append (Mind 7004216cd), committed through `_mind_writer`.
- The parked vmap-jit row's PyAutoFit claim was dropped on Mind main (1b99a15ec).
- Trap: the first CI run failed the tenant firewall (real repo names in new test fixtures in `test_batch_declared_repos.py`); the full local pytest suite does not run that check. Run `repos_sync.py --check --only "tenant firewall (organ code)"` before pushing Brain tests.
- Follow-up idea (not filed): refuse a `(no branch` repos bullet in `_mind_writer.validate_op` beside `pr_key_errors`.

## Original prompt

# A task parked before its first edit still claims its repo and starves the backlog

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-28
Issued: 2026-11-28
Epic: autonomous-orchestrators
Consequence: judge
Witness: (1) on Mind main, `active.md`'s `vmap-jit-recompiles-per-nautilus-batch-length` row no longer claims PyAutoFit, and a planner dry run (`pyauto-brain batch plan` or a shadow brief check) no longer skips PyAutoFit drafts as "repo PyAutoFit claimed by vmap-jit-recompiles-per-nautilus-batch-length"; (2) a test that fails on the base commit: an `active.md` row whose `repos:` entry has no branch (a task parked before implementation) is not returned by the claim readers (`worktree_list_claimed` in `bin/worktree.sh` and the batch planner's claim check), while a row with a real branch still is
Review-minutes: 10
Lane: any
Unattended: never

Found reviewing the shadow maintenance shift 2026-11-27-pm (human ruling 2026-11-28: "fix the PyAutoFit claim").

The shift digest skipped **80 PyAutoFit drafts** as "repo PyAutoFit claimed by `vmap-jit-recompiles-per-nautilus-batch-length`". That task parked on a question before any edit. It has no branch and no worktree. Its `active.md` row still lists:

```
- repos:
  - PyAutoFit: (no branch; parked before implementation — stated bug did not reproduce)
```

The question (Q41) has been answered ("Do 1"), so the task restarts in a later shift. It should claim PyAutoFit only when it actually starts work.

## What

1. **Now (Mind):** drop the `repos:` block from that row; keep the row itself (issue, question, prompt, status). Push through a temp worktree on origin/main. The restart claims PyAutoFit again when it begins.
2. **The rule (Brain):** a `repos:` entry with no branch (or a row whose status is `awaiting-input` with no worktree) is not a claim. Change the readers, not every writer: `worktree_list_claimed` in `bin/worktree.sh` and the batch planner's repo-claim check (`_batch.py` / `_brief.py` claim code, the "repo X claimed by Y" reason). Shift workers that park before their first edit should also stop writing a no-branch `repos:` entry: find where the shift worker or the watcher writes it and say which.
3. Tests for both readers; a real-branch claim still blocks.
