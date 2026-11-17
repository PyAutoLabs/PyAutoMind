## The shift watcher — the one exemption to "sessions end at their deliverable" (2026-11-03)

`policy/end_at_deliverable.md` stands as written for every Claude session,
orchestrator and worker alike, and its hook keeps blocking them. This page
names the single thing that is allowed to keep time.

**The watcher is a deterministic script, not a session** (built in phase 3 of
the autonomous-orchestrators epic; a systemd user timer or cron entry). It polls
`gh pr checks`, the project `hpc/sync jobs` verb (never raw `squeue`) and Mind
state, and starts a Claude session (`claude --bg`) only when there is work to
do. No tokens are spent watching.

What keeps the exemption narrow:

- It **calls no Claude tool** and **arms nothing inside a session**. Its
  only `claude` calls are local CLI reads: `claude agents --json` for its
  workers, and `claude auth status --json` (the login probe, no model call)
  on a shift's first tick and when a worker shows as blocked. A session
  it starts is an ordinary session: it ends at its deliverable, and
  `send_later`, `ScheduleWakeup`, `CronCreate`, `RemoteTrigger` and `/loop`
  stay blocked for it.
- It **dispatches nothing without an open shift brief** — a
  `PyAutoMind/batches/<slot>.md` record carrying a `brief:` block whose
  `dispatched:` has passed and whose `review-at:` has not
  (`PyAutoBrain/AUTONOMY.md`, "Shift briefs and unattended `glance`"). A
  tick with no open brief does nothing. **It finds the brief itself** on
  Mind `origin/main`, read locally and never fetched for this, so only a
  pushed brief opens; two open briefs grant nothing, and it idles saying so.
  `PYAUTO_SHIFT_BRIEF` in its env file is only an override, honoured inside
  that brief's own window (2026-11-17, PyAutoBrain#659).
- **An expired CLI login holds it.** When the login probe finds `loggedIn:
  false` or a `loginExpiresAt` already passed, the watcher records a
  `login-expired` event ("CLI login expired: run `claude /login`"), never a
  worker "blocked on a person", and starts no worker until the probe passes.
- **It ends with the shift.** After `review-at:` it posts the digest and
  sweeps late arrivals; once `review-at:` + 45 min has passed and the digest
  is posted, it stops ticking that slot and renews no lease.
- **Kill switch:** it checks for a `STOP` file in its slot directory **first**,
  before reading anything else, and does nothing while that file exists. The
  human can also write it from their phone by commenting `/stop` on the
  shift's issue, or comment `/pause` to hold spawns, re-dispatches and new
  close-outs until `/resume` (reaps and mentions continue)
  (PyAutoBrain#622; `PyAutoBrain/AUTONOMY.md` watcher network surface,
  amendment 2026-11-13).

The watcher's per-shift event file may be watched by one cockpit session the human starts
(`shift_cockpit_watch.md`, "The one watch a session may hold"). That watch reads a local file,
ends with the shift, and is not in the control loop: closing the chat changes nothing.

Why it is this narrow: the timer rule was written after five batch members armed
hourly check-ins on 2026-08-31, and a mobile `/prm` re-armed a 60-minute
`send_later` hourly all night on 2026-09-03 with no task active, draining usage.
Both were sessions keeping time. The watcher keeps time so that no session has
to; anything wider than this page reopens those two nights.
