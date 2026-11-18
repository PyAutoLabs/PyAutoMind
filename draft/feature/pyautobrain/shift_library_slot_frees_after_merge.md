# M3.6i A shift's library slot frees once its task's PR has merged

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-18
Epic: autonomous-orchestrators
Consequence: judge
Witness: `python -m pytest tests/test_batch_plan.py tests/test_batch_named_tasks.py -q` passes with new tests that fail on today's main: (1) a brief naming two glance tasks on PyAutoGalaxy plans only the first while the first is live or its PR is open; (2) once the watcher's counters record the first as done with every PR in its `merged` list, the next tick's plan admits the second; (3) a first task done with an open (unmerged or refused) PR, or parked on a question, still holds the library; (4) a first task abandoned with no PR frees it
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-18, while launching shift 2026-11-18-pm (7 named glance bugs: 5 on PyAutoGalaxy,
2 on PyAutoFit): "but we can do the shift it does one task per library but over the shift it
will do all 7 in the end right one after another?" — then, told it does not: "do B".

Option B as offered: change the rule so a library's next named task starts once the previous
one on that library has merged.

## Why

`_batch.plan` admits one task per `LIBRARY_REPOS` repo per plan ("<repo> already claimed this
shift"). The watcher re-plans every tick, and `on_origin` keeps a task the shift already picked
in every later plan ("A task this shift already picked stays"). So the first PyAutoGalaxy pick
holds PyAutoGalaxy until `review-at:`, even after its glance close-out has merged it. A brief
naming five PyAutoGalaxy bugs runs one of them; the rest sit idle for hours.

The rule exists because concurrent library PRs collide at merge: the first merge moves `main`
and stales the others' test and smoke evidence. A task whose PR has already merged collides
with nothing, so holding its library past the merge serves no purpose.

## What to change

- The watcher tells the planner which of this shift's own picks no longer hold their
  libraries: done, with at least one PR and every PR in its `outcomes[task].merged`; or done or
  abandoned with no PR and no open question.
- `_batch.plan` keeps such a pick in the plan (so it is still known, counted and never
  re-dispatched) but does not add its repos to the claimed-library set.
- Anything else still holds: live, parked on a question, done with an open or refused PR (a
  judge PR waiting for `/prm`, a glance PR past `merge-cap:`).
- The next task on that library starts on a later tick, from a worktree cut from the merged
  `main` (start_library already branches from origin/main).
- AGENTS.md "The watcher" and batch.md say the slot frees at merge; `brief --check` wording
  stays ("will not start yet — PyAutoGalaxy held by <task> until its PR merges" is a nicer
  message than "already claimed this shift", if cheap).

## Not in scope

- Running two tasks on one library at once.
- Raising `merge-cap:` or changing close-out guards.
