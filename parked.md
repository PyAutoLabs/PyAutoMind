# Parked tasks

Tasks that were started or scoped but are not currently in flight. Listed
here so they remain visible across machines instead of disappearing into
unindexed worktrees or stashes. Move an entry back to `active.md` (or to
`planned.md` if re-scoping is needed) when work resumes; move to
`complete.md` once shipped.

## pyauto-update-digest
- parked: 2026-05-17 (worktree last touched)
- classification: workflow (PyAutoMind)
- location: orphan worktree at ~/Code/PyAutoLabs-wt/pyauto-update-digest/
- branch: feature/pyauto-update-digest (clean, no changes)
- notes: |
    Orphan worktree containing only a clean PyAutoMind checkout on the
    branch. No staged or unstaged changes. Action: `worktree_remove
    pyauto-update-digest`.

## strip-non-jit-noise-add-alma-high-res
- parked: 2026-05-18 (worktree last touched)
- classification: developer-tooling (autolens_profiling + autolens_workspace_developer)
- location: orphan worktree at ~/Code/PyAutoLabs-wt/strip-non-jit-noise-add-alma-high-res/
- branch: feature/strip-non-jit-noise-add-alma-high-res (merged to origin/main, upstream gone)
- notes: |
    Orphan worktree found during 2026-05-28 repo hygiene. Holds modifications
    to 9 likelihood scripts in autolens_profiling and 1 file in
    autolens_workspace_developer plus untracked alma_high_res datasets.
    The branch was merged (origin/main is ahead by 19) but this worktree
    kept evolving after the merge.
    Action: review the diffs; if the post-merge edits are wanted, commit on
    a new branch; otherwise `worktree_remove strip-non-jit-noise-add-alma-high-res`.
