# Queue

The one file the human maintains by hand, and the only thing they have to think
about between slots: **what I want done next, roughly in order**.

**Order is priority.** There is no `priority:` field here — moving an entry up
*is* the act of prioritising it. Nothing else about an entry needs to be true for
it to sit in this file; the planner decides what is actually startable.

A batch is never composed here. `pyauto-brain batch plan` reads this file, the
backlog and the open-PR state, and proposes the next batch against a review-minute
budget (`PyAutoBrain/agents/conductors/batch/AGENTS.md`). The human approves or
edits that proposal in their slot — they do not hand-pick members.

An entry leaves the queue when its work reaches `complete/`, **not** when it is
dispatched. A task in flight is still the thing the human wants.

## Schema

```markdown
## <n>. <label>
- kind: prompt | epic-slice | theme-sweep
- ref: draft/<work-type>/<target>/<name>.md    # kind: prompt
- ref: euclid-dr1-prep                          # kind: epic-slice — the next phase
- ref: numba-cpu                                # kind: theme-sweep — any ready prompt on this theme
- lane: any | local-dev                         # optional; default any
- note: <one line, optional>
```

Three kinds, because "line up a big epic and take slices of it" and "do whatever
is ready on this theme" are both things a human wants to say without naming
files:

- **`prompt`** — one named prompt. The literal case.
- **`epic-slice`** — the named epic's *next* phase, whatever that turns out to
  be. At most one slice per epic enters any one batch: phases are ordered, so two
  members of the same epic could not run in parallel anyway, and this is what
  interleaves small pieces of long programmes with standalone work.
- **`theme-sweep`** — any `Unattended: ready` prompt carrying that primary
  `Themes:` keyword (vocabulary: `themes.md`). Useful for "keep chipping at the
  numba path" without deciding which chip.

`lane: local-dev` marks work needing the local dataset and output trees, an SSH
endpoint, or the human at the machine. A cloud session detects its own lane and
will not plan the other one — it reports the count instead, so nothing is
silently dropped. One queue holds both lanes; the planner filters.

## 1. Retire parked-at-ship for batch members
- kind: prompt
- ref: draft/feature/pyautobrain/batch_no_park_at_ship.md
- note: human 2026-08-31 pm review — "send off a batch and don't think about it again"; doctrine edit, do together

## 2. Carried members formalisation
- kind: prompt
- ref: draft/feature/pyautomind/batch_carry_forward.md
- note: human 2026-08-31 pm review — long-running members roll to the next batch automatically; adopted mid-slot, formalise

## 3. Subhalo validation follow-up wave
- kind: retired
- moved-to: PyAutoCortex phases/subhalo_validation/ (2026-09-01)
- lane: local-dev
- note: review tweak 2026-08-31 — human wants to inspect the _adapt_split_fix result; no subhalo[2]; RectangularBilinear runs. The wave is now four Cortex phases (one per lens); record complete/2026/09/subhalo-followup-moved-to-cortex.md

## 4. Euclid docs + structure tidy (phase 3a addendum)
- kind: epic-slice
- ref: euclid-dr1-prep
- note: review tweak 2026-08-31 folded into draft/docs/euclid/restore_pipeline_narrative_prose.md; start_here.py contradiction must be ruled at plan time

## 5. numba solve vs JAX sparse operator
- kind: prompt
- ref: draft/research/autoarray/numba_solve_vs_jax_sparse_operator.md
- note: review intake 2026-08-31 — same linear algebra? GPU-JAX amenable or CPU-sparsity-bound?

## 6. Batches strip on the dashboard
- kind: prompt
- ref: draft/feature/pyautobrain/batch_board.md
- note: human 2026-08-31 — important, do soon; strip above "Start here", not a standalone surface

## 7. Witness campaign
- kind: prompt
- ref: draft/feature/pyautomind/witness_campaign.md
- note: highest-leverage backlog item (151/153 judge); human-declared witnesses only; fill work

## 8. batch collect
- kind: retired
- shipped-as: PyAutoBrain#332 → PR#333, complete/2026/09/batch-collect.md (2026-09-02)
- note: `pyauto-brain batch collect` shipped; the phase's remaining verb is re-filed as draft/feature/pyautobrain/batch_slice.md

## 9. Euclid Lane: recut
- kind: retired
- shipped-as: superseded by cortex-birth phase 5 (2026-09-02)
- note: draft/research/euclid/batch_science_lane.md is marked superseded; leg A (the `Lane:` recut) has no surface left — every Cortex phase is `Lane: local-dev` by construction

