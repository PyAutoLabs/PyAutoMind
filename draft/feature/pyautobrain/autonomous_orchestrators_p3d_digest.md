# Autonomous orchestrators phase 3d: `batch digest` — digest + proof packets, digest validator, one issue comment per shift

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
Epic: autonomous-orchestrators
Phase: 3
Consequence: judge
Witness: `batch digest` appends a `## Digest` to a fake shift's brief record matching `PyAutoMind/batches/AGENTS.md` (brief work vs backlog picks each with a one-line reason, one proof packet per task, every counter), `batch brief --check` gains a digest check that accepts it and refuses one missing a counter or a pick reason, and the digest is posted exactly once as a comment on a sandbox issue (a second run posts nothing); `pytest PyAutoBrain/tests -q` green
Review-minutes: 20
Unattended: never
Lane: local-dev

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md; slice of phase 3 (slicing: `complete/2026/11/autonomous-orchestrators-p3a.md`, prompt section "Slicing"; 3a shipped as PyAutoBrain#556).

Closes phase 3. The network surface for the comment is the one AUTONOMY.md names in 3a. The HTML packet stays opt-in (`packet: yes`).

<!-- filed by hand 2026-11-03 when phase 3 was sliced 3a–3d (human decision); headers mirror intake's -->
