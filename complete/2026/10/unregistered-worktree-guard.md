## unregistered-worktree-guard
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/470
- completed: 2026-10-06
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/474
- bundle: pyautobrain-worktree-guards

Merged PyAutoBrain#474 (db2aa37) into main 2026-10-06 via /prm (tier `notify`; PyAutoBrain has no PR test CI, gate was the local full Brain suite). Issue #470 closed.

worktree_check_conflict reads git worktree list for the requested repos and WARNs on any worktree no active.md claim covers (exit code unchanged). New report-only worktree_audit_orphans lists unclaimed worktrees with ahead/behind/dirty and flags zero-commit claims STALE? (48 orphans on the dev box at ship time; removes nothing). New tests/test_worktree_orphan_guard.py (8); full suite 1203 passed.

No workspace impact (Brain tooling only); no pending-release obligation.

## Original prompt

# Unregistered worktrees are invisible to the conflict guard

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: notify
Witness: a worktree that exists on disk but appears in no Mind registry is either reported by `worktree_check_conflict` (or an adjacent audit command) or is gone; demonstrated against the `scientific-workflow-language` HowToFit worktree named below.
Review-minutes: 0
Unattended: ready
Issued: 2026-10-05

`worktree_check_conflict <task> <repo>` decides whether a repo is claimed by
reading the PyAutoMind registries (`active.md`, `planned.md`, `parked.md`). A
worktree that exists on disk but is in none of them is therefore invisible to the
guard: it cannot report the conflict, because as far as the registry is concerned
the repo is free.

Concrete instance, found 2026-09-14:

    /home/jammy/Code/PyAutoLabs/.worktrees/scientific-workflow-language/HowToFit
    branch: feature/scientific-workflow-language  (8883fcc)
    27 commits behind origin/main, 0 commits of its own, 0 changed files
    present in no Mind registry

Harmless in itself — the branch is empty, so any parallel work is disjoint by
construction — but it is debris, and it is debris of a kind the guard is
structurally unable to warn about. The same session also found the registered
`howtofit-mode` claim on HowToFit had 0 commits and 0 changed files, i.e. a live
claim that had never been used; between them, the registry both over-reports
(stale claims) and under-reports (orphan worktrees).

Two pieces of work, separable:

1. **Sweep the debris.** Remove `scientific-workflow-language` and audit for other
   worktrees on disk that no registry mentions, across all repos. `git worktree
   list` per repo versus the registries is the comparison.

2. **Close the blind spot.** Give the guard, or a companion audit, a view of what
   is actually on disk, so an unregistered worktree is reported rather than
   silently treated as "repo free". Related and worth deciding together: whether a
   registered claim with 0 commits and 0 changed files should decay or be
   reported as stale, since that is the over-reporting half of the same problem.

Existing related memory: the guard fires at REPO granularity, so a human routinely
approves a parallel worktree when file sets are disjoint. That judgement depends on
the guard's picture being complete, which this shows it is not.

Type: maintenance
Target: PyAutoBrain
Difficulty: small
Priority: normal

<!-- found during HowToFit#62 branch survey and close-out, 2026-09-14 -->
