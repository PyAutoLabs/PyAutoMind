# Carried members: long-running batch work rolls into the next batch automatically

Type: feature
Target: pyautomind
Repos:
- PyAutoMind
- PyAutoBrain
Themes:
- batch
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Epic: two-slot-batching
Filed: 2026-08-31

Human direction (2026-08-31-pm slot, verbatim):

"""
a common thing we may want to do with a batch is acknowledge that certain runs
(like the laptop run here) are going to take a while and simply do the review on
everything that is ready, with the laptop run basically automatically be picked
up by the next batch without us specifying it (e.g. its in flight and then
deferred to the next).
"""

Formalise the carry-forward adopted mid-slot on 2026-08-31:

1. **Batch record schema** (`batches/AGENTS.md`): a member outcome `CARRIED` —
   dispatched, still in flight at review; not delivered, not failed, needs no
   ruling in this slot's review.
2. **Collect**: a carried member's packet section shows status only (no ruling
   controls) and is excluded from the review progress count; its est.
   review-minutes are listed separately from the slot's reviewable total.
3. **Next batch plan/dispatch**: carried members from the previous batch record
   enter the new batch automatically as members (no re-specification by the
   human, no re-dispatch — they are already running); their review happens in
   the slot where their results land. The queue entry stays until complete/, as
   already documented.
4. Reference behaviour: batch 2026-08-31-pm members subhalo-follow-up-wave and
   jax-inference-phase1-refs.

Witness: the 2026-09 batch record following a batch with a CARRIED member shows
that member present without the human naming it, and `batches/AGENTS.md`
documents the CARRIED outcome.
