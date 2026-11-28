Merged PyAutoBrain#726 and PyAutoMind#611 (human /prm, 2026-11-27).

A parked task holds its library's start for 15 minutes (`PARK_HOLD_GRACE`), not the rest of the shift. This is ruling (d) as amended 2026-11-24. Inside the grace, held tasks count as startable, so the shift doesn't close early. After it:
- **Outcome park:** the library is released.
- **Lease park (blocked session):** stopped through the shared `/kill` stop path (`_stop_session`); the library is released once the reap sees the session end (human ruling 2026-11-27: "Stop, then release").
- **Failing closed:** a failed stop keeps the hold and raises `park-stop-failed`. A stopped session still alive after `PARK_STOP_END_S` (600 s) raises `park-stop-overdue`; the library stays held and the waiting task counts as final.
- **Answered parks:** an answered park waiting to restart keeps its library. The planner, claim gate and spawn loop share one hold wording, and the digest lists park holds on their own line.

Witness: 18 tests in `tests/test_parked_hold_grace.py`, all red on origin/main. They include a replay of the real 2026-11-24-am counters: the park is at 08:32:52Z, the tasks are held until 08:48Z and not ready to close early, and both held tasks start at +15 min instead of the 08:34Z early close. Full suite 2578 passed. Independent Opus review, three rounds: two majors fixed, round 3 CLEAN. Heart dev-ship GREEN.

Follow-up filed: `draft/bug/pyautobrain/second_park_of_same_task_files_no_new_question.md`.

## Original prompt

# A park on a question releases its library's start after 15 minutes (amend ruling (d))

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-11-24
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/720
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: orchestrator tests that fail on the base commit and pass after: (1) a task on PyAutoGalaxy parks on a question while a second named task waits on PyAutoGalaxy; for 15 minutes after the park the second task is refused as held but counted `startable`, so `early_close_ready` stays False; at the first tick after 15 minutes the second task spawns; (2) the same for a worker that ended with an open question in its outcome (PARKED-ON-ISSUE) instead of a lease park; (3) an answer that arrives after the grace while another worker is live on that library restarts the parked task only once the library is free, and two workers never run on one library; (4) an answer inside the grace restarts it as today. Plus a replay of the 2026-11-24-am counters showing `mge_deflections_reverse_mode_nan_at_grid_centre` and `jit_cache_not_hit_modeling_visualization` would have started at 15 minutes after `substructure_util_zero_padded_halo_slots_make` parked, instead of the shift closing early at 08:34Z
Lane: local-dev
Unattended: never

## Re-check (2026-11-24, at source on PyAutoBrain 76b5316)

Shift 2026-11-24-am closed early at 08:34Z (review-at 09:30Z) with
`mge_deflections_reverse_mode_nan_at_grid_centre` and `jit_cache_not_hit_modeling_visualization`
never started: `substructure_util_zero_padded_halo_slots_make` parked on a question while holding
PyAutoGalaxy and PyAutoLens. That is not a watcher fault. It is ruling (d) of 2026-11-19
(`AUTONOMY.md`, "approved, all six yes", M3.6j): "a park on a question keeps holding its
library's start". The holds live in `released_picks` (parked tasks, and done tasks whose outcome
carries an open question) and `_library_holder` (live, parked and re-dispatch-pending tasks),
both in `agents/conductors/batch/_orchestrator.py`. A held task is refused as `final`, not
`startable`, so with no lease live `early_close_ready` closes the shift. The early close is
correct under (d); the hour was lost to the hold.

## Human ruling (2026-11-24, in chat)

"Release after 15 min". Ruling (d) is amended: a park on a question (a lease park, or a worker
that ended with an open question in its outcome) holds its library's start for **15 minutes**
from the park, so a quick answer from the cockpit restarts it as today. After that the library
is released for the next task, as for a task whose worker ended with its PR open. An answer that
arrives later restarts the task only when its library is free; it waits like any other task.
Merges stay in PR order (rulings (a) to (c), S6), unchanged.

## What

- `_orchestrator.py`: the parked hold carries its start time (lease `parked_at`, or the `.done`
  arrival time for an outcome question) and expires at +15 min (one constant). Inside the grace
  a task held by it is refused but `startable`, so the shift stays open; after it, the hold is
  gone from `released_picks` and `_library_holder`. A restart after the grace goes through the
  same library check as every task.
- `AUTONOMY.md`: amend (d) in place with the date and this ruling, keeping the old text as
  history; `agents/conductors/batch/AGENTS.md` and Mind `batches/AGENTS.md` where they describe the
  parked hold and the early close.
- The digest's held reason says when the hold ends ("autogalaxy held by X (parked) until 08:49Z").

This changes the watcher, so it is never a shift task (organ rule): build it in chat, merged by
the human's `/prm`, deployed only when no shift is live.

## Why now

The M3 gate shift (draft brief in `Science/scratch/m3_gate_shift_2026-11/`) carries six
PyAutoFit tasks in series. Under (d), one park on the first stalls the other five for the rest
of the shift.
