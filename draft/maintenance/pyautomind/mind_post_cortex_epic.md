# Mind after the Cortex — shed the science-epic scaffolding, add the PR ledger

Type: maintenance
Target: pyautomind
Repos:
- PyAutoMind
- PyAutoBrain
- PyAutoCortex
- PyAutoHeart
Themes:
- mind-workflow
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-09-03

Umbrella ledger for the `mind-post-cortex` epic (registered in `epics.md`).
This file is never issued; the five phase prompts are, ONE at a time, in order.

## Original request (verbatim, 2026-09-03)

> After implementing Cortex we have removed science projects, which are big
> epics and require their own reviews and systems to manage, from Mind, which
> is now the software ecosystem tool. Do an assessment of whether there is
> functionality or over enginerring aspects of Mind we no longer need, that
> were really required just to manage epic science projects which have now
> been removed. Also assess if given the software heavy, PR focused, nature of
> how we use mind espedcially with batching if we shuld add anything else to
> it and if the Mind batch plan epic can be retired or if it has anyting we
> should still use.
>
> ok lets go, file it and do all 7 of the listed thigns

## The assessment (2026-09-03, three read-only Opus audits)

The Cortex split was clean — nothing in Mind tracks runs or rulings and every
`active.md` row is PR-shaped — but a layer of scaffolding built to price and
schedule science-epic review stayed behind and the software loop never used
it. Only two dev batch slots ever ran (both 2026-08-31); in the only real one
all nine members merged one at a time via `/prm` with no packet ruling. The
review-cost model is near-constant on the backlog (`Consequence: judge` on
152/158 drafts, `Witness:` on 9/167, two calibration records with no actual
minutes). Meanwhile the ledger stops at "issue open": `library-pr:` /
`workspace-pr:` are written by `ship_library` and read by `/prm` but absent
from the `active.md` schema, the dashboard shows no PR link, and the
pending-release gate lives only in a live `gh` search on the Brain board.

## Phases (issue ONE at a time; each is one PR per repo it touches)

1. **Retire the `two-slot-batching` epic** —
   `draft/maintenance/pyautomind/mind_post_cortex_p1_retire_batch_epic.md`.
   Ledger-only (auto-merges). Keeps witness campaign, tier-A shadow and slice
   as standalone prompts; retires dispatcher, budget loop, nightly pass, dev
   carry-forward; reconciles the five stale 2026-08-31-pm `active.md` rows.
2. **Delete the science residue** —
   `draft/maintenance/pyautomind/mind_post_cortex_p2_science_residue.md`.
   `cortex-half:` keys, the `jax-inference-profiling` Mind entry, `Lane:` and
   the `epic-slice`/`theme-sweep` queue kinds, the phantom `experiment/`
   work-type, five RAL-run prompts → Cortex phases, the all-science am batch
   record. Touches REFERENCE.md/ROUTING.md/scripts → human PR.
3. **PR ledger + pending-release view** —
   `draft/feature/pyautomind/mind_post_cortex_p3_pr_ledger_pending_release.md`
   (assessment gaps 1 and 2).
4. **Batch plan fidelity** —
   `draft/feature/pyautobrain/mind_post_cortex_p4_batch_plan_fidelity.md`
   (gaps 3, 4, 5, 7: derive `--awaiting-review`, wire `queue.md` order, merge
   order in the packet, batch-record drift checks).
5. **Heart freeze flag** —
   `draft/feature/pyautoheart/mind_post_cortex_p5_heart_freeze_flag.md`
   (gap 6).

## Explicitly OUT of scope (assessment findings not adopted, or later)

- Collapsing `planned.md`/`parked.md` into a `Status:` value; removing the
  pinned half of `bundles.md`; deleting `lifecycle.py move`/`orphans`,
  `Closes-when:`, the undocumented `Parent:` key; moving the arXiv workflows
  and `spawn.py` out of Mind. File separately if wanted.
- Do NOT add live CI state, open-PR mirrors, mergeability or remote-branch
  existence to Mind — GitHub answers those and any cached copy is stale by
  construction.
- The `research` autonomy cap stays: verdict-shaped research still parks for
  a human (`numba-vs-jax-sparse` is the live example).
