# Batch records

One file per dispatched batch: `<YYYY-MM-DD>-<am|pm>.md`. Written at dispatch,
appended at collection. This is the ledger of what was sent into one shift and
what came back — the same genre as `complete/`, and the evidence base the budget
and the review-minute estimate are calibrated from.

It auto-merges (`scripts/ledger_merge.py` — `batches/` is a ledger dir), because
an unattended system that cannot record its own history unattended will not
record it.

## Schema

```markdown
# Batch 2026-09-03 pm
- dispatched: 2026-09-03T17:40Z
- review-at: 2026-09-04T08:00Z     # stated by the human AT DISPATCH
- shift: night                     # free-text label the human gives it
- lane: any
- review-minutes-planned: 42
- usage-window-at-dispatch: <5h %, weekly %, opus %>
- heart-ack:                  # the reason set acknowledged FOR THIS SHIFT
  - <reason line>
- members:
  - <slug>: <prompt path> — <tier> — <review-minutes> — <outcome>
- collected: 2026-09-04T08:30Z
- reviewed-at: 2026-09-04T08:30Z   # when they actually sat down
- usage-window-at-collect: <5h %, weekly %, opus %>
- delivered: <n>/<n>
- packet: batches/packets/<YYYY-MM-DD>-<slot>.html
- review: batches/reviews/<YYYY-MM-DD>-<slot>.md
- review-minutes-actual: <n>
- notes: |
    What actually happened. Anything that stalled, and why.
```

## The four fields that are easy to get wrong

**`delivered:` is not "green".** A cloud session's green status means the session
started and exited without an infrastructure error; it does **not** mean the task
succeeded. A member counts as delivered only with a PR that has a non-empty diff
and checks that actually ran. A member that ends green with no PR is reported as
**not delivered**, loudly, at the top of the packet.

**`heart-ack:` is the shift's grant, written verbatim.** `AUTONOMY.md` ("Leg 4
under a batch launch") scopes a YELLOW acknowledgement to one shift and to the
reason set named here. Recording it loosely is how a scoped grant becomes a
standing one, which doctrine voids.

**`review-minutes-actual:` is the only calibration there is.** The planned figure
is a seed from the sizing faculty; this is what the slot really cost. Without it
the estimate never improves, and the whole batch size rests on it.

**`packet:` is the page the human actually reviewed, archived.** One
self-contained HTML file per slot under `batches/packets/` (see that folder's
`AGENTS.md`), written at dispatch with PENDING members and refreshed at
collect. It is the historical record of what the human was shown; a batch
whose packet was never archived cannot be audited against what they ruled on.

**`review:` is what the human said, verbatim.** The markdown their packet-page
submission produced (or the orchestrator transcribed), one file per slot under
`batches/reviews/`. The orchestrator parses it at close-out — merges, rulings,
queued follow-ups all trace back to a line in this file, not to a memory of a
conversation.

**`review-at:` is the shift, and it is the human's to declare.** There is no
schedule: a slot is whenever they come in, so at dispatch they state when they
expect to be back and **the shift is dispatch → `review-at:`**. The batch's
grant expires there (`AUTONOMY.md`, "What a batch launch is"), and a member not
dispatched inside it returns to the queue. `reviewed-at:` is the same number
measured rather than promised — the pair is what the human's own estimates are
calibrated against, exactly as `review-minutes-actual:` calibrates the cost. A
`review-at:` that passes with nobody there dispatches nothing; the grant just
expires.
