# M3.6a Shift launch preflight: shift issue, login probe, the watcher finds the open brief

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-17
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/659
Filed: 2026-11-17
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: `python -m pytest tests/test_batch_brief.py tests/test_orchestrator_*.py -q` passes with new tests that fail on today's main: (1) `batch brief --new` with a fake `gh` creates one PyAutoMind issue and writes its URL as `issue:`; (2) `brief --check` on a live brief without `issue:` exits non-zero and names the key; (3) a fake `claude` printing "Login reached its time limit" makes `brief --check` fail and makes the first tick log a `login-expired` event, not "blocked on a person"; (4) with two brief fixtures on a fake Mind origin/main the watcher ticks the one whose `dispatched:` has passed and `review-at:` has not, and with two open briefs it idles and logs "two open briefs"; (5) a tick after `review-at:` + 45 min exits without ticking work and leaves every lease file's mtime unchanged
Lane: local-dev
Unattended: never

## Why

Shift 2026-11-16-pm lost time at launch to four things the launch could have checked.

- **No shift issue.** The kick-off chat grepped `_brief.py` for `issue:`, found nothing and
  dropped it. `brief --check` passed. So there was no live status comment, no steering by
  comment, no `/cap`, and the digest and the late-arrival correction were never posted
  (`digest.posted`: "the brief names no issue:").
- **Expired CLI login.** Both first workers stopped at 17:54:48Z and restarted at 17:56:36Z
  after the human's `/login` and a message from the kick-off chat. The watcher called it
  "blocked on a person".
- **Watcher on the old brief.** The 17:49Z tick read "idle: review-at 2026-11-14T19:35Z has
  passed", because `PYAUTO_SHIFT_BRIEF` in the env file still named the 14 Nov brief. The
  human edited the env file and the chat fast-forwarded the shared Mind checkout. 5 minutes
  lost.
- **The watcher never stops.** On 2026-11-17 it was still ticking every 3 minutes and still
  renewing the lease on the question the human had answered.

## What

1. `batch brief --new` creates the shift issue on PyAutoMind and writes `issue:` into the
   brief. `brief --check` refuses a live brief (not `shadow: yes`) without `issue:`.
2. A login probe: `brief --check` and the first tick run a cheap `claude` call and refuse or
   pause with their own event wording ("CLI login expired: run `claude /login`"), distinct
   from "blocked on a person".
3. The watcher finds the brief itself. It reads `batches/*.md` on Mind `origin/main` and takes
   the one brief whose `dispatched:` has passed and whose `review-at:` has not. Two open
   briefs means it idles and says so. Only a pushed brief counts, so "pushing the brief is the
   launch" keeps its meaning. `PYAUTO_SHIFT_BRIEF` becomes an override, not the source.
4. Once the late window closes (`review-at:` + 45 min) the watcher stops ticking the slot and
   renewing its leases.

## Out of scope

- The watcher reading the shared Mind checkout at all: that is M4.3 and the infrastructure
  review.
- Worker SSH keys and the worker environment (infrastructure review).
- Raising caps by comment (`/cap` already exists; it needs the issue this task creates).
