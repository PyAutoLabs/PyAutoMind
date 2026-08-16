# Decide whether the clipper belongs in the search identifier

Type: feature
Target: autofit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: human-required
Priority: high
Status: formalised

Filed 2026-08-16. Follow-up 4 owed by the prior-support `Clipper`
(`complete/2026/08/prior-support-clipper.md`, PyAutoFit#1477).

**`Autonomy: human-required` on purpose.** Either answer has a cost that lands
on someone's stored results, and the trade is a judgement about the project's
data, not a technical detail an agent should settle.

## The fact

The clipper does **not** enter the search identifier. Verified against
PyAutoFit `main` on 2026-08-16:

```
af.MultiStartAdam(name="x")                             -> 2bada4747f74bc46bf812605a762def9
af.MultiStartAdam(name="x", clipper=ClipperNone())      -> 2bada4747f74bc46bf812605a762def9
af.MultiStartAdam(name="x", clipper=ClipperPriorBox())  -> 2bada4747f74bc46bf812605a762def9
```

Two runs differing only in prior-support enforcement — which can change the
answer, and demonstrably does — share one output directory.

## Both answers cost something

**Leave it out (status quo).** Existing on-disk results are never orphaned, and
phase 1 stays back-compatible by construction. But runs that differ in a
result-affecting setting collide, and stacked with the `.completed`
short-circuit a later run silently returns the earlier one's numbers. That is
live right now for the phase-2 campaign, whose arms 1 and 2 differ in *nothing
else* — see
`draft/feature/autofit/clipper_validation_campaign.md`, which works around it
with unique per-arm names.

**Put it in.** Arms separate naturally and the identifier tells the truth about
what produced a result. But **every existing multi-start and BFGS output
directory re-keys**, so stored results are orphaned — they are not deleted, but
nothing finds them any more. That is the same comparability argument
PyAutoFit#1472 made when deferring its own policy change, and it collides with
phase 3, which wants a benchmark re-baseline it can compare against history.

## Options, none pre-selected

1. **Status quo**, with the collision documented wherever it bites. Cheapest;
   leaves a footgun that has already been stepped on once.
2. **Include the clipper in `__identifier_fields__`.** Honest; orphans stored
   results.
3. **Include it only when it is not `ClipperNone`.** Unclipped runs keep their
   existing directories, clipped runs get their own. Back-compatible *and*
   collision-free — but the identifier becomes conditional, which is a new
   concept in that machinery and needs checking against how identifiers are
   consumed (database, aggregator, `.completed` discovery).
4. **Leave the identifier alone and make the collision loud** — refuse to
   short-circuit on `.completed` when the search config differs from the one
   recorded in the completed run's `search.json`. Fixes the general
   cached-result hazard rather than this one instance.

Option 3 is the obvious-looking compromise and option 4 is the one that closes
the whole class; both need someone to confirm the consumers can take it.

## Sequencing

**Best decided before phase 3, not after.** Phase 3 flips the default to
`ClipperPriorBox` and carries a re-baseline; if the identifier changes at the
same time, the re-baseline and the re-keying are entangled and neither can be
read cleanly. Deciding this first — either way — leaves phase 3 with one
variable.

## Whatever is chosen

- State the decision and its reason in the record. A future reader hitting a
  collision needs to know it was chosen, not overlooked.
- If the identifier changes, say plainly in the release notes that stored
  results re-key, and check whether a migration is wanted.
- If it does not change, the phase-2 mitigation (unique `name` per arm) becomes
  permanent advice for anyone comparing clipper settings, and belongs in the
  `Clipper` docstring rather than only in a campaign prompt.

## Out of scope

- Flipping the default (phase 3).
- The `.completed` short-circuit's other manifestations, unless option 4 is
  chosen — in which case they are the point.
