# Batch phase 2 — the `batch` conductor: plan, slice, collect

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- mind-workflow
- dashboard
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Epic: two-slot-batching
Phase: 2
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30

The reasoning half. **No dispatch in this phase.** With phases 0-2 shipped the
human runs `pyauto-brain batch plan` in their slot, reads the proposal, and taps
the dashboard chips to launch — the same mechanics as today, but against a
backlog that is finally batchable and a plan that respects what review costs.

A thin conductor under `agents/conductors/batch/`, registered in
`bin/pyauto-brain`. The judgement lives in the sizing faculty (phase 0); this
composes and reports.

## `batch plan` — compose the next batch

Reads `queue.md`, the backlog, `epics.md`, `active.md` and the open PR list.
Emits a **BatchDecision**: proposed members, the review budget they consume,
the lane, and what it rejected and why.

The composition rule, and the one that matters:

> **Σ `Review-minutes:` over tier-`glance` and tier-`judge` members ≤ 45.**

Not a task count. Tier-`notify` members cost zero human minutes once phase 4
lands and are capped separately by throughput, not by attention. In practice a
slot holds two or three `judge` tasks, or one `judge` plus several `glance`.
Say this in the decision, plainly, every time — the number is the whole point.

Other constraints, each stated as applied:

- **One member per library repo per shift.** August records name PyAutoFit
  118/332, PyAutoArray 98, PyAutoGalaxy 82, PyAutoLens 78; drawing several
  concurrent members from that distribution makes a same-repo pair the expected
  case. They do not collide at dispatch — separate worktrees — they collide at
  *merge*, because the first `/prm` moves `main` and invalidates the others'
  test and smoke evidence. Workspace, docs and organ repos are exempt.
  Effective parallelism is therefore about the number of distinct hot repos
  touched, two or three, not six. Plan for that rather than around it.
- **Backpressure, as a ramp and never a deadlock.** Count **tasks awaiting
  review**, not PRs (94 of 332 August records name two or more PRs, so a
  PR-count cap trips on a single healthy batch). Above half the cap, halve the
  next batch. At the cap, plan a batch of one, never zero — an academic will
  miss slots and vanish for conference weeks, and the missed slot is the common
  case, not the exception. A system whose response to a busy week is zero
  throughput has inverted its own purpose.
- **One slice per epic per batch.** Epic phases are ordered, so two members of
  one epic could not run in parallel anyway. This is also what delivers "small
  bits of long tasks alongside standalone tasks".
- **Readiness and lane.** Every member is `Unattended: ready`; a cloud shift
  takes no `Lane: laptop` member.

Reuse the auto-bundler wholesale (`_intake.py:807-1008`) for grouping: the
theme-primary pooling key and the Jaccard affinity packing are already right and
already tuned. Replace only its **points** currency with review-minutes —
`BUNDLE_SIZE_POINTS` was a context-window packing heuristic for one session and
was never a measure of anything else. Do not write a second packer.

## `batch slice <prompt>` — the decomposition pass

The pass `AUTONOMY.md` and the sizing faculty have named since inception and
which has never been built. Input: a `needs-slicing` prompt. Output: two to four
children with explicit seams, plus an `epics.md` entry if the parent is not
already an epic. The judgement belongs to the faculty; the conductor writes the
files under `--apply`.

Seam rules, in priority order:

1. **A slice is one unattended run** — it finishes without context compaction.
2. **A slice is independently reviewable, and carries its own witness.** If a
   proposed slice has no witness, it is not a slice, it is a smaller `judge`
   task — say so rather than shipping the illusion.
3. **A slice is independently revertible.**
4. Prefer seams at repo boundaries, and library before workspace, because the
   merge gate already works that way.

Never rename or retire the parent without the human saying so.

## `batch collect` — the packet

Gather each member's outcome: what changed and why in one line, **the witness and
whether it holds**, the diff size, which gate legs actually ran and what they
returned, any flagged decision, and the links. Ordered failures-first.

Assert delivery rather than inferring it: a PR exists, its diff is non-empty, its
checks ran. Green is not done — officially, a cloud session's green status
"means the session started and exited without an infrastructure error. It does
not mean the task in your prompt succeeded." A member that ends green with no PR
is reported **not delivered**, loudly, at the top.

Record the human's *actual* review minutes per member when the slot ends. That
is the only thing that will ever calibrate phase 0's estimate.

## Done when

- `plan | slice | collect` run offline and stdlib-only, like every Brain
  entrypoint.
- `plan` states the review budget it spent and refuses to exceed it.
- Backpressure ramps and is proven never to return an empty batch.
- Tests: the review-minute budget, one-member-per-library-repo, the ramp,
  one-slice-per-epic, lane exclusion, and a slice proposal rejected for having
  no witness.
