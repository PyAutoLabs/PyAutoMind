# Batch reviews — what the human ruled, verbatim

One markdown file per slot: `<YYYY-MM-DD>-<slot>.md` — the review the human
submitted from the packet page (its "submit" step produces exactly this file,
committed via the page's GitHub button or pasted to the orchestrator), or the
same content dictated in-chat and transcribed. The batch record's `review:`
field points here.

The orchestrator parses this file at close-out (2026-08-31): every merge
(`/prm`), every science ruling written into a project ledger, and every
follow-up queued at the top of `queue.md` traces back to a line here — not to
a memory of a conversation. Follow-ups are enacted in the **next** batch; a
review never executes its own follow-ups.

## Schema

```markdown
# Review 2026-09-04 am
- packet: batches/packets/2026-09-04-am.html
- reviewed-at: 2026-09-04T08:30Z
- review-minutes-actual: 55

## <member slug>
- decision: merge | tweak | reject | defer   # science members (Cortex vocabulary): accept | rerun | drop | leave-to-finish
- note: |
    The human's words, verbatim. For tweak/rerun this line becomes the
    follow-up prompt's seed.
```

Members the human left untouched are listed with `decision: defer` by the
orchestrator, never silently dropped. Like every file in `batches/`, this is
ledger-side: it auto-merges, because a review that cannot land unattended
cannot close a batch unattended.
