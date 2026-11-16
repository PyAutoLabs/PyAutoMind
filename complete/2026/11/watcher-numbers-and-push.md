Programme tasks **M1.5** (PyAutoBrain#610) and **M1.6** (PyAutoBrain#611), epic `autonomous-orchestrators` phase 8, in one branch. Shipped as PyAutoMind#560 (204b8d94c) and PyAutoBrain#612 (f80cba7da), merged 2026-11-12. These were the last two tasks of M1.

**M1.5.** The findings were re-checked on Brain 68e263a: CODE-4, ORCH-7 and ORCH-8 partly hold, FLOW-6 and SIG-5 hold.
- Tokens:
  - Per-session usage is read every tick and replaced, never added.
  - Usage is deduplicated by message id. Cache-read and subagent transcripts are reported separately.
  - Unmeasured usage is `None` (refuses spawning) and is written `null`. After 3 unreadable reads the session's reservation counts instead.
  - A spawn reservation makes the cap bind on tick 1.
- The digest:
  - Counters come from per-worker exits and GitHub's merged state, read after a final reap.
  - New `### Workers` and `### Refusals` sections.
- One `batches/pilot/pilot.jsonl` line per shift, through one-Mind-writer upserts, with `pilot.md` rendered from it.
  - A late arrival amends the line and posts one correction comment.
  - A failed post is retried, at most 3 attempts, never after a timeout.

**M1.6.** ORCH-13 was re-checked and holds.
- Human rulings, live: the channel is a GitHub @mention on the digest issue; the posting identity is a bot token, `PYAUTO_SHIFT_GH_TOKEN`; the AUTONOMY.md network-surface amendment is signed off in full.
- One comment per blocked worker, derived from durable state, marked before posting and retried, including in the late sweep.
- The posting token is never passed to workers or close-outs.
- The digest warns when the poster is the mentioned account.

**Witness** (named tests, all passing):
- `test_orchestrator_tokens.py`
- `test_digest_counters.py`
- `test_orchestrator_mentions.py`
- `test_the_watchers_posting_token_never_reaches_a_worker_or_closeout`

Brain suite: 1747 passed. CI green on both PRs.

**Review:** three rounds of FINDINGS, all fixed or ruled by the human, then clean:
- a self-mention cannot notify;
- the amendment went beyond the ruling;
- a mention was lost on a crashed tick;
- one unreadable transcript blocked all spawns;
- subagent tokens were missed;
- the bot token leaked to workers;
- the `gh api user` call was unlisted;
- the doc did not match the code.

**Heart:** RED at ship (local canonical checkouts; install check F; release integrate). The live human gave a development-only override plus the merge command.

**Human acts before the next live shift:** create a bot account token (PyAutoMind `issues: write`), set `PYAUTO_SHIFT_GH_TOKEN` in the watcher's environment, and set `shift_watcher.mention_login`.

## Original prompt

# Shift watcher: a shift's numbers are right and kept

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Filed: 2026-11-12
Issued: 2026-11-12
Epic: autonomous-orchestrators
Consequence: glance
Witness: (1) `pytest tests/test_orchestrator_tokens.py`: a live fake worker's usage is in counters["tokens"] on the tick it is read, before any `.done`; a close-out session's usage is added; a transcript repeating one message id counts it once; an unreadable usage makes the next spawn refuse "token usage unavailable", never adds 0. (2) token-budget 100 with a 60-token spawn reservation spawns one worker on tick one and refuses the second. (3) `pytest tests/test_digest_counters.py`: a worker read as `killed` at first tick gives workers-crashed 1 and a line `spawned/crashed`; a PR a human merged before review-at counts in `merges`; a `.done` written after the last tick appears in the digest. (4) after finish_shift, `batches/pilot/pilot.jsonl` holds exactly one line for the slot; a late arrival sets `amended` on that line, never a second line. (5) `pytest tests/` passes offline.
Review-minutes: 20
Unattended: never
Lane: any

Source: programme M1.5; ecosystem review CODE-4, ORCH-7, ORCH-8, FLOW-6, SIG-5 (unverified by the review), **re-checked 2026-11-12 on PyAutoBrain origin/main 68e263a** (after #604 and #607): CODE-4 partly, ORCH-7 partly (parked undercount fixed by #604), ORCH-8 partly (late `.done` now reaches the record), FLOW-6 holds, SIG-5 holds. Out of scope: double-count on a dying tick and open close-outs at review-at (`draft/bug/pyautobrain/shift_watcher_followups_after_state_gaps.md` items 1 and 8).

1. **Tokens only at finish.** `_orchestrator.py:514-516` adds usage only when a lease ends; `_closeouts` (899-1046) never does. Read usage every tick for every live, parked and close-out session, stored per session (replace, never add).
2. **The measure.** `transcript_tokens` (406-419) sums input+output+cache-creation on every line (about 1.6× the per-message figure), drops cache-read, and returns 0 with no transcript. Deduplicate by message id, report cache-read separately, and return None when unavailable; None refuses spawning.
3. **The cap cannot bind on tick one.** 717-721 compares spent tokens only. Reserve a per-worker estimate at spawn until real usage replaces it.
4. **Digest from tallies.** `_digest.py:242-243` takes merges from `.done`/close-outs and crashes from a tally a failed launch never adds to (`_orchestrator.py:736`). Derive both from per-worker exit states (spawned, finished, crashed, parked, late) and from GitHub's merged state for each PR in the window; print one line per worker.
5. **No reap at finish.** `finish_shift` (846-848) builds from counters without `_reap`; reap first.
6. **Written once.** The pilot row is queued once (860) and the post marker is created before the post (872); the late sweep (778-820) amends only the record. Have the late sweep amend the row and post one correction comment; retry a failed post. Keep issue URLs out of `prs` (`parse_done`, `_digest.py:65-78`).
7. **One machine-readable row.** Append `batches/pilot/pilot.jsonl` (slot, mode, tokens by component, merged PR URLs with mergedBy and merge actor, per-worker exits, stall minutes, amended); keep `pilot.md` as its render. Live rows need non-null tokens.

<!-- filed 2026-11-12 by the programme lead session from a read-only re-check (programme M1.5) -->
