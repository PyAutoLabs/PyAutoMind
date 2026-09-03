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

1. **Retire the `two-slot-batching` epic** — **SHIPPED 2026-09-03**, record
   `complete/2026/09/mind-post-cortex-p1.md` (issue PyAutoMind#389 closed;
   ledger-only, auto-merged as `49d0b530` from `claude/mind-post-cortex-p1`,
   no PR). Kept witness campaign, tier-A shadow and slice as standalone
   prompts; retired dispatcher, budget loop, nightly pass, dev carry-forward;
   reconciled the five stale 2026-08-31-pm `active.md` rows.
2. **Delete the science residue** — **SHIPPED 2026-09-03**, record
   `complete/2026/09/mind-post-cortex-p2.md` (issue PyAutoMind#390 closed;
   PyAutoCortex#8 `d23a51a8`, PyAutoBrain#343 `338addad`, PyAutoMind#391
   `e705eee7`). Removed the Cortex-half epic keys, the JAX profiling Mind
   entry, the lane header and the two non-prompt queue kinds, the phantom
   prototype work-type; the RAL-run prompts became Cortex phases and the
   all-science am batch record moved to the Cortex.
3. **PR ledger + pending-release view** — **SHIPPED 2026-09-03**, record
   `complete/2026/09/mind-post-cortex-p3-pr-ledger.md` (issue PyAutoMind#392
   closed; PyAutoMind#393 `7d3ed60f`, PyAutoBrain#344 `fcb43755`,
   PyAutoHeart#195 `b91c026a`). Schematised `library-pr:`/`workspace-pr:` as
   repeatable keys plus `pending-release:`/`release-gate:`, made a row that
   declares open PRs and names none a `lifecycle.py check` error, gave the
   dashboard an In-flight PR link per key and a Pending release section, and
   named `/review_release` step 6 as the one step that clears the chain. Fixed
   in passing the `--mind <relative>` bug that had every CI render silently
   dropping the Cortex-gate badges.
4. **Batch plan fidelity** — **SHIPPED 2026-09-03**, record
   `complete/2026/09/mind-post-cortex-p4-batch-fidelity.md` (issue
   PyAutoBrain#345 closed; PyAutoBrain#346 `d442df5d`, PyAutoMind#394
   `c00098e1`). Gaps 3, 4, 5 and 7: `--awaiting-review` is derived from
   `active.md`'s PR keys instead of assuming an empty review queue; `queue.md`
   order now ranks the pool and the file says what `plan` really reads (that
   file, the `draft/` backlog, the derived queue depth — no `gh` call);
   `collect` fills a per-member `outcome:` from the ledger and emits a
   `merge-order:` block as advice for the human's `/prm` sequence; and
   `lifecycle.py check` opens the batch records at last — an unresolvable
   member `prompt:` path is drift, a closed record with no
   `review-minutes-actual:` is a warning. The check degrades in a shallow
   clone, so `lifecycle_drift.yml` now checks out at `fetch-depth: 0`.
5. **Heart freeze flag** — **SHIPPED 2026-09-03**, record
   `complete/2026/09/mind-post-cortex-p5-heart-freeze.md` (issue PyAutoHeart#196
   closed; PyAutoHeart#197 `4b873047`, PyAutoBrain#347 `67971f21`,
   PyAutoHands#275 `128d9a1d`). Gap 6: Heart owns a `freeze.json` flag with a
   `pyauto-heart freeze` verb (`--set/--until/--clear/--show`) that expires by
   `until` rather than by discipline; `validate --ingest`, `review_release` and
   the Hands `pre_build` are the real call sites; Brain reads it on three
   surfaces — `vitals` prints it, `batch collect` and the status box carry it,
   and `/prm` stops on a library-repo PR while it is active (`--thaw "<why>"`
   overrides, logged to `autonomy_log.md`). Heart's `readiness` verdict is
   deliberately unchanged: the freeze is advice-with-teeth for `/prm` only.

**The epic is COMPLETE** — all five phases shipped 2026-09-03.

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

## Retired from epics.md (2026-09-03)

## mind-post-cortex
- title: Mind after the Cortex — shed the science-epic scaffolding, add the PR ledger
- ledger: draft/maintenance/pyautomind/mind_post_cortex_epic.md
- status: COMPLETE — all five phases shipped 2026-09-03 (records complete/2026/09/mind-post-cortex-p1.md, -p2.md, -p3-pr-ledger.md, -p4-batch-fidelity.md, -p5-heart-freeze.md). Phase 1 issue PyAutoMind#389 closed (ledger-only, auto-merged as `49d0b530` from `claude/mind-post-cortex-p1`, no PR); phase 2 issue PyAutoMind#390 closed (PyAutoCortex#8 `d23a51a8` + PyAutoBrain#343 `338addad` + PyAutoMind#391 `e705eee7`); phase 3 issue PyAutoMind#392 closed (PyAutoMind#393 `7d3ed60f` + PyAutoBrain#344 `fcb43755` + PyAutoHeart#195 `b91c026a`); phase 4 issue PyAutoBrain#345 closed (PyAutoBrain#346 `d442df5d` + PyAutoMind#394 `c00098e1`); phase 5 issue PyAutoHeart#196 closed (PyAutoHeart#197 `4b873047` + PyAutoBrain#347 `67971f21` + PyAutoHands#275 `128d9a1d`).
- notes: five phased prompts from the 2026-09-03 assessment — (1) retire the two-slot-batching
  epic keeping witness campaign / tier-A shadow / slice as standalone prompts and reconcile the
  five stale 2026-08-31-pm active.md rows; (2) delete the science residue (the Cortex-half epic
  keys, the JAX profiling entry, the lane header and the two non-prompt queue kinds, the phantom
  prototype work-type, the RAL prompts that became Cortex phases, the am batch record); (3) schematise library-pr/workspace-pr +
  PR column + pending-release view; (4) batch plan fidelity (derived backpressure, queue order,
  merge order, batch-record drift checks); (5) Heart freeze flag. Issue ONE at a time, in order.
