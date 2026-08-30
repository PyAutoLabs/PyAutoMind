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
- shift: night
- lane: any
- review-minutes-planned: 42
- usage-window-at-dispatch: <5h %, weekly %, opus %>
- heart-ack:                  # the reason set acknowledged FOR THIS SHIFT
  - <reason line>
- members:
  - <slug>: <prompt path> — <tier> — <review-minutes> — <outcome>
- collected: 2026-09-04T08:30Z
- usage-window-at-collect: <5h %, weekly %, opus %>
- delivered: <n>/<n>
- review-minutes-actual: <n>
- notes: |
    What actually happened. Anything that stalled, and why.
```

## The three fields that are easy to get wrong

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
