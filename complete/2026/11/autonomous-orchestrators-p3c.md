- epic: autonomous-orchestrators (phase 3c of 3a–3d; epic draft/feature/pyautobrain/autonomous_orchestrators_epic.md)
- summary: one Mind writer per shift (AUTONOMY.md "One Mind writer per shift — 2026-11-03", implemented and enforced). PyAutoBrain#560: agents/conductors/batch/_mind_writer.py — worker Mind changes queue as op files in <slot>/ledger/ (append | write | move | remove | drop-section), each path checked ledger-only by Mind's own scripts/ledger_merge.py (default deny); commit_ledger applies all pending ops in a temporary detached worktree on origin/main, commits once, pushes, and on a moved main replays the ops on the new origin/main (≤3 tries; no reset, no force — a test pins it); bin/shift_ledger.py (worker-side op CLI); bin/worker_git_hooks/pre-commit refuses a Mind commit under PYAUTO_SHIFT_WORKER=1 and chains other repos' own hooks via --git-common-dir; _orchestrator.py worker_env() injects core.hooksPath through GIT_CONFIG_COUNT/KEY/VALUE and each tick commits pending ops after the reap. The 3b sandbox fence is LIFTED (human decision 2026-11-03). PyAutoMind#526: sandbox is a test marker only.
- witness: tests/test_orchestrator_mind_writer.py 9/9 on real git (bare remote + canonical clone + racing clone: two workers land in one orchestrator commit, a concurrent commit is replayed over never forced, non-ledger path refused before anything moves, worker hook refuses a direct Mind commit); dispatch + watcher 33 passed 1 skipped; full suites Brain 1482 / Mind 712; tenant firewall OK.
- ci at merge: Brain pytest 3.12/3.13 pass; Mind dashboard refresh + privacy pass, spawn-drift `drift` job skipped (path-filtered).
- note: ledger ops live in <slot>/ledger/, the lease directory's sibling (AUTONOMY wording says "the lease directory") so ops outlive their lease. The PR asked for Mind#526 first; it merged seconds after Brain#560 (Mind PR was a one-line docs change, no dependency).
- next: 3d digest (draft/feature/pyautobrain/autonomous_orchestrators_p3d_digest.md), now unblocked.
- heart: YELLOW, reason set acknowledged by the human at ship; judge tier, human /prm 2026-11-04.

## Original prompt

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
