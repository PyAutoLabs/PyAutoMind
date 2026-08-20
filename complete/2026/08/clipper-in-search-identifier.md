# clipper-in-search-identifier (decided: option 2 — the clipper enters the MLE identifiers)

- library-prs: https://github.com/PyAutoLabs/PyAutoFit/pull/1494
- merge-commits: PyAutoFit `f3767a79743e6976accd8fd6957afc5f366654fb` (2026-08-18)
- issue: PyAutoFit#1493 (closed by #1494)
- summary: The prior-support `Clipper` did not enter the search identifier, so
  two runs differing only in a result-affecting setting shared one output
  directory and — stacked with the `.completed` short-circuit — a later run
  could silently return the earlier one's numbers. **Decided option 2:**
  `__identifier_fields__ = ("clipper",)` on `AbstractMultiStartGradient` and
  `AbstractBFGS`, accepting that every existing multi-start and (L)BFGS output
  directory re-keys. Nested samplers, MCMC searches and `Drawer` are deliberately
  untouched and pinned byte-identical.
- validation: 104 lines of new identifier tests (5 new cases) — hash-lists pinned
  for `Nautilus`/`DynestyDynamic`/`Emcee`/`Zeus`/`Drawer`, a fork test over
  `MultiStartAdam` and `LBFGS`, and a tripwire asserting the nested samplers
  never grow a `clipper` attribute.
- release: shipped in PyAutoFit **2026.8.20.1** (2026-08-20).

## The decision, and why — this was chosen, not overlooked

The prompt put four options up with none pre-selected and marked itself
`Autonomy: human-required`, because either answer costs someone's stored
results. The human chose **option 2: put it in, unconditionally, scoped to the
searches that consume it.**

Why not the others:

- **Option 1 (status quo)** leaves a footgun that had already been stepped on
  once — the phase-2 validation campaign's arms 1 and 2 differ in *nothing else*
  and collided, and were only saved by per-arm unique names.
- **Option 3 (include only when not `ClipperNone`)** buys back-compatibility
  with a *conditional* identifier — a new concept in that machinery, and one
  every consumer (database, aggregator, `.completed` discovery) would have to be
  re-checked against. Rejected as a novel special case guarding a one-off.
- **Option 4 (make the `.completed` short-circuit loud instead)** closes the
  wider class of cached-result hazards and remains worth doing, but it does not
  make the identifier tell the truth about what produced a result. It was not
  taken here and is **not** carried forward by this record — file it fresh if
  wanted.

The cost was paid with eyes open: **stored multi-start and (L)BFGS results are
orphaned, not deleted.** Nothing finds them by identifier any more. The
re-key hits *every* such directory, including runs that never passed a clipper,
because the pre-change hash list for these searches was the class name alone
(`AbstractSearch.__identifier_fields__` is the empty tuple, and
`Identifier._add_value_to_hash_list` then contributes no fields) — adding one
field changes the hash for the default construction too.

## The scoping constraint is the load-bearing part

The clipper is resolved on `AbstractMLE`, and the fix declares the field on the
two MLE subclasses that *consume* it — not on `NonLinearSearch`. Hoisting it
would put the clipper within reach of the nested samplers' identifier machinery
and silently re-key the entire nested-sampling archive, which is a far larger
body of stored results and one where the setting cannot affect the answer at
all. `test_nested_samplers_have_no_clipper` exists to fail loudly if anyone
tries.

`Drawer` is the same rule in miniature: it inherits the attribute from
`AbstractMLE` but never consumes it, so it deliberately does **not** declare the
field. **A setting that cannot change the result must not re-key stored
results** — that is the general principle this task settled, and it is worth
more than the specific answer.

## Sequencing paid off

The prompt argued this had to be decided **before** phase 3 (flipping the
default to `ClipperPriorBox`), so the re-baseline and the re-keying would not be
entangled. That held: the identifier change landed 2026-08-18 on its own, and
phase 3 now has one variable rather than two.

## Residuals — what this record does NOT claim is done

1. **The release notes do not say plainly that stored results re-key.**
   PyAutoFit 2026.8.20.1's notes carry the commit subject
   (`feat: clipper enters the MLE search identifiers (#1494)`) and nothing more.
   The prompt asked explicitly for a plain statement that existing multi-start
   and (L)BFGS output directories are orphaned. Amend that release's notes, or
   carry the sentence into the next release's.
2. **"Check whether a migration is wanted" was never answered.** No migration
   ships, and no decision that one is unwanted is on record. Users with stored
   multi-start/(L)BFGS results have no path to re-key them.
3. **The phase-2 campaign record's ARM-COLLISION TRAP section is now stale.**
   `complete/2026/08/clipper-validation-campaign.md` states as fact that the
   clipper does not enter the identifier, with three empirically-verified hashes.
   True on 2026-08-16, false since 2026-08-18. A pointer note was added there in
   this same change; the historical measurement is left intact.
4. **Option 4 remains open** as the general fix for the `.completed`
   short-circuit returning cached results when the search config differs.

## Mind-side drift this closed

The work shipped in PyAutoFit on 2026-08-18 while the prompt sat in
`draft/feature/autofit/clipper_in_search_identifier.md` — never issued into
`active/`, never registered, and never recorded. Four other records and drafts
still pointed at that draft path as an *open* question. This record is the
retrospective close; the code has been on `main` since #1494 merged.

The transferable lesson: a task that ships straight from a decision — no issue,
no branch registration — leaves no trace in the Mind unless the record is
written by hand afterwards. `lifecycle.py check` does not catch it, because it
only guards `active.md` against `complete/`; a prompt that never entered
`active/` is invisible to the drift guard.

## Original prompt

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
