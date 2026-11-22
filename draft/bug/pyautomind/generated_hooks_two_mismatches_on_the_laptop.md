# Heart reports 2 generated-hook mismatches on the laptop that no organ-only session can see

Type: bug
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Review-minutes: 5
Unattended: never
Lane: local-dev

## Finding

Shift briefs 2026-11-19-pm, 2026-11-19-pm2 and 2026-11-20-am were each acknowledged YELLOW on two
reasons. The first, 46 stale end-at-deliverable blocks, is fixed at its cause: the block now rides
`session_hook_propagate.yml` (2026-11-22). The second is still open:

    manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml

A cloud session with the five organs checked out reads that leg OK (5 of 50 repos), and the
propagation workflow already pushes the hooks to every repo, so the two are most likely on the
laptop only: a checkout behind its origin, or another session's worktree (the leg reads those
too).

## Ask

reproduce before fixing: on the laptop, `python3 PyAutoMind/scripts/repos_sync.py --check --only "generated hooks (session-start + end-at-deliverable)"` names the two.

1. Name the two and say which case each is.
2. A checkout behind origin: pull it. A stale worktree of a finished task: remove it through the
   usual close-out. Anything else (a repo the workflow cannot push to, a hook edited by hand) is
   a finding for the human, not a fix to guess at.
3. First check that the first propagation run after 2026-11-22 cleared the 46 deliverable
   blocks: the same command with `--only "end-at-deliverable blocks (generated)"` reads OK.

## Provenance

[from: orchestrator review 2026-11-22 of shifts 2026-11-19-pm, 2026-11-19-pm2 and 2026-11-20-am]
