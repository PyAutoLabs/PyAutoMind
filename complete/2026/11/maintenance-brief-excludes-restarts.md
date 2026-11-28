Merged PyAutoBrain#743 (human /prm, 2026-11-28).

Human ruling 2026-11-28, from the review of shadow maintenance shift 2026-11-27-pm: **answered-question restarts stay out of maintenance shifts.** They restart in the next ordinary shift.

Every resume path is gated for a brief with a `maintenance:` block, shadow or live:
- `_brief.scope()` rejects resume records unless the brief names the task (an `/add` counts as named). Those tasks are listed under `backlog_gates.answered_deferred`, and the digest shows "Answered, left for the next ordinary shift".
- The watcher's in-shift restart (`released_here`) restarts only named tasks or the shift's own picks.
- `_batch.plan` is covered by `scope()`. Carry-over is unaffected.

A deferred task's answer is never used up.

**Also fixed:** a shadow shift's proposed picks were using up an answer's release (`parked_elsewhere`/`picked_in`), which would have stopped Q39–41 from ever resuming. Proposals are now skipped; live accounting is unchanged.

**"NOT RECORDED":** it was a misleading fallback label, not a gap. A resumed pick now names the answer's release.

**Checks:**
- 9 new tests; 8 fail on main.
- Full suite 2810 passed. Two local `test_prompt_budget` cases fail because of an old Node on the laptop; CI passes them.
- Independent Opus review CLEAN.
- Heart dev-ship GREEN.

## Original prompt

# A maintenance brief must not resume answered-question tasks

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-28
Issued: 2026-11-28
Epic: autonomous-orchestrators
Phase: 14
Consequence: judge
Witness: a test that fails on the base commit: a shadow or live maintenance brief (`maintenance:` block, `backlog: none`) beside an answered parked task proposes or starts only its generated tasks, never the answered resume; the same answered task still resumes in an ordinary brief
Review-minutes: 10
Lane: any
Unattended: never

Human ruling 2026-11-28 (review of shadow maintenance shift 2026-11-27-pm): **keep answered restarts out of maintenance shifts.**

That shift (`backlog: none`, generated tasks only) also proposed three answered-question restarts: `group_los_halos` (Q39), `group_subhalo_sensitivity` (Q40) and `vmap_jit_recompiles_per_nautilus_batch_length` (Q41). They come in through the resume path, which bypasses the dip rules, and the digest marks them "NOT RECORDED".

## What

In the planner and scope (`_brief.scope()` and the resume path in `_batch.py`/`_orchestrator.py`), a brief with a `maintenance:` block does not take answered resumes. Those tasks stay startable and restart in the next ordinary shift. Say so in the 14.3 docs. Also check what "NOT RECORDED" means in the digest for a resumed pick, and fix it if it's a gap.
