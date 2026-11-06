- epic: autonomous-orchestrators (pilot 4c follow-up; issue PyAutoBrain#592)
- summary: PyAutoBrain#593. The watcher unit template gets `KillMode=process`: under the default control-group, systemd killed the `claude --bg` daemon (started by the first worker inside the oneshot tick) and every worker when the tick exited. `_digest.ENDED_STATES` (failed, killed, error, …): an ended real worker with no `.done` is a crash at once (no grace), re-dispatched once then abandoned; an ended close-out is refused; `batch watch` shows "ended (…)". Batch AGENTS.md documents both, plus the need to re-copy installed units.
- trigger: pilot live shift 1 (2026-11-06, PyAutoMind#542): 3 workers spawned 10:10:30, `failed` about 30 s later, no transcripts, 0 tokens; held their leases 40 min as "running"; digest said "not started" (explained on #542).
- witness: PASS. Real systemd check (transient oneshot units spawning a haiku `claude --bg` probe): KillMode=control-group → `failed` at unit exit; KillMode=process → `working`, then `done`. Control: old `_orchestrator.py` fails the new reaping tests (5). Brain 1633 passed; tenant firewall OK.
- human action owed: re-copy the unit (`cp …/bin/systemd/pyauto-orchestrator.service ~/.config/systemd/user/ && systemctl --user daemon-reload`), then re-run live shift 1.
- heart: STALE (21 h) acknowledged by the human at ship; glance tier, in-turn merge.

## Original prompt

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
