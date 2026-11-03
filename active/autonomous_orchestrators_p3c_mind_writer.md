# Autonomous orchestrators phase 3c: one Mind writer per shift — ledger lines via the lease directory, orchestrator commits from a temporary worktree

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
Witness: with a tmp bare-remote Mind: two fake workers each drop a claim and a close-out ledger file in their lease directories, the orchestrator commits both from a temporary worktree cherry-picked onto origin/main, the canonical checkout's `git status` is unchanged throughout, a concurrent unrelated commit on the remote is rebased over (never `reset --hard`, never force), and a worker attempting a direct Mind commit is refused by the worker contract; `pytest PyAutoBrain/tests -q` and PyAutoMind tests green
Review-minutes: 20
Unattended: never
Lane: local-dev

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md; slice of phase 3 (slicing: `complete/2026/11/autonomous-orchestrators-p3a.md`, prompt section "Slicing"; 3a shipped as PyAutoBrain#556).

Implements AUTONOMY.md "One Mind writer per shift — 2026-11-03". Reuse the temp-worktree + cherry-pick pattern the /prm close-out already uses under a dirty shared Mind; the dashboard self-heal bot is the only other mover of main and the orchestrator rebases over it.

<!-- filed by hand 2026-11-03 when phase 3 was sliced 3a–3d (human decision); headers mirror intake's -->
