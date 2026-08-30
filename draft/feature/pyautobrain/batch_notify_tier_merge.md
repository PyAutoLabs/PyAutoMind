# Batch phase 4 — the tier-A merge tier (a decision, not a build)

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- mind-workflow
Difficulty: medium
Autonomy: human-required
Priority: high
Status: draft
Epic: two-slot-batching
Phase: 4
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30

**This is the only phase in the epic that reduces the human's total attention
rather than re-timing it.** Everything else moves review into two blocks; this
removes some of it. It is therefore also the only phase that changes the
organism's safety model, and it must be put to the human as a decision with
evidence, not implemented because the plan said so.

Do not start this as code. Start it as a written proposal on an issue.

## The problem it answers

August shipped 332 completion records, about eleven a day. There was never a
throughput problem. The scarce resource is the human's judgement, and they are
the PI of every decision in the organism — choosing API philosophy on behalf of
an external reporter, ruling on a statistical gate with six caveats, deciding
whether a number marked "not citable" may be cited.

Batching schedules those decisions into two blocks. It does not make any of them
cheaper. If the batch layer ships without a merge tier, the human ends up doing
*more* AI-development hours than today, at 6am, from a phone.

## The proposal

For tier `notify` work only — docs, notebooks, profiling scripts, organ-repo
tooling, test-only changes, and pure refactors carrying a byte-equality witness —
`/prm` merges without waiting for the human. The human is **notified, not
consulted**, and can revert.

Gate, all legs, no substitutions:

1. tests, including downstream suites where public API moved;
2. smoke;
3. review — CLEAN;
4. Heart, under phase 3's shift semantics;
5. **an independent-model adversarial review that explicitly tries to falsify
   the run's witness** (phase 3, leg 5) — mandatory here, never optional;
6. the witness itself holds, checked mechanically.

Any leg that did not *run* is a park, not a pass.

## What this changes in doctrine

`AUTONOMY.md` today: merge and issue-close are "human, always", at every level,
and "an explicit future flag may extend autonomy to merge; it does not exist and
must not be assumed." This phase is that flag, and it must be written as a dated,
scoped, revertible edit — not as an implied consequence of batching.

Scope it as narrowly as it can usefully be:

- Tier is decided by **rules over repo class and surface** (phase 0), never by
  the agent's own reading of its work.
- Never available where the diff touches a public API, a default value, an error
  contract, or a file named in an external reporter's issue — regardless of tier.
- Never available to a run that flagged a decision (phase 3).
- A weekly digest lists everything merged this way, so "notified" is a fact and
  not a theory.
- A kill switch, in the manner of `NIGHTLY_RELEASES`.

## How to decide it honestly

Run it **shadowed first**. For four weeks, tier-`notify` work still waits for the
human — but the full six-leg gate runs, the verdict is recorded, and the human
records whether they would have merged unchanged. Then compare: how often did the
gate say merge and the human disagree? That number, on this organism's own work,
is the only basis on which to grant or refuse the tier.

The base rates to beat, both from this repo's own ledger: 20% of August records
carry a CORRECTION or a retraction, and the review leg on autonomous ships is
today the branch's own author.

If the shadow window is not clean, the answer is no — and the epic still works,
just with less throughput. Say that up front so the decision is not loaded.

## Done when

- A written proposal exists on an issue, with the shadow-window results in it.
- The human has said yes or no, dated, in `AUTONOMY.md`.
- If yes: the edit names its scope, its kill switch and its revert condition.
