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
Below the queue it sorts by `Priority:`, then cheapest review first. An entry
written against `draft/…` keeps its place after the prompt moves to `active/`.

**An empty list stops a shift** (M2.3, PyAutoBrain `AUTONOMY.md` "M2 rulings —
2026-11-12"): with no live entry here an unattended shift takes its brief's
named tasks and dips into no backlog. **Every ref is checked**:
`scripts/lifecycle.py check` fails on a `kind: prompt` ref that resolves to no
`draft/` or `active/` prompt, so an entry whose work has shipped moves to the
footer below.

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

## Retired

Entries that have left the queue. Kept for the record of what was wanted and
what replaced it; `batch plan` ignores them.

### numba solve vs JAX sparse operator
- shipped-as: PyAutoArray#513 → complete/2026/09/numba-vs-jax-sparse.md (2026-09-01)
- note: review intake 2026-08-31 — same linear algebra? GPU-JAX amenable or CPU-sparsity-bound? The research verdict closed the issue on 2026-09-01 and the prompt was absorbed into its record; the live entry kept a dangling `draft/` ref until the M2.3 check found it and it was retired 2026-11-12

### Witness campaign
- shipped-as: PyAutoMind#398 → complete/2026/09/witness-campaign.md (2026-09-17)
- note: highest-leverage backlog item (151/153 judge); human-declared witnesses only; fill work. Seven ledger passes gave 137 backlog prompts a human-declared `Witness:`; the queue entry kept a dangling `draft/` ref until retired by the human on 2026-11-07

### Retire parked-at-ship under `--auto`
- shipped-as: PyAutoBrain#365 → complete/2026/09/batch-no-park-at-ship.md (2026-09-07)
- note: human 2026-08-31 — "the parked thing is an annoying middle ground which requires human time"; the AUTONOMY.md doctrine edit shipped: an effective-supervised `--auto` run now decides-and-flags at the ship checkpoint instead of parking, and the batch planner rejects only `human-required`

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
- note: `pyauto-brain batch collect` shipped; the phase's remaining verb is re-filed as draft/feature/pyautobrain/batch_slice.md, since shipped (PyAutoBrain#591 → complete/2026/11/batch-slice.md)

### Euclid Lane: recut
- shipped-as: superseded by cortex-birth phase 5 (2026-09-02)
- note: complete/archive/shelved/batch_science_lane.md is marked superseded; leg A (the `Lane:` recut) has no surface left — every Cortex phase is `Lane: local-dev` by construction
