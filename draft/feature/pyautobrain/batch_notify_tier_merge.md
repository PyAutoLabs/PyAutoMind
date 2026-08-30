# Batch phase 4 — the tier-A merge tier: shadow window, then the decision

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

**Decided 2026-08-30: shadow it for four weeks, then decide.** The human chose
the shadow window over granting or refusing the tier outright. This prompt is
now the protocol for that window, and the protocol is pre-registered — the
decision rule is fixed *before* the data arrives, so the answer cannot be
rationalised afterwards.

**Window: 2026-08-30 → 2026-09-27.**

## Why this matters more than any other phase

Everything else in the epic moves review into two blocks. This is the only
mechanism that removes some of it. August shipped 332 completion records, about
eleven a day, with the human in-session; there was never a throughput problem.
The scarce resource is the human's judgement, and batching alone schedules more
of it per hour rather than less.

## What the tier would cover, and how much of the flow that is

Measured over all 332 August records, bucketed by the repos their PRs name:

| Bucket | Share | Tier |
|---|---|---|
| organ repos only (Brain, Mind, Memory, Heart, Hands, Gut, Scientist) | **56 · 17%** | the `notify` candidate pool |
| workspace / assistant / profiling only | 52 · 16% | mostly `glance`, some `notify` |
| touches a core library | 99 · 30% | `glance` or `judge` |
| names no PR at all — research, decisions, verdicts | **125 · 38%** | `judge` by nature |

Two honest readings of that table, and both belong in the decision:

1. **The window will be well powered.** At ~56 candidates a month, four weeks
   yields roughly fifty — enough to decide on, without waiting a quarter.
2. **The ceiling is about 17% of throughput.** Auto-merge is worth the doctrine
   change, but it is not the answer on its own. The single biggest bucket is the
   38% that produce no PR at all: research, decisions and written verdicts,
   whose review *is* the judgement. Nothing in this epic makes those cheaper, and
   the plan should stop implying otherwise. If the human wants that bucket
   cheaper too, it is a separate question about how verdicts are structured, not
   about merge automation.

## The protocol

**Start now, cheaply.** The window is four weeks of wall-clock, so it must not
wait on phases 1-3 or it puts the decision on the critical path twice. Two
stages:

- **Stage 1 (from 2026-08-30, needs only phase 0's tier rules).** At every
  close-out, whatever the workflow, record the row below. The gate column records
  the four-leg gate plus whether the witness held.
- **Stage 2 (once phase 3's adversarial leg exists).** Same rows, with the
  fifth leg's verdict recorded too. Rows are marked `stage: 1|2` so the two are
  never silently pooled.

**Where the rows live:** appended to `PyAutoMind/autonomy_log.md` as its own
table. That file is already an append-only calibration record and already a root
ledger file, so the window needs no new infrastructure and no allowlist edit —
it can start today.

One row per tier-`notify` candidate:

```
| date | task | tier | gate (tests/smoke/review/heart/witness[/adversary]) | human action | stage |
```

`human action` ∈ `merged-unchanged` / `merged-after-substantive-change` /
`not-merged`.

**"Substantive" is defined now, not later**, so the judgement at close-out is
mechanical: a change the human would have minded finding already merged. A
changed default, a user-visible error message, a removed or weakened test, a
renamed public thing, a docs claim that was wrong — substantive. Typos, wording,
formatting, comment polish — not.

## The decision rule, pre-registered

Over a window of **at least 40** tier-`notify` candidates:

- **Grant the tier** if `merged-after-substantive-change` + `not-merged` = **0**.
- **Grant it narrowed** if every such case falls in one identifiable sub-class
  (say, "organ repos with no tests"): exclude that sub-class from the tier by
  rule, and grant the rest. The exclusion is written into the doctrine edit.
- **Refuse** otherwise, and say so plainly. The epic still works — with less
  throughput and a longer review queue — so the decision is not loaded.

Fewer than 40 candidates at the end of the window is not a pass. Extend the
window; do not lower the bar.

The base rates this is being judged against, both from this organism's own
ledger: **20% of August records carry a correction or a retraction**, and the
review leg on autonomous ships is today, in practice, the branch's own author.

## If the answer is yes

The doctrine edit in `AUTONOMY.md` must be dated, scoped and revertible.
`AUTONOMY.md` today says merge and issue-close are "human, always" at every
level, and that "an explicit future flag may extend autonomy to merge; it does
not exist and must not be assumed." This is that flag. Write it as such.

Scope, as narrow as it can usefully be:

- Tier decided by **rules over repo class and surface** (phase 0), never by the
  agent's own reading of its work.
- Never where the diff touches a public API, a default, an error contract, or a
  file named in an external reporter's issue — regardless of tier.
- Never for a run that flagged a decision (phase 3).
- The full six-leg gate, with any leg that did not *run* counting as a park.
- A weekly digest of everything merged this way, so "notified" is a fact rather
  than a theory.
- A kill switch, in the manner of `NIGHTLY_RELEASES`.
- A standing revert condition: one substantive escape retires the tier pending
  a fresh window.

## Done when

- The shadow table exists in `autonomy_log.md` and is being appended to.
- At window close, the counts are reported against the pre-registered rule
  before any recommendation is written.
- The human's yes, narrowed-yes or no is recorded in `AUTONOMY.md`, dated.
