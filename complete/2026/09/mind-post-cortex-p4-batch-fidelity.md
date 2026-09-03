- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/345 (closed, completed 2026-09-03)
- completed: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/346 (merged `d442df5d`)
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/394 (merged `c00098e1`)
- epic: mind-post-cortex (phase 4 of 5; ledger draft/maintenance/pyautomind/mind_post_cortex_epic.md)
- shipped: the batch planner now reads the two inputs it always claimed to read, and the
  batch record now says what became of its members and in what order to merge them.
  Assessment gaps 3, 4, 5 and 7.
  - **Backpressure is derived, not assumed** (`_batch.py`). `--awaiting-review` defaulted to
    `0` and was never derived, so every shift was planned as if the human's review queue were
    empty. `derive_awaiting_review()` counts `active.md` rows carrying a `library-pr:` /
    `workspace-pr:` key — phase 3's schema, the primary signal — or whose `status:` reads
    `awaiting-merge` / `PR open`, the fallback for rows written before phase 3. The flag still
    overrides (it defaults to `None`, so an explicit `--awaiting-review 0` is still an
    override, not an absence), and the plan header prints which source was used.
  - **`queue.md`'s contract is now true.** The file said the planner reads it; `plan()` read
    neither it nor the open-PR state. `read_queue()` parses the `kind: prompt` entries in file
    order and `queue_rank()` matches on the relative path *then* the basename, so an entry
    written against `draft/…` keeps its place after the prompt moves to `active/`. The pool
    sort became `(queue_rank, review_minutes, priority_rank, path)`: a queued prompt outranks
    an unqueued one, file order wins among queued, and below the queue it is still
    cheapest-first. `queue.md` itself now enumerates the three inputs — this file, the `draft/`
    backlog, the derived review-queue depth — and states that **nothing in `plan` calls
    GitHub**, so a shift stays plannable offline.
  - **Outcomes are accounted from the ledger.** All nine members of the only real dev slot
    (2026-08-31-pm) merged, and every one of them is still recorded `decision: UNREVIEWED` —
    the completion records knew, and nothing read them. `member_outcome()` resolves each
    member to `merged` (a `complete/` record names it) / `rejected-at-review` (a review ruling)
    / `carried` (still in `active.md`) / `unreviewed`, in that order, because a rejected member
    is still in `active.md`. `collect` writes an `- outcomes:` block onto the record, and the
    next `plan` reports the previous slot's `carried` members first — they are already costing
    the human review-minutes in the slot being planned. No `gh` call fills it, and none should:
    the organism's own files are what a record is allowed to claim.
  - **`merge-order:` is the only order the record can give.** `members:` is dispatch order and
    the packet sorts by health, so `collect` used to decline outright. It now emits dispatch
    order with library repos first (the library-first gate) and same-repo members serialised,
    because the first `/prm` moves `main` and stales its siblings' evidence. Nothing is
    filtered out — a member with no PR is listed in place with what it is waiting on — and it
    is never enacted: `/prm` stays the human's, one PR at a time.
  - **`lifecycle.py check` opens the batch records at last** (`batch_member_problems()`,
    `batch_record_warnings()`). A member whose `prompt:` path resolves in no state folder *and*
    has never existed in git history is drift, exit 1: the record is wrong about what it
    dispatched, and the member's question and witness cannot be read. A closed record with no
    `review-minutes-actual:` is a warning, exit 0, and deliberately stays one — it is the only
    calibration the review-minute budget has, and failing CI over it would price a missing
    number like a broken ledger. Member lines that are not the grammar (a hand submission, a
    science wave with a sentence where the path goes) are left alone.
  - **The shallow-clone seam, found in CI.** "Has this path ever existed" is unanswerable at
    depth 1, so the leg degraded every absorbed prompt to drift. It now detects the shallow
    clone and collapses to a single warning; `lifecycle_drift.yml` checks out at
    `fetch-depth: 0` so the check keeps its teeth where it matters. Mind is markdown — a full
    clone is cheap.
  - **The pm record's bad member line is fixed.** `subhalo-follow-up-wave` cited
    `draft/research/subhalo_validation/follow_up_wave_adapt_split_and_rectangular.md` and
    asserted it "never existed"; git history says it did, and had already been routed out of
    `draft/` before the slot. The line now cites the completion record that resolves, and the
    false clause is gone — which is also the first thing the new check would have caught.
- verification: `pytest -q` green in both repos; `python3 scripts/lifecycle.py check` clean on
  Mind `main`. CI on the merge heads: Brain Tests pytest 3.12 + 3.13; Mind Dashboard Refresh,
  Lifecycle Drift and Spawn Drift — every run, every leg.
- follow-ups: none filed. The `outcomes:` / `merge-order:` blocks are written by `collect` from
  the next slot on; the two 2026-08-31 records predate them and are left as they are, with the
  missing `review-minutes-actual:` standing as the warning it is meant to be.

## Original prompt

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
Issued: 2026-09-03

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
