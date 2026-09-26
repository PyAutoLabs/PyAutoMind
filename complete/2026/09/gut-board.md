- issue: https://github.com/PyAutoLabs/PyAutoGut/issues/9 (closed)
- completed: 2026-09-26
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/421, https://github.com/PyAutoLabs/PyAutoGut/pull/10 (MERGED)
- workspace-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/14 (MERGED)
- epic: organ-cockpit (scope widened by the human 2026-09-26: "a clear overview of everything in gut, and ways to click buttons to remove it permenantly")
- heart-ack: "Heart YELLOW (score 85): three pre-existing manifest-drift reasons (hub organism blurb 7, organism-map blocks 1, workspace checkouts 1); live human 'continue' after the reasons were shown, 2026-09-26"
- witness: gut_board.yml run 36258481348 green with `state: ok`; https://pyautolabs.github.io/PyAutoGut/ + state.json live (yellow | 0 due · 43 in transit · 4 held · 8 due on other repos · 1 orphan); cockpit Gut card populated. Human leg pending: Void permanently on `__selftest_branch__` → ref gone, issue closed with SHA.
- decisions: Nerves gets no board (no standing state; cockpit keeps a grey card). The Gut README's "no dashboard by design" is superseded. The void button = a prefilled `void: <name>` issue; Submit is the human `--yes`; void.yml (issues: opened, author_association gate, namespace/held refusals) deletes with the repo token, records the pre-delete SHA, closes the issue, re-dispatches the board. Undated entries are never bulk-voided. Ledger retirement stays a session act (the workflow cannot edit the Mind).
- gotchas: the overdue material is NOT in the Gut — 0 of its 48 refs are due; 8 overdue refs sit on sibling repos (Mind 3, Brain 2, Heart, Lens, Galaxy) which the Gut token cannot delete → "held on another repo" bucket, feed yellow; GITHUB_TOKEN cannot CREATE a Pages site even with pages: write + enablement: true ("Resource not accessible by integration") — create it once with a human token (`gh api -X POST repos/O/R/pages -f build_type=workflow`) then re-dispatch; void names come from `archive-ref` via `_hygiene_condemned.ref_name`, never the `##` heading (hygiene `run_sweep` still uses the heading); batch globs (`pyautomind-*`) expand to one row per ref; PyAutoGut has no pytest CI (19 tests ran locally).
- follow-ups (not filed): void.yml with PAT_PYAUTOLABS for sibling-repo refs; hygiene run_sweep → ref_name; PyAutoLens orphan archive/condemned/paper-jax-intro-revision untracked; all-due voids show as dangling not voided-pending.
- summary: Gut board (Pages, shared theme), state.json feed and one-tap "Void permanently" via prefilled issues handled by void.yml; the board reconciles ls-remote refs against condemned.md into due / transit / held / elsewhere / history / orphan / dangling / voided-pending buckets. Brain 114+66 tests, Gut 19.

## Original prompt

# Birth a PyAutoGut board (Pages) so the footer family can carry the Gut

Type: feature
Target: pyautogut
Repos:
- PyAutoGut
Difficulty: medium
Autonomy: safe
Priority: low
Status: formalised
Consequence: notify
Witness: Either a PyAutoGut board renders with the shared theme (a `gut` entry in `ORGANS` and `MARKS`, `gut: PyAutoGut` in `config/policy.yaml` `board: boards:`, a Pages publish workflow, rows for transit contents, next sweep, recoverable refs and last releases) or the decision not to build it is recorded; the Nerves-board decision is recorded either way.
Review-minutes: 0
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/PyAutoGut/issues/9
Epic: organ-cockpit
Filed: 2026-09-04

The one-tap board family (`PyAutoBrain/config/policy.yaml`, `board: boards:`)
currently names seven boards: brain, mind, cortex, memory, heart, hands,
organism. Two organs in the ruled order have no board at all — **Nerves** and
**Gut** — so the cross-board footer cannot carry them and neither has a palette
entry in `PyAutoBrain/board/_theme.py` `ORGANS`.

The Gut is the one with obvious board-shaped content: condemned self-material
held as durable git refs through a transit window, what is in transit, what is
due to be voided on the next sweep, and what a sweep just released. That is a
list of rows with a 📋 copy-for-Claude payload each — exactly the one-tap board
shape.

Work:

- Decide whether the Gut board is warranted now, and what its rows are (transit
  window contents, next sweep, recoverable refs, last sweep's releases).
- If yes: render it with the shared theme (`PyAutoBrain/board/_theme.py`) the way
  the Heart/Hands/Memory boards do, add a `gut` palette entry to `ORGANS` and a
  mark to `MARKS`, add `gut: PyAutoGut` to `config/policy.yaml` `board: boards:`,
  and wire a Pages publish workflow.
- Decide separately whether **Nerves** gets a board. Nerves is a configuration
  and serialization layer with little standing state; it may be right that it
  never grows one. Record the decision either way so this question is not
  re-asked.

Filed from the board-family footer work (2026-09-04), which made the footer read
the canonical list — the family is now only as complete as `boards:` is.
