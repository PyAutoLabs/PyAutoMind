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

- It **calls no Claude tool** and **arms nothing inside a session**. A session
  it starts is an ordinary session: it ends at its deliverable, and
  `send_later`, `ScheduleWakeup`, `CronCreate`, `RemoteTrigger` and `/loop`
  stay blocked for it.
- It **dispatches nothing without an open shift brief** — a
  `PyAutoMind/batches/<slot>.md` record carrying a `brief:` block whose
  `review-at:` has not passed (`PyAutoBrain/AUTONOMY.md`, "Shift briefs and
  unattended `glance`"). A tick with no open brief does nothing.
- **Kill switch:** it checks for a `STOP` file in its slot directory **first**,
  before reading anything else, and does nothing while that file exists.

Why it is this narrow: the timer rule was written after five batch members armed
hourly check-ins on 2026-08-31, and a mobile `/prm` re-armed a 60-minute
`send_later` hourly all night on 2026-09-03 with no task active, draining usage.
Both were sessions keeping time. The watcher keeps time so that no session has
to; anything wider than this page reopens those two nights.
