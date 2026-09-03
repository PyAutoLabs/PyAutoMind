# Queue

The one file the human maintains by hand, and the only thing they have to think
about between slots: **what I want done next, roughly in order**.

**Order is priority.** There is no `priority:` field here — moving an entry up
*is* the act of prioritising it. Nothing else about an entry needs to be true for
it to sit in this file; the planner decides what is actually startable.

A batch is never composed here. `pyauto-brain batch plan` proposes the next one
against a review-minute budget (`PyAutoBrain/agents/conductors/batch/AGENTS.md`),
and the human approves or edits that proposal in their slot — they do not
hand-pick members.

**What the planner actually reads**, and nothing else:

1. **this file** — the `kind: prompt` entries, in file order;
2. **the `draft/` backlog**, graded through the sizing faculty;
3. **the review-queue depth**, derived from `active.md`: a row naming an open PR
   (`library-pr:` / `workspace-pr:`) or whose `status:` says `awaiting-merge` /
   `PR open`. That is what "the open-PR state" means here — the ledger's own
   count, not a live one. Nothing in `plan` calls GitHub, and a shift stays
   plannable offline.

The order in this file is what the planner does with it: a queued prompt
outranks an unqueued one, and among queued prompts the file's order wins.
Below the queue it sorts cheapest-first, because that part of the list is read
when there is a slot to fill and the question is what fits in it. An entry
written against `draft/…` keeps its place after the prompt moves to `active/`.

An entry leaves the queue when its work reaches `complete/`, **not** when it is
dispatched. A task in flight is still the thing the human wants.

## Schema

```markdown
## <n>. <label>
- kind: prompt | retired
- ref: draft/<work-type>/<target>/<name>.md    # kind: prompt
- note: <one line, optional>
```

Two kinds. **`prompt`** is a named prompt file — the live case, and the only one
`pyauto-brain batch plan` reads. **`retired`** is an entry that has left the
queue (shipped, shelved, or moved to the Cortex) but whose note is worth keeping,
because *what the human wanted and why it stopped being wanted* is the queue's
only history. Retired entries carry the pointer that replaced them
(`shipped-as:` / `shelved-as:` / `moved-to:`) and live in the footer, not the
ordered list.

The two non-prompt kinds — "the named epic's next phase" and "anything ready on
this theme" — were removed on 2026-09-03. Both were written for science epics,
which now live in the Cortex, and no code ever read them (`_batch.py` globs
`draft/**/*.md`). The optional lane field went with them: where the work can run
is a Cortex phase-header key now (`PyAutoCortex/REFERENCE.md`), and every Cortex
phase is `local-dev` by construction.

## 1. Retire parked-at-ship under `--auto`
- kind: prompt
- ref: draft/feature/pyautobrain/batch_no_park_at_ship.md
- note: human 2026-08-31 — "the parked thing is an annoying middle ground which requires human time"; an effective-supervised `--auto` run decides-and-flags at ship sign-off instead of parking, since the run already ends at PR-open. AUTONOMY.md doctrine edit, human-required

## 2. numba solve vs JAX sparse operator
- kind: prompt
- ref: draft/research/autoarray/numba_solve_vs_jax_sparse_operator.md
- note: review intake 2026-08-31 — same linear algebra? GPU-JAX amenable or CPU-sparsity-bound?

## 3. Witness campaign
- kind: prompt
- ref: draft/feature/pyautomind/witness_campaign.md
- note: highest-leverage backlog item (151/153 judge); human-declared witnesses only; fill work

## Retired

Entries that have left the queue. Kept for the record of what was wanted and
what replaced it; `batch plan` ignores them.

### Carried members formalisation
- shelved-as: complete/archive/shelved/batch_carry_forward.md (2026-09-03)
- note: the Cortex half shipped (`_batch.py carried_members`, `carried:`/`carried-from:` on the Cortex batch record); the dev half retired with the two-slot-batching epic

### Subhalo validation follow-up wave
- moved-to: PyAutoCortex phases/subhalo_validation/ (2026-09-01)
- note: review tweak 2026-08-31 — human wants to inspect the _adapt_split_fix result; no subhalo[2]; RectangularBilinear runs. The wave is now four Cortex phases (one per lens); record complete/2026/09/subhalo-followup-moved-to-cortex.md

### Euclid docs + structure tidy (phase 3a addendum)
- ref: euclid-dr1-prep
- shipped-as: euclid#47 → PR#48, complete/2026/09/restore-pipeline-narrative-prose.md (2026-09-01)
- note: review tweak 2026-08-31 was folded into the phase-3 prompt and shipped with it — README structural edits, the scripts/tools/ move and the AGENTS.md shortening all landed in PR #48; the start_here.py contradiction was ruled at plan time (kept as a documented shim over initial_lens_model.fit)

### Batches strip on the dashboard
- shipped-as: PyAutoBrain#341 → complete/2026/09/batch-status-box.md (2026-09-03)
- note: shipped as the batch status box on both dashboards; the prompt was folded into that record (2b5af675) and `ref:` no longer resolves — reconciled 2026-09-03

### batch collect
- shipped-as: PyAutoBrain#332 → PR#333, complete/2026/09/batch-collect.md (2026-09-02)
- note: `pyauto-brain batch collect` shipped; the phase's remaining verb is re-filed as draft/feature/pyautobrain/batch_slice.md

### Euclid Lane: recut
- shipped-as: superseded by cortex-birth phase 5 (2026-09-02)
- note: complete/archive/shelved/batch_science_lane.md is marked superseded; leg A (the `Lane:` recut) has no surface left — every Cortex phase is `Lane: local-dev` by construction
