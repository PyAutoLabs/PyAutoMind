Programme task **M1.1** (epic `autonomous-orchestrators`, phase 8). Shipped as PyAutoBrain#604, merged 2026-11-12T17:03:58Z (eecd2d505). Issue PyAutoBrain#603, closed.

The four state-machine gaps in the shift watcher that the ecosystem review of 2026-11-10 confirmed are closed, all in `agents/conductors/batch/_orchestrator.py` and `_watch.py`:
- **CODE-1:** transitions are persisted as they happen, and a failed spawn becomes a refusal.
- **CODE-2:** a failed liveness read counts as unknown, a crash needs two unlisted reads, and the grace is 420 s.
- **ORCH-1:** a parked lease is kept, and its `.done` is still consumed.
- **ORCH-3:** GitHub's PR state decides every merge count:
  - A `merged` file counts only when GitHub says MERGED. While the PR is OPEN or GitHub can't be read, the slot stays held. A CLOSED PR is a refusal.
  - A non-merged verdict on a PR GitHub shows MERGED is recorded as "merged outside the close-out".
  - A merge GitHub confirms with no file counts.
- The `KeyError 'spawned'` on digest ticks is fixed.

**Witness** (command and observed result):
- `python -m pytest tests/test_orchestrator_*.py tests/test_batch_watch.py -q`: 134 passed, 1 skipped (base: 116 passed, 1 skipped).
- These witness tests pass:
  - `test_a_tick_that_raises_after_a_reap_keeps_the_outcome_and_never_redispatches`
  - `test_a_failing_claude_agents_read_leaves_live_workers_live[rc1|timeout|badjson]`
  - `test_a_parked_worker_that_finishes_after_review_at_is_a_late_arrival`
  - `test_a_github_merged_pr_with_no_closeout_file_counts_as_one_merge`
- All 18 new or rewritten tests fail against the base source (checked independently).
- PR CI: pytest 3.12 and 3.13 green (run 43264970985).

**Review:** an independent Opus review returned FINDINGS on ab48caa, two must-fix items on ORCH-3 (a `.closeout` beat GitHub, and a human's merge was counted as unattended). Both were fixed in 1898e11. The re-review was CLEAN.

**Heart:** RED at ship (PyAutoLens canonical checkout on a branch and dirty; install check F; release integrate). None of the reasons is in PyAutoBrain. The live human gave a development-only RED override plus the merge command ("Override + merge on green"), recorded on the issue, the PR, `active.md` and `autonomy_log.md`.

**Follow-ups** (out of scope): `draft/bug/pyautobrain/shift_watcher_followups_after_state_gaps.md`, 9 items. These include double counting in the write-before-delete window, spawn refusals retried every tick, close-outs still OPEN at `review-at`, and the digest wording for merges made outside the close-out.

There is no pending release: PyAutoBrain is an organ, not a published library.

## Original prompt

# Shift watcher: close four state-machine gaps before the next live shift

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: issued
Filed: 2026-11-10
Issued: 2026-11-12
Epic: autonomous-orchestrators
Consequence: glance
Witness: four new tests pass and the batch conductor's existing suite still passes: (1) a tick that raises after a reap does not dispatch the finished task again and keeps its outcome; (2) a failing `claude agents` call leaves both live workers live with crashes 0; (3) park, then `.done` appears, and the next tick records the outcome, tokens and a late-arrival line; (4) a PR that GitHub reports merged with no `.closeout` file counts as 1 merge and writes a stage-2 row
Review-minutes: 10
Unattended: never
Lane: any

Source: the ecosystem review of 2026-11-10, findings CODE-1, CODE-2, ORCH-1 and ORCH-3, each confirmed by an independent verifier. Report: https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm (private) and `Science/scratch/ecosystem_review_2026-11/REPORT.md`, Appendix A. Verifier notes: `verdicts/CODE-1.json`, `CODE-2.json`, `ORCH-1.json`, `ORCH-3.json` in that folder; reproduction scripts in `evidence/orch_code/`.

All four are in `agents/conductors/batch/_orchestrator.py`. Line numbers are as of Brain `c41d016`.

1. **A tick that fails part-way forgets what it already did (CODE-1).** The reap deletes a finished worker's lease and `.done` marker (`:446-447`) and consumes `.closeout` files, but counters are written only at the end of the tick (`:596`, `:638`). Any exception in between loses the transition. Reproduced: a finished task dispatched again, a second close-out session for the same PR, a merged verdict never counted.
   Fix: write counters (or an append-only event line) straight after the reap and after each spawn and close-out start; catch a per-task spawn failure, record it as a refusal and carry on; delete `.done` and `.closeout` only after the write.
2. **One failed liveness read declares every worker dead (CODE-2).** `AgentsView._load` returns an empty list when `claude agents --json --all` fails, times out or prints bad JSON (`:325-333`). The lease grace is 120 s (`:52`) against a measured median tick of 184 s.
   Fix: return a distinct "unknown" result and skip every liveness decision for that tick; require consecutive unlisted reads, or a positive ended state, before a crash is counted; set the grace to at least two measured tick intervals.
3. **A parked worker leaves the state machine for good (ORCH-1).** Parking unlinks the lease (`:457`); `leases()` reads `*.json` only (`:411-418`), so the reaper and the late sweep (`:540-541`) never read its `.done`. This is the stranded PR of the 2026-11-06-pm shift.
   Fix: keep the lease with state `parked`; let the reaper and the late sweep also pick up a `.done` for any parked task.
4. **The merge count trusts a local file, never GitHub (ORCH-3).** A close-out that merges and then ends before writing `.closeout` is recorded as refused (`:824-830`) and frees a cap slot (`:853-854`).
   Fix: before counting a merge, freeing a cap slot or marking a close-out refused, read the PR state (`gh pr view --json state,mergedAt,mergedBy`). Count a merge GitHub confirms even with no file, and write the stage-2 row from it.

Not in scope: moving shift state off the laptop (that is the cloud watcher design, `draft/feature/pyautobrain/shift_watcher_in_the_cloud.md`), and the `KeyError 'spawned'` in `main()` on digest ticks, which is worth fixing in the same PR if it is one line.

`Unattended: never` because a shift should not change the watcher that is running it.

<!-- filed 2026-11-10 by the ecosystem review (draft/research/pyautobrain/ecosystem_review_for_autonomous_runs.md); headers mirror intake's -->
