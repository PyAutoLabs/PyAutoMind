# Batch phase 0 — the review-cost model

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
Phase: 0
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30

Nothing downstream in this epic is sound while the system cannot say what a task
will **cost the human to review**. This phase adds that judgement and re-grades
the backlog. It writes no dispatcher and no queue.

Four judgements, all in the sizing faculty (`agents/faculties/sizing/`), all
surfaced on the `SizingSurface` and written by intake as prompt headers.
`ORGANISM.md` puts them here rather than in a conductor: they are opinions, and
a conductor never consults another conductor.

## 1. `Consequence:` — the tier

Decided by **rules over repo class and surface**, never by an agent's assessment
of its own work:

```
Consequence: notify | glance | judge
```

- **notify** — docs, notebooks, profiling scripts, organ-repo tooling, test-only
  changes, and pure refactors carrying a byte-equality witness.
- **glance** — library-internal change with a machine-checkable witness;
  workspace scripts.
- **judge** — public API, default values, error contracts, science policy,
  anything answering an external reporter, and **anything with no witness**.

That last clause is the one that makes the rest work. Derive the repo class from
`PyAutoMind/repos.yaml`, which already carries category for every repo; do not
hand-maintain a second list.

## 2. `Witness:` — what makes it reviewable

A free-text line naming the machine-checkable claim that will make this task
reviewable in minutes rather than by reading the diff. The evidence that this is
the real lever is in the ledger: the completions that *are* fast to review are
the ones carrying witnesses — "ids bit-identical, 62→9.7 ms", "31-rule
byte-equality", control-tested spy sentinels, "0.068″ parity vs the published
model". The ones that are slow carry prose.

The point is that the witness is chosen **at conception**, so the work is scoped
to be provable. A prompt with no plausible witness is not a badly-written
prompt — it is tier `judge`, and should say so.

## 3. `Review-minutes:` — the honest estimate

An integer. Calibrate against real records rather than inventing a scale:
`cmap-magma-default` (filed small-medium, safe) is 15-25; an
`autoarray-adapt-images-precondition`-shaped API fork is 15-20; a
`harvest-0827-gate-b-pt2`-shaped statistical ruling is not reviewable in a slot
at all and should be planned as its own slot. Consequence-free work is 2-5.

Seed the model from the tier, then correct it: phase 7's batch records carry the
*actual* minutes the human spent, and this estimate is what they calibrate.

## 4. `Unattended:` — the readiness grade

```
Unattended: ready | needs-slicing | never
```

Distinct from `Difficulty:`, which is static blast radius. This answers: can it
finish without me? The load-bearing rule for `needs-slicing`, and the reason this
is not difficulty renamed: **a task that would need context compaction to finish
is too big to run unattended.** `anthropics/claude-code#54393` — a postmortem of
five consecutive failed autonomous overnight runs — names "good plan → compact →
garbage drift" as a primary failure primitive, and nothing downstream catches it.

`never` covers science runs, releases, and anything whose deliverable is a judged
verdict rather than a merged PR.

(There is deliberately no `needs-decisions` grade and no preflight
question-harvest pass. See below.)

## 5. Fix `infer_autonomy` — as an experiment, not a graduation

`_intake.py:276` returns `supervised` whenever `repo_count > 1`, which fires on
nearly every real task and is why 120 of 137 prompts are supervised. Replace the
trigger set with the factors that actually predict a park: `architectural_risk`,
`human_judgement`, and difficulty at `large` and above. Multi-repo stays a
`Difficulty:` input, where it already is.

**Do not justify this with "238 rows, zero rejected".** Read
`two_slot_batching_epic.md` for why that statistic fails: the log is July
human-in-session work with ~7 rows for all of August, `rejected` is structurally
unreachable (a withdrawn five-PR mechanism was logged `reverted`; a
human-rejected recommendation was logged `amended`), two rows say verbatim "NOT a
clean row for graduation purposes", and every clean row was produced *with this
guard on*.

Ship it instead as a **dated experiment** recorded in `AUTONOMY.md`: 20
unattended launches under the new rule, external-review leg mandatory, rows
written per work-type, and an explicit `rejected-at-review` outcome that the
**human** stamps in the slot — so the demotion trigger can actually fire. If the
window is not clean, the doctrine edit reverts. Phase 3 adds the outcome value;
this phase writes the experiment's terms.

## 6. Re-grade the backlog

Run the model over all of `draft/` and write the new headers. Never overwrite a
human-declared value — the declared-outranks-derived rule already in
`effective_difficulty` applies to every one of these. Report disagreement rather
than resolving it silently.

Render tier and review-minutes on the dashboard, and replace Quick wins
(`small and safe`, currently near-empty) with **"fits a slot"**: `Unattended:
ready`, ordered by review-minutes ascending.

## Why there is no preflight question-harvest

The obvious companion idea — read a prompt and emit the decisions the run would
park on, so the human answers them up front — does not survive the evidence.
Of the 46 parked rows in `autonomy_log.md`, **19 park at ship sign-off**: the
contract park `supervised` imposes, which item 5 above dissolves outright. A
sample of the remainder was **0 for 8** on predictability from the prompt: the
fork appeared because the world differed from the prompt (a provisioning map
diverging from the plan's "7 scripts"), or only existed after reproduction (pin
`tfp-nightly`), or killed the premise mid-work ("RE-SCOPED: tail = env drift, not
9 code bugs"), or was Heart RED, or was environmental. The genuinely
preflightable decisions are already enumerated by the Intake Agent in the prompt.

Preflight would harvest what intake already harvested and miss what parks
actually park on, while spending slot minutes the epic cannot afford. The
residual is handled by phase 3's capped decide-and-flag instead.

## Done when

- `pyauto-brain sizing <prompt>` reports tier, witness presence, review-minutes
  and readiness alongside difficulty.
- The four keys are in `HEADER_FIELDS` hygiene and in `REFERENCE.md`.
- The before/after distribution is in the PR body, and the experiment's terms are
  in `AUTONOMY.md` with a date.
- Tests: no-witness ⇒ `judge`; repo class drives tier; declared beats derived.
