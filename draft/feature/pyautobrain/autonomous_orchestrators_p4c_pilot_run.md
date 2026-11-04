# Autonomous orchestrators phase 4c: run the Dev orchestrator pilot (2 shadow + ≥4 live shifts)

Type: research
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: human-required
Priority: high
Status: formalised
Filed: 2026-11-04
Epic: autonomous-orchestrators
Phase: 4
Blocked-by: draft/feature/pyautobrain/autonomous_orchestrators_p4b_unattended_closeout.md
Consequence: judge
Witness: `PyAutoMind/batches/pilot.md` holds ≥ 6 shift rows, the 2 shadow baseline rows included, each with `review-minutes-actual` filled; a write-up evaluates the epic's "Success measures (pilot)" against them (planned vs actual minutes within 25 % by the sixth shift, revert/corrective-PR rate vs the calibration log, verified work per review-minute vs the shadow baseline); it records whether `claude --bg` workers are attachable and whether they appear in the desktop app's session list, and whether Claude Code Projects is available in the UI
Review-minutes: 60
Unattended: never
Lane: local-dev

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md, phase 4; slice 4c of 4a–4c. Mostly the human's time: this slice is the pilot itself, not code. Any fix it uncovers is filed as its own prompt.

1. **The human installs the watcher timer.** The steps are in `PyAutoBrain/agents/conductors/batch/AGENTS.md` "Installing the timer is the human's act"; no session installs it.
2. **Two shadow shifts** (`shadow: yes`, from 4a) set the baseline: the orchestrator proposes and digests, and the human works as today and logs minutes.
3. **At least four live shifts:** 2–3 workers, 2 h each, only `notify` / `glance` work plus invariance or refactor tasks, `glance` merges under the 4b guards with `merge-cap:` set in each brief.
4. **First-shift checks:** `claude attach <id>` on a live worker, and whether `--bg` sessions show in the desktop app, recorded either way. Check Claude Code Projects in the UI; if it is there, trial it for the cloud lane only, with Mind and auto-memory kept as the sources of truth.
5. **Write-up** at `complete/` close-out: the success measures, the overrule rate, and a recommendation on loosening "Goal decomposition files drafts only" (AUTONOMY.md, which says it is never loosened before this evidence exists).

Tier: judge — merge mode: human `/prm`.

<!-- filed by hand 2026-11-04 when phase 4 was sliced 4a–4c (agent proposal, human approved filing); headers mirror intake's -->
