## prm-shadow-row-notify-tier
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/364
- completed: 2026-09-07
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/395 (merge eec96d41)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/366 (merge af8f2ef5)
- summary: |
    The tier-`notify` auto-merge decision's shadow window is fed again, by the act that happens on every
    shipped task: `/prm` close-out. `PyAutoMind/scripts/lifecycle.py shadow-row` appends one six-cell row
    under `## Shadow window` in `autonomy_log.md` and rewrites the section's `Count toward 40:` line
    (dry-run by default, `--apply` writes, exit 2 on a missing heading/table, `|` in a cell traded for `/`).
    `/prm` sub-step 5.3b (PyAutoBrain `skills/prm/prm.md`) runs for tier-`notify` candidates only: the gate
    cell is copied from the task's ship calibration row, `stage` is 2 if an independent-model adversary leg
    ran else 1, the human answers one question (merged unchanged, or after a substantive change), and the
    row rides the same Mind commit and push the close-out already makes. `reference.md` documents the cell
    sources. The doctrine edit in `AUTONOMY.md` ("an explicit future flag may extend autonomy to merge") is
    NOT written here — it is written when the window reaches 40 and the human rules.
- ledger: |
    `autonomy_log.md` shadow-window header restated as a counted window (to 40, re-opened 2026-09-03 from
    the first `/prm`-appended row), with the history sentence corrected (the two-slot batching epic was
    retired; the batch slot door lives on and runs only when a batch is launched). The mis-filed
    2026-09-07 `corrective` row (jax-grad-delaunay-fd-sweep-repin) moved to the main calibration table.
    Count line at ship: `Count toward 40: 1 (stage 1: 0, stage 2: 1) — window re-opened 2026-09-03; first
    /prm-appended row: none yet; legacy rows not counted: 1`.
- tests: |
    `PyAutoMind/tests/test_autonomy_log_shadow.py` (14 tests: heading, six-column schema, allowed
    `human action` values on rows at/after the /prm epoch, count line agrees with rows, dry-run vs
    `--apply` on a fixture, invalid action exits non-zero). `PyAutoBrain/tests/test_board.py`: a six-column
    shadow row renders through `collect_autonomy` (regex unchanged; tier lands in the level chip, action in
    the outcome chip). Mind 412 passed; Brain 917 passed plus the known worktree-only Cortex fixture failure.
- traps: |
    The PR's `drift` check is tree-wide: it failed on other live sessions' unclaimed active/ prompts
    (rows whose slug differs from the filename and carry no `- prompt:` line) and on this task's own prompt
    because the branch predated its registration commit (git-add-after-git-mv dropped active.md; recovered
    in 1e73d82b). Fixed by merging origin/main into the branch and claiming the last orphan on its row
    (`- prompt: active/cortex_projects_route_through_assistant.md`, human-authorised).
- follow-ups: |
    First real shadow row lands at the next `/prm` of a tier-`notify` task. Sibling task
    batch-no-park-at-ship (PyAutoBrain#365) shipped in the same session.

## Original prompt

# The tier-`notify` auto-merge decision — re-open the shadow window, then decide

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
Consequence: judge
Review-minutes: 20
Unattended: never
Filed: 2026-08-30
Issued: 2026-09-07

**Decided 2026-08-30: shadow the tier before granting or refusing it.** The
question is whether an agent may ever *merge* its own low-consequence work —
`AUTONOMY.md` says merge and issue-close are "human, always" at every level, and
that "an explicit future flag may extend autonomy to merge; it does not exist
and must not be assumed". This prompt is the protocol for deciding whether to
write that flag, and the protocol is pre-registered: the decision rule is fixed
*before* the data arrives, so the answer cannot be rationalised afterwards.

**The window is re-opening, not closing.** Measured 2026-09-03: the shadow table
in `autonomy_log.md` holds **2 rows**, against the **40** its own pre-registered
rule requires, and **nothing has fed it since 2026-08-31** — the rows were being
appended by a batch review slot, and the batch workflow was retired on
2026-09-03 (`complete/archive/epics/two_slot_batching_epic.md`). Two rows is not
a weak answer, it is no answer. The rule's own instruction covers exactly this
case — *"Fewer than 40 candidates at the end of the window is not a pass. Extend
the window; do not lower the bar."* — so the nominal close of 2026-09-27 is
void, and the window re-opens from the first row appended under the new
mechanism below.

## Why this is worth measuring at all

Every other workflow change re-times the human's review — schedules it, batches
it, moves it later. This is the only mechanism that *removes* some of it. August
shipped 332 completion records, about eleven a day, with the human in-session;
there was never a throughput problem. The scarce resource is the human's
judgement, and re-timing it does not create more of it.

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
   whose review *is* the judgement. Nothing here makes those cheaper, and no
   claim should imply otherwise. If the human wants that bucket cheaper too, it
   is a separate question about how verdicts are structured, not about merge
   automation.

## The protocol

**The row must be appended by the act that actually happens.** The first attempt
anchored the append to a batch review slot; two slots ever ran, so two rows
exist. The act that happens on every shipped task, every time, on every surface,
is **`/prm` close-out** — it already judges the PR's checks, merges, closes the
issue, moves the prompt to `complete/` and regenerates the dashboard. Appending
one row there is the deliverable of this prompt:

- **`/prm` appends the shadow row** for every tier-`notify` candidate it merges,
  reading the gate legs it has already evaluated and the human action it has
  just taken. No new surface, no separate discipline to remember, and the row
  cannot be forgotten by a session that never came back.
- **The window re-opens from the first row appended that way** and runs until
  40 candidates have accumulated. Report the counts against the rule at that
  point — not on a calendar date.

Two stages, unchanged and never pooled:

- **Stage 1** — the four-leg gate plus whether the witness held.
- **Stage 2** — the same rows with the independent-model adversarial leg's
  verdict recorded too. Rows are marked `stage: 1|2`.

**Where the rows live:** appended to `PyAutoMind/autonomy_log.md` as its own
table, as they are today. That file is already an append-only calibration record
and already a root ledger file, so the window needs no new infrastructure and no
allowlist edit.

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

Over a window of **at least 40** tier-`notify` candidates (2 as of 2026-09-03 —
the count restarts from the first `/prm`-appended row):

- **Grant the tier** if `merged-after-substantive-change` + `not-merged` = **0**.
- **Grant it narrowed** if every such case falls in one identifiable sub-class
  (say, "organ repos with no tests"): exclude that sub-class from the tier by
  rule, and grant the rest. The exclusion is written into the doctrine edit.
- **Refuse** otherwise, and say so plainly. Nothing else depends on the answer —
  the workflow is unchanged either way — so the decision is not loaded.

Fewer than 40 candidates is not a pass. Extend the window; do not lower the bar.
This rule has already fired once, on 2026-09-03, and is why the window is being
re-opened rather than closed.

The base rates this is being judged against, both from this organism's own
ledger: **20% of August records carry a correction or a retraction**, and the
review leg on autonomous ships is today, in practice, the branch's own author.

## If the answer is yes

The doctrine edit in `AUTONOMY.md` must be dated, scoped and revertible.
`AUTONOMY.md` today says merge and issue-close are "human, always" at every
level, and that "an explicit future flag may extend autonomy to merge; it does
not exist and must not be assumed." This is that flag. Write it as such.

Scope, as narrow as it can usefully be:

- Tier decided by **rules over repo class and surface** (the sizing faculty),
  never by the agent's own reading of its work.
- Never where the diff touches a public API, a default, an error contract, or a
  file named in an external reporter's issue — regardless of tier.
- Never for a run that flagged a decision.
- The full six-leg gate, with any leg that did not *run* counting as a park.
- A weekly digest of everything merged this way, so "notified" is a fact rather
  than a theory.
- A kill switch, in the manner of `NIGHTLY_RELEASES`.
- A standing revert condition: one substantive escape retires the tier pending
  a fresh window.

## Done when

- `/prm`'s close-out appends the shadow row for every tier-`notify` candidate it
  merges, and the row lands without the human doing anything extra.
- The shadow table in `autonomy_log.md` is growing again, its header states the
  re-opened window, and the count toward 40 is readable from the table itself.
- At 40 candidates the counts are reported against the pre-registered rule
  before any recommendation is written.
- The human's yes, narrowed-yes or no is recorded in `AUTONOMY.md`, dated.
