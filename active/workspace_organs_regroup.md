# Group the infrastructure checkouts under organs

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoHeart
- PyAutoHands
- PyAutoCortex
- PyAutoMemory
- PyAutoNerves
- PyAutoGut
- PyAutoScientist
Difficulty: large
Autonomy: supervised
Consequence: judge
Status: approved — human said “ok go” after the two-phase plan
Filed: 2026-09-19
Issued: 2026-09-19
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/397
Witness: Flat and grouped infrastructure resolve identical repository identities; all 38 manifest checkouts, twelve smoke bootstraps, imports, commands and retained Git worktrees pass after the move, preserving untracked and ignored data.

## Original request

how complex would it be from here to take the final step and also make an organs folder for PyAutoScientist and others?

Approval: ok go

## Approved plan

Phase 1: make infrastructure discovery work with flat and organs/ layouts; merge and validate. Phase 2: move the eight organs and PyAutoScientist with the existing journal, repair links, and repeat imports, worktree and coverage checks. Keep PyAutoArray, the public hub, root marker and activation entrypoint at root. Preserve existing user changes, results and other tasks.

## Detailed implementation

- Brain agents/_repo_paths.py: bootstrap Mind manifest discovery independently of the manifest, support flat and one-family placement, reject ambiguities; package_paths uses the same discovery. Root resolution retains marker-first semantics.
- Brain launchers, resolver loaders, agents, board, worktree and migration helpers: replace root/organ joins with shared lookup; locate Brain itself without circular dependency, preserve flat CI and task bundles.
- Mind scripts/repos_sync.py, session_bootstrap.sh, policy/smoke_bootstrap.py and propagation: locate Brain and Mind after nesting, add organs paths for nine repos, regenerate the twelve deployed smoke shim blocks.
- Heart and Hands root/resolver loaders and organ consumers: support grouped infrastructure, keep standalone/flat fallback; inspect Cortex, Memory, Nerves, Gut and Scientist for consumed fixed sibling paths and fix only actual callers.
- Focused flat/grouped/missing/ambiguous tests, organ suites and independent review. Merge tested source PRs, then refresh canonical repos.
- Fresh inventory; move nine real checkout directories without cleaning, repair retained Git worktrees, symlinks, root activation, local IDE/hook config and installed skill links. Journal must survive moving Mind and preserve rollback.
- Validate manifest 38/38, actual smoke bootstrap 12/12, imports, commands and retained worktrees. Record completion and remove only this task worktrees.

Suggested branch: feature/workspace-organs-regroup
