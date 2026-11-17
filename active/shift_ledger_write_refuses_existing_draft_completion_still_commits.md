# M3.6d A shift worker's edit to an existing Mind file is set aside, but its completion record still commits

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-17
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/660
Filed: 2026-11-16
Epic: autonomous-orchestrators
Phase: 10
Consequence: glance
Witness: `python -m pytest tests/test_orchestrator_mind_writer.py -q` passes with new tests that fail on today's main: (1) queueing `op: write` on a path that exists on Mind origin/main is refused at queue time and the worker is told; (2) the new edit op applies when the expected base matches and is set aside when it does not; (3) a worker with one op set aside has its `complete/` record held (no completion commit lands); (4) `shift_ledger table-append` reaches the first table of `autonomy_log.md` once the heading is there; (5) a mechanical set-aside gives one digest line and no NEEDS YOU event
Lane: any
Unattended: never

Seen in shift 2026-11-16-pm (18:21Z). Worker `dashboard_titles_two_drafts_by_their_filed_line` shipped as Mind ledger ops. Its three `op: write` edits to existing drafts were set aside ("write: <path> already exists", ledger `set_aside/`), raised as three NEEDS YOU lines, but its `complete/2026/11/dashboard-titles-filed-line.md` write committed. So Mind recorded the task shipped while the drafts were unchanged. The human applied the set-aside text by hand (cockpit, 2026-11-16).

1. Give the Mind writer an op that edits an existing file (a replace with an expected-base check, so it cannot clobber a concurrent change), and have the worker contract use it for edits; keep `write` create-only.
2. Make a worker's ledger ops land together: if any op is set aside, hold back its completion record (or mark the task not shipped) instead of committing it alone.
3. One NEEDS YOU line per worker for set-aside ops, naming the task, not one per file.

## Added 2026-11-17 (M3.6d, from the shift 2026-11-16-pm review)

This prompt is now milestone task M3.6d of the autonomous-orchestrators epic. Further
evidence from the same shift: four more `write` ops were set aside the same way (the record's
warnings list `sibson_serial_kernel_loses_allocation_hoisting.md`,
`delaunay_nn_numba_optimal_remeasure_after_677.md`,
`tutorial_correctness_and_howtogalaxy_parity.md` and `complete/2026/11/seed-samplers-byte-stable.md`).
PyAutoMind#579 is still open because of it. Five workers hit `table-append` failing on
`autonomy_log.md`, so no calibration row was queued for the shift's merges. The cockpit chat
applied four "needs you" events without waiting for the human, because they were mechanical
refusals.

4. **Refuse at queue time.** A `write` on a path that already exists on Mind origin/main is
   refused when the worker queues it, so the worker can switch to the edit op while it is
   still running, instead of the set-aside surfacing after the worker has ended.
5. **The edit op** in item 1 is part of this task, not a follow-up.
6. **A heading above the first `autonomy_log.md` table**, so `shift_ledger table-append` can
   reach it (it needs a `## ` heading). This is a Mind data change and goes in this task's
   Mind PR.
7. **A mechanical set-aside is not a "needs you" event.** It is a digest line (and, after
   M3.3 slice 2, an entry in the decisions block). Item 3 then applies only to set-asides that
   need a human choice.

Out of scope: the one network write path to Mind `main` (M4.3), and the auto-mode classifier
denying Mind lifecycle commands inside workers (infrastructure review).
