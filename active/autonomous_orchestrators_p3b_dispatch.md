# Autonomous orchestrators phase 3b: real dispatch — session template, `claude --bg` workers, liveness, token budget

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: human-required
Priority: high
Status: formalised
Filed: 2026-11-03
Issued: 2026-11-03
Epic: autonomous-orchestrators
Phase: 3
Consequence: judge
Witness: `batch dispatch` builds the worker command from the orchestrator's session template (sources, bootstrap, brief path, `/start_dev <path> --auto`, the end-at-deliverable contract) and a unit test asserts it is never bare; with `PYAUTO_ORCHESTRATOR_FAKE=0` on the laptop one `claude --bg` worker is spawned against a no-op sandbox prompt, appears in `claude agents --json`, is attachable, and its lease heartbeat follows its liveness; the brief's `token-budget:` is decremented from the worker's final usage and the N+1th spawn past it is refused; the worker permission mode is declared (decided with the human) and a worker that hits a prompt is reported, not left stalled; `pytest PyAutoBrain/tests -q` green
Review-minutes: 20
Unattended: never
Lane: local-dev

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md; slice of phase 3 (slicing: `complete/2026/11/autonomous-orchestrators-p3a.md`, prompt section "Slicing"; 3a shipped as PyAutoBrain#556).

Real workers on top of the 3a watcher core. Decide with the human, at plan time, the worker permission mode (a `--bg` worker that hits a permission prompt stalls silently: auto mode plus the repo allowlists is the starting proposal). Recheck the CLI facts first (`claude --help`, `claude agents --help`; 2.1.316 on 2026-11-03 had `--bg`, `attach`, `logs`, `stop`, `rm`, `respawn`, and `agents --json [--all] [--cwd]`). Whether `--bg` sessions show in the desktop app is phase 4's first witness, not this one.

<!-- filed by hand 2026-11-03 when phase 3 was sliced 3a–3d (human decision); headers mirror intake's -->
