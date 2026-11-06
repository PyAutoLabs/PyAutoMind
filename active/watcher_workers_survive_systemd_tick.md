# Live workers die with the watcher's systemd tick; failed workers are never reaped

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-11-06
Issued: 2026-11-06
Epic: autonomous-orchestrators
Consequence: glance
Witness: the unit template carries `KillMode=process`; a real worker whose `claude agents` state is `failed` (no `.done`) is reaped as a crash at the next tick and re-dispatched once; a `failed` close-out is refused; `batch watch` shows it as ended; one systemd-run tick spawning a real `claude --bg` session leaves that session alive after the tick exits; the full Brain suite passes
Review-minutes: 10
Unattended: never
Lane: local-dev

Pilot live shift 1 (2026-11-06, PyAutoMind#542): all 3 workers were killed about 30 seconds after spawn, because systemd's default KillMode=control-group took the claude --bg daemon down with the oneshot tick. The watcher then held their leases for 40 minutes because it reads `failed` as alive. Human: "yes do the fix".

<!-- filed by hand 2026-11-06; headers mirror intake's -->
