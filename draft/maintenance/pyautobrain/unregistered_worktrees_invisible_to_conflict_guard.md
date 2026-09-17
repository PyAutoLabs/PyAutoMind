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
