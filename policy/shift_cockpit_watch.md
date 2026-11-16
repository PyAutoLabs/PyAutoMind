<!-- The carve-out to policy/end_at_deliverable.md, worded as the human approved it
     (DESIGN §3.1, H1 (a), H2 (b): 45 min). It lives on its own page because
     end_at_deliverable.md is stamped into every repo's AGENTS.md and is capped at
     10 lines; that page carries the ban and a pointer here. Enforced by
     policy/end_at_deliverable_hook.sh (PyAutoBrain#646). -->

## The one watch a session may hold: the shift cockpit (2026-11-16, human ruling)

A Claude session may keep one watch running past its turn only when all of these hold:

1. **The human asked for it in this session** ("watch the shift"), and the session is running
   the `cockpit` skill. No other skill, agent, shift worker or close-out session arms it.
2. **It is exactly the shift's event stream.** The watch is the `Monitor` tool running
   `<PyAutoBrain>/bin/pyauto-brain batch watch --stream --record <PyAutoMind>/batches/<slot>.md`
   (plus `--from`, `--for`, `--home`), with nothing before, after or around it. That command
   reads one local file the shift watcher writes. It makes no network call and spends no
   tokens until an event lands.
3. **The shift is open.** It may start only from 30 minutes before the brief's `dispatched:`
   to 45 minutes after its `review-at:` (the late-sweep window). The hook refuses it outside
   that window.
4. **It ends with the shift, and is not re-armed.** The stream exits at the shift's end, at
   `STOP`, or when the window closes. The session arms it again only after a `segment-end`
   line, which the stream prints just before Monitor's 30-minute limit while the shift is
   still open. After any other exit it never arms it again.
5. **Steering stays on the shift issue.** Every steering act is a comment from the human's
   login on the shift's issue, which the watcher reads. The chat may post that comment for
   the human, and it steers the shift in no other way.

Everything else `end_at_deliverable.md` bans stays banned, inside a shift as well as
outside it:
- `send_later`, `subscribe_pr_activity`, `CronCreate`, `ScheduleWakeup` and `/loop`;
- `RemoteTrigger` create, update and run;
- any `Monitor` or background command that watches GitHub (CI, a review, a merge, a PR, an
  issue), including one on a PR the shift itself opened.

A session that wants to know whether a PR is green reads it once and reports.
