## ag-workspace-test-gitignore-fix
- issue: none — direct cleanup follow-up to ag-interferometer-jax-viz (#43)
- completed: 2026-05-14
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/45
- repos: autogalaxy_workspace_test
- notes: |
    Two-commit cleanup PR. Commit 1: git rm 6 binary artifacts that #44
    leaked. Commit 2: upgrade .gitignore from per-type entries to
    autolens_workspace_test-style **/images/ glob.

    Caught between merge of #44 and the active.md update — inspected
    PR #44's file list via `gh pr view 44 --json files`, found 6 unwanted
    PNGs/FITS, filed the cleanup PR within minutes of the original
    merge. Both PRs now in main; binaries never lived on main for long.

    The two commits could have been one if the .gitignore Edit had been
    staged before `git rm` (the Edit modification was unstaged when I
    ran `git commit`, so only the deletes landed in the first commit).
    Filed a separate commit on top rather than amending per the
    no-amend convention.
