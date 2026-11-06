# Move the shift watcher off the laptop: a cloud-run orchestrator

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: human-required
Priority: normal
Status: draft
Filed: 2026-11-06
Epic: autonomous-orchestrators
Consequence: judge
Review-minutes: 30
Unattended: never
Lane: any

Human (2026-11-06): "I want it to run on web server mobile if thats feasible?" Today the watcher is a systemd user timer on the laptop (WSL) spawning `claude --bg` workers there. AUTONOMY.md "The watcher's network surface — 2026-11-03" makes it "opt-in and laptop-only". The weekend of 2026-11-07 runs a **manual** cloud lane instead (the human starts Claude Code web sessions from the phone; kit in `draft/feature/pyautobrain/mobile_shift_operation.md`).

Questions to settle before any build (each is the human's ruling):
1. Where does the tick run: a scheduled cloud routine, GitHub Actions cron, or a small always-on host? Each changes the watcher's network surface (it would need to read Mind from GitHub and start sessions remotely).
2. How does it start a worker: a cloud Claude Code session per task (API or trigger), with no shared filesystem, so leases, `.done` and proof packets move to GitHub (PR body/comments) or Mind ops.
3. What becomes of the one-Mind-writer, the kill switch (`STOP` file) and the token cap when there is no local slot directory.
4. A dated AUTONOMY.md edit widening "laptop-only".

Evidence to gather first: the manual cloud lane's results (does a cloud worker reach a clean PR on organ, Hands and assistant repos; what it cannot do).

<!-- filed by hand 2026-11-06; headers mirror intake's -->
