# batch-plan-kind-cortex-admits-only-ready

Retired unimplemented at the `cortex-checkin` close-out: the thing it asked to
fix no longer exists.

The prompt asked the batch conductor's `plan --kind cortex` to admit
`awaiting-ruling` and `submitted`/`running` members so a cortex review slot
could be conductor-opened rather than hand-written. Phase 1 of the
`cortex-checkin` epic (PyAutoBrain#348, merged
`fc1cb32f6e226ddd2da24448769f1f77ebed6421`; PyAutoCortex#10, merged
`6cd6220e8e86711919c8261d3230564f22b09036`) deleted the whole review-slot
apparatus for the cortex kind — `plan --kind cortex`, the packets, the partial
reviews, the carried members, the status box and the slot/shift vocabulary —
because the measurement said nobody used it: 0 slots were opened by the
conductor, 0 rulings came from a packet, 0 partial reviews were filed and
`review-minutes-actual` was never filled, while all 22 rulings were reached in
a live session.

Proof, not resemblance: `--kind` is gone from `agents/conductors/batch/_batch.py`
on PyAutoBrain `main`, and `batch --help` now offers only `{plan,collect}` with
no kind at all. There is no `plan --kind cortex` left to give a `--board` form.

What replaces it is phase 2's `/cortex` check-in door (PyAutoBrain#350 /
PyAutoCortex#11) — the human checks in on the runs through one door rather than
working a scheduled review shift through a packet page.

Retired under the `/prm` close-out of the `cortex-checkin` epic on 2026-09-04.
No issue was ever opened for it; it never left `draft/`.

## Original prompt

`draft/feature/pyautobrain/the_batch_conductor_s_plan_kind_cortex.md`

```
# The batch conductor's `plan --kind cortex` admits only `ready` phases…

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready

The batch conductor's `plan --kind cortex` admits only `ready` phases, so a slot
made of legacy-born `awaiting-ruling` members and `submitted`/`running`
carry-forwards (batch 2026-09-02-pm) had to be hand-written. Add a form
(`plan --kind cortex --board` or admit awaiting-ruling + submitted/running
members by default) so such slots are conductor-opened and their packets
conductor-built.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from user-intake -->
```
