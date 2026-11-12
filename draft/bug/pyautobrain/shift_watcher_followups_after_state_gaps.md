# Shift watcher: follow-ups found while closing the four state-machine gaps

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-12
Epic: autonomous-orchestrators
Consequence: glance
Witness: one test per item below fails on the M1.1 merge commit and passes after; the batch conductor's suite still passes
Review-minutes: 10
Unattended: never
Lane: any

Source: the implementing worker and the independent review of PyAutoBrain#603 (programme M1.1, 2026-11-12). Out of scope for #603; none blocks M1. All in `agents/conductors/batch/_orchestrator.py` / `_watch.py`.

1. **Write-before-delete can double-count.** Tokens and crashes are written before the lease is unlinked; a tick that dies in between re-reaps the same lease and adds them twice. Same for the stage-2 row if the tick dies between `queue_op` and `_write_counters`. Make the applies idempotent (e.g. key each applied transition by lease id + event in the counters file).
2. **A spawn refusal is retried every tick** and adds a refusal row each time; in the "printed no session id" case (rc 0) a session may already be running with no lease and `sessions` is never incremented. Decide: cap retries per task per shift, and on rc 0 with no id, look the session up in `claude agents` before refusing.
3. **A spawn that crashes leaves a lease with pid 0 and no agent id**; `_alive(0)` then calls `os.waitpid(0)`. Guard pid ≤ 0.
4. **A parked lease keeps `late_sweep` running** with one `claude agents` read per tick until the parked session ends; a parked worker a human unblocks runs without holding a worker slot.
5. **`batch watch` counts a `liveness-unknown` event as "reaped 1".**
6. **Some dispatch tests call the real `gh pr checks`** because they don't pass `health=`; inject a fake so the suite is offline.
7. **Digest wording for a merge outside the close-out.** `_digest.py` prefixes every refused close-out with "awaiting /prm", so a PR a human already merged reads "awaiting /prm — close-out refused: merged outside the close-out (mergedBy=…)". Give `merged_outside` its own digest line.

<!-- filed 2026-11-12 by the programme lead session from the #603 worker report and independent review -->
