## pyauto-update-digest
- issue: (none — recovered by repo_cleanup sweep)
- completed: 2026-06-07
- workspace-pr:
  - https://github.com/PyAutoLabs/PyAutoPrompt/pull/20
- repos: PyAutoPrompt
- notes: Stranded worktree on `feature/pyauto-update-digest` — the feature body had already squash-merged via #19, leaving 4 follow-up `ci:` commits on a branch that had drifted ~231 commits behind main. A direct merge would have reverted ~13,965 lines across 151 prompt files. Extracted ONLY the forward `.github/workflows/morning_status.yml` delta (~40 lines) onto a fresh branch from main: add `id-token: write`, swap API key → Claude Max OAuth token, drop the temporary secret-probe step + repair the scheduled-run gate, simplify the Write-tool prompt. Verified no secret-probe remained in the committed file. Stale `feature/pyauto-update-digest` deleted local + remote. (Note: `gh pr create` chokes on PyAutoPrompt's SSH remote — used `gh api repos/.../pulls` instead.)
