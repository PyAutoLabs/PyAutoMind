# Run orchestrator shifts from mobile (weekend away from the laptop)

Type: research
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: human-required
Priority: high
Status: draft
Filed: 2026-11-06
Epic: autonomous-orchestrators
Consequence: judge
Witness: from a phone only (no laptop keyboard), the human lands a shift brief, the watcher on the laptop opens it at `dispatched:`, workers run, the digest posts on its issue, the human reads it and runs `/prm` on one PR — each step recorded as it happened, including what failed
Review-minutes: 20
Unattended: never
Lane: any

Original request (human, 2026-11-06): "I am away this weekend so would like to try running this stuff on mobile, could we make a prompt to begin trying to set that up in a new mobile chat?"

## Where the pilot stands (PyAutoBrain#574, phase 4c)

- 4 of 6+ pilot shifts done: 2 shadow, 1 live that failed at spawn (systemd killed the workers; fixed in PyAutoBrain#593), 1 live re-run. The re-run's 3 named tasks gave 2 stale-prompt verdicts and 1 PR, autogalaxy_workspace_test#134, merged. Rows are in `batches/pilot/pilot.md`.
- Shift fixes since then, all merged: readable digest (#580), a shift opens at `dispatched:` (#590), `KillMode=process` + ended workers reaped (#593), no EnterWorktree + `decision-taken` label rule + late-arrival sweep (#595).
- How a shift runs today (`PyAutoBrain/agents/conductors/batch/AGENTS.md`, `PyAutoMind/batches/AGENTS.md`):
  - The human writes a brief into `PyAutoMind/batches/<slot>.md`, and that is the dispatch.
  - A **systemd user timer on the laptop** (WSL) runs `orchestrator_watch.py` every 2 min.
  - Real workers are `claude --bg` sessions on the laptop. The digest posts once on the brief's `issue:`.
  - Merges beyond the one unattended `glance` close-out are the human's `/prm`.

## What blocks running it from a phone (check each; do not assume)

1. **The laptop must stay up.** WSL's VM shuts down when idle, and `loginctl show-user jammy -p Linger` was `Linger=no` on 2026-11-06, so the user timer may not run with no terminal open. Needs: the laptop awake and plugged in, the WSL VM kept alive (`.wslconfig` `vmIdleTimeout`, or a keep-alive), and possibly `loginctl enable-linger` (the human's act).
2. **Landing a brief from the phone.** A brief committed to `PyAutoMind/main` from GitHub reaches the laptop only if the canonical Mind checkout is pulled. The watcher reads the local file. Options: the watcher reads the brief from `origin/main` (git fetch: is that inside its network surface? AUTONOMY.md "The watcher's network surface — 2026-11-03" allows only `gh pr checks`, `claude agents` and one comment, so this needs a ruling), or a separate pull timer.
3. **Pointing the timer at the brief.** `PYAUTO_SHIFT_BRIEF` in `~/.config/pyauto/orchestrator.env` names one brief, so every new shift means editing a laptop file. Proposal to evaluate: the watcher picks the open brief itself (the newest record in `batches/` whose window covers now).
4. **Reading and acting from the phone.** The digest is a GitHub issue comment (fine on mobile). `/prm` needs a Claude session with GitHub access: Claude Code on the web or app (cloud session, no `gh`; see `PyAutoBrain/skills/GITHUB_ACCESS.md`), or Remote Control of a laptop session. Worth testing which is real today.
5. **Attaching to a stuck worker** (`claude attach`) is laptop-only. With the #595 fixes it should be rarer; a parked worker posts its question on its issue.

## What this first mobile session should do

1. Read this prompt, PyAutoBrain#574 and `PyAutoMind/batches/pilot/pilot.md`. Find out what this surface can do: GitHub read/write? Remote Control? Mind commits?
2. Report which of blockers 1–5 can be worked around from mobile **this weekend** and which need laptop changes the human must make before leaving. Give the exact commands for each laptop step.
3. Propose the smallest path to one mobile-run live shift. Likely: keep-alive + linger on the laptop, the brief and env set before leaving, and only reading digests and `/prm` from the phone.
4. File any code change as its own draft prompt; do not build in this session. A watcher change to the network surface or brief discovery is `judge` and needs the human's ruling.

Next live shift candidates must be checked against current `main` before briefing: 2 of 3 named prompts in the last shift were stale.

<!-- filed by hand 2026-11-06 at the human's request; headers mirror intake's -->
