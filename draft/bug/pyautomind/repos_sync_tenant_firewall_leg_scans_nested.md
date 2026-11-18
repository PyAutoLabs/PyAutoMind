# repos_sync tenant-firewall leg scans nested .worktrees/ folders

Type: bug
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: notify
Witness: with a nested worktree at `PyAutoBrain/.worktrees/<x>`, `repos_sync.py --check` reports no tenant-firewall mismatch (unit test pins it) and a new instance fact in tracked organ code is still caught
Review-minutes: 0
Unattended: ready
Lane: any

Source: /health session 2026-11-18. Human chose "file a bug prompt".

`python3 PyAutoMind/scripts/repos_sync.py --check` (and Heart's manifest_drift
check, which runs it) reported "tenant firewall (organ code) — 40 mismatch(es)"
on 2026-11-18. All 40 were under `PyAutoBrain/.worktrees/clara-readme/` — a
nested git worktree of a merged docs branch (PyAutoBrain#613) — e.g.
`PyAutoBrain/.worktrees/clara-readme/agents/conductors/bug/_bug.py: new instance
fact(s) in unlisted file — 'PyAutoArray'`. The organ's real tracked code was
clean. Removing the worktree cleared it, but any session that parks a worktree
under `<organ>/.worktrees/` (Brain and Mind both carry one routinely) will turn
the firewall leg red again, and the gate can be red on a laptop for reasons
that are not organ code.

Other repos_sync legs already treat working-tree debris as not-the-repo
(`scripts/repos_sync.py` ~line 1509: "`tmp/`, `output/`, `.worktrees/`, a
virtualenv are not the repo's"). The tenant-firewall leg should apply the same
exclusion — ideally by walking only `git ls-files` of the organ, so untracked
and nested-worktree files are never scanned.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2076909a-d18c-4718-a05e-9afa6642996d/scratchpad/intake/firewall.md -->
