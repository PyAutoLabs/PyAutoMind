# Batch plan fidelity: derive backpressure, honour `queue.md`, emit merge order, check batch records

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: normal
Status: draft
Consequence: judge
Witness: `pyauto-brain batch plan --dry-run` with a fixture `active.md` holding three `awaiting-merge` rows reports `awaiting_review=3` without the flag and shrinks the proposal accordingly; a fixture `queue.md` order is reflected in `priority_rank` (top entry first among equals); `batch collect` on the 2026-08-31-pm fixture emits a `merge-order:` list that places library PRs before their workspace dependants and serialises same-repo members; `lifecycle.py check` flags a batch record member whose prompt path does not exist and a closed record with no `review-minutes-actual:`; all Brain and Mind tests pass
Review-minutes: 20
Unattended: ready
Epic: mind-post-cortex
Phase: 4
Filed: 2026-09-03

Phase 4 of `mind-post-cortex` — assessment gaps 3, 4, 5 and 7. Two PRs: Brain
(`agents/conductors/batch/_batch.py` + tests) and Mind (`lifecycle.py` + docs).

1. **Derive `--awaiting-review` (gap 4, S).** `_batch.py` ~L2978: the flag
   defaults to 0 and is never derived, so every plan assumes an empty review
   queue. Count `active.md` rows whose `status:` contains `awaiting-merge` /
   `PR open` (after phase 3, rows carrying a `*-pr:` key) and use that as the
   default; the flag overrides. Print the derived count in the plan header.
2. **Make `queue.md`'s contract true (gap 5, S).** `queue.md` L10-12 says the
   planner reads it and the open-PR state; `plan()` (~L160-260) reads neither.
   Wire queue order into `priority_rank` (a queued prompt outranks an
   unqueued one; among queued, file order wins) and correct the doc to say
   exactly what is read. Open-PR state = the derived count from item 1; say
   so.
3. **Dev batch outcome accounting (gap 3, M — the part not covered by
   carry-forward).** Extend the batch record schema (`batches/AGENTS.md`)
   with a per-member `outcome:` of `merged | rejected-at-review | carried |
   unreviewed` and make `batch collect` fill it from the ledger (a
   `complete/` record → merged; still in `active.md` → carried; review file
   ruling → rejected) rather than leaving `decision: UNREVIEWED`. The next
   `plan` reads the previous record's `carried` members first.
4. **Merge order in the packet (gap 7, M).** `collect` declines today
   (~L1261-1264: "members is sorted by HEALTH, so it cannot drive a merge
   order"). Add a `merge-order:` block computed from `dispatch_order` +
   library-first (`LIBRARY_REPOS`) + shared-repo serialisation, rendered in
   the packet's summary and the record. It is advice for the human's `/prm`
   sequence, not an action.
5. **Batch-record drift checks (gap 7, S).** `lifecycle.py check`: every
   `batches/*.md` member `prompt:` path must resolve (the pm record cites one
   that never existed, L37); a record with `closed:`/review present but no
   `review-minutes-actual:` warns ("the only calibration there is",
   `batches/AGENTS.md` L66). Fix the pm record's bad path as part of this.

Tests: extend `PyAutoBrain/tests` batch fixtures (mind the `_batch` substring
trap in `_cortex.py` noted in memory) and Mind `tests/test_lifecycle*.py`.
