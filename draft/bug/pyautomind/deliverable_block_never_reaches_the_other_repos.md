# The end-at-deliverable block is stale in every repo but the organs, so Heart is YELLOW on every brief

Type: bug
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: human-required
Priority: medium
Status: draft
Consequence: judge
Review-minutes: 10
Unattended: never
Lane: any

## Finding

Three shift briefs in a row carry the same `heart-ack:` line, typed by the human at launch
(`batches/2026-11-19-pm.md`, `batches/2026-11-19-pm2.md`, `batches/2026-11-20-am.md`):

    manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml
    manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml

The 46 are real and are on `origin/main`, not only on the laptop. `policy/end_at_deliverable.md`
gained the shift-cockpit exception (and `Monitor`), and the copies in the other repos' `AGENTS.md`
were never regenerated. A fresh clone of PyAutoMemory read stale on 2026-11-22
(`repos_sync.py --check --only "end-at-deliverable blocks (generated)"`), and one `--write` fixed
it; PyAutoBrain, PyAutoHeart and PyAutoCortex were already current.

Nothing delivers this block. `.github/workflows/session_hook_propagate.yml` pushes the hook
scripts and the where-to-file block to every repo, and its header says on purpose that "the
organism-map, history, remote-session and deliverable blocks stay out of this job and keep their
reviewed regeneration waves". No wave ran after the policy text changed, so every brief since has
launched YELLOW on a reason nobody can clear from an organ-only session.

## Ask

reproduce before fixing: with the full workspace checked out, `python3 PyAutoMind/scripts/repos_sync.py --check --only "end-at-deliverable blocks (generated)"` lists the stale repos (46 on 2026-11-20).

The human decides which of these it is; do not pick for them.

1. **The block rides the bot push** (as the where-to-file block does since PyAutoMind#442): add
   `policy/end_at_deliverable.md` to the workflow's `paths:`, call the same function `--write`
   uses for the deliverable block on the cloned tree, stage `AGENTS.md` as now, and rewrite the
   header paragraph that keeps the block out. One dispatch then clears all 46, and a later edit
   to the policy text can never strand them again.
2. **One hand wave now**, from the laptop: `repos_sync.py --write`, then a commit per repo. The
   block stays out of the workflow, and the next edit to the policy text needs another wave.

The 2 `generated hooks` mismatches are a different leg and were not found from an organ-only
session (5 of 50 repos checked out, all current). Read them on the laptop with
`repos_sync.py --check --only "generated hooks (session-start + end-at-deliverable)"`; the leg
reads other sessions' worktrees too, so a stale worktree is the likely cause.

## Provenance

[from: orchestrator review 2026-11-22 of shifts 2026-11-19-pm, 2026-11-19-pm2 and 2026-11-20-am]
