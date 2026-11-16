## Sessions end at their deliverable

A session ends when it reports its deliverable — never arm anything that
outlives the turn to wait for CI, a review or a merge: no `send_later`, no
`subscribe_pr_activity`, `CronCreate`, `ScheduleWakeup`, `/loop`, `RemoteTrigger`
create/update/run, or `Monitor` or background loop on GitHub. Judge once, report,
stop; the human re-runs `/prm` (or the batch review) when it is green. The one
exception, the shift cockpit's stream: PyAutoMind `policy/shift_cockpit_watch.md`.
Measured: five batch members armed hourly check-ins on 2026-08-31, and a mobile
`/prm` re-armed a 60-minute `send_later` all night on 2026-09-03, draining usage.
