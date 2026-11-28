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
