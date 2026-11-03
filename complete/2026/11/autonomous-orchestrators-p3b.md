- epic: autonomous-orchestrators (phase 3b of 3a–3d; epic draft/feature/pyautobrain/autonomous_orchestrators_epic.md)
- summary: real shift workers on the 3a watcher core. PyAutoBrain#558: agents/conductors/batch/worker_template.md (the one worker prompt: /start_dev <path> --auto, brief path, end at deliverable, never commit to Mind, write <lease>/<task>.done); _orchestrator.py session_command (`claude --bg --name shift:<task> --permission-mode <mode> <prompt>`, never bare), RealSpawner parsing the printed `backgrounded · <id> · <name>` id, AgentsView over `claude agents --json --all` (working → heartbeat; blocked → parked after STALL_GRACE_S 15 min, never killed or re-dispatched; done + marker → released; done without → crashed, re-dispatched once), transcript_tokens (input + output + cache creation from the local transcript named by sessionId) and the brief token-budget refusal; real dispatch fenced to `sandbox: yes` until 3c. _brief.py worker-mode (default auto — human decision 2026-11-03; bypassPermissions refused) and sandbox. PyAutoMind#525 documents both keys.
- witness: 17 dispatch tests (fake claude + fake agents view), 16 watcher tests; live sandbox worker: states working → done, 26,510 tokens, `claude logs` rc 0, removed; full suites Brain 1473 (+1 opt-in live) / Mind 712; CI green first time.
- traps (CLI 2.1.316): `claude --bg` ignores --session-id (track the printed short id; full sessionId from `claude agents --json`); the live state word is `working`; --bg refuses an untrusted folder at once (exit 1, "Workspace not trusted") — task worktrees under the -wt root are untrusted, so workers launch from the workspace root; an empty "reply DONE" worker costs ~26k tokens (the startup context).
- next: 3c one Mind writer — lifts the sandbox fence.
- heart: YELLOW, reason set acknowledged by the human at ship; judge tier, human /prm.

## Original prompt

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
