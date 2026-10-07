# Gut Void reaches condemned refs held on sibling repos

PyAutoGut#12 → `dad7367c` (closing PyAutoGut#11), merged 2026-09-27 with `--merge`.
Member of bundle `cockpit-followups` (with nerves-unused-keys, start-dev-heart-gate);
epic organ-cockpit. Fable-planned, Opus-executed; Heart YELLOW acked by the human 2026-09-27.

- issue: https://github.com/PyAutoLabs/PyAutoGut/issues/11
- completed: 2026-09-27
- library-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/12

## What shipped
- `void.yml` authenticates with `PAT_PYAUTOLABS` so the Void button can delete refs held on
  sibling repos; board rows for refs held elsewhere now get the button.
- Per-ref failure reporting instead of one opaque job failure; tests (23 passed), README and
  AGENTS.md updated; `gut_board.yml` re-dispatched after merge.

## Original prompt

# Organ cockpit: Gut void button reaches refs held on sibling repos

Type: feature
Target: PyAutoGut
Repos:
- PyAutoGut
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: the human presses Void permanently on one of the 8 overdue sibling refs → the ref disappears from that repo, the issue closes with the SHA, the board's 'due on other repos' count drops by one.
Review-minutes: 3
Unattended: ready
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/PyAutoGut/issues/11
Filed: 2026-09-26
Epic: organ-cockpit

The Gut board (PyAutoGut#9, shipped 2026-09-26) voids refs with the repo's own token, so it can only delete refs under refs/heads/archive/condemned/ in PyAutoGut itself. The ledger's 8 overdue entries are refs archived onto sibling repos (PyAutoMind 3, PyAutoBrain 2, PyAutoHeart, PyAutoLens, PyAutoGalaxy) — the board lists them under 'held on another repo' with only a void-via-session payload, and they keep the feed yellow. The human wants the button to remove everything.

1. void.yml: when the void-plan resolves a name to a ref held 'on <Repo> origin', delete it there with secrets.PAT_PYAUTOLABS (the token branch_archive.yml already uses for cross-repo pushes): ls-remote the sibling → record the SHA → git push https://x-access-token:PAT@github.com/<owner>/<Repo>.git --delete <ref> → verify. A missing or 403 token reports per ref in the closing comment and leaves that ref in place; the issue closes only if every requested ref was voided or explicitly skipped.
2. scripts/board.py: rows in 'held on another repo' gain the Void permanently button (prefilled issue with the repo named in the body); 'Void all due' covers them; the void-plan JSON carries the repo per name.
3. Tests: void-plan carries the repo; the workflow YAML contains the PAT path and the per-ref failure handling; the board renders the button on elsewhere rows.

Out of scope: editing the Mind ledger from the workflow (still a session act); orphans on sibling repos with no ledger entry.

Witness: the human presses Void permanently on one of the 8 overdue sibling refs → the ref disappears from that repo, the issue closes with the SHA, the board's 'due on other repos' count drops by one.

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from user-intake -->
