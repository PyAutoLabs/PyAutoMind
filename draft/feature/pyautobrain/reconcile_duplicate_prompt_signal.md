# `intake reconcile` should score prompts against each other, not only against records

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Filed: 2026-08-27

Every signal `intake reconcile` computes today scores a **prompt against the
completion archive** — `record-says-shipped`, `rare-topic-overlap`,
`shared-identifiers`, `referenced`, `stale-status`. Nothing scores the live
prompts **against each other**, and near-duplicate filings are a standing hazard
of a 134-prompt backlog that several independent sessions file into.

## The case that motivated this

Two prompts, same finding, five days apart, neither naming the other:

- `draft/bug/workspaces/jax_likelihood_pins_stale_by_1e4.md` (filed 08-14)
- `draft/bug/autolens/jax_likelihood_smoke_pins_stale.md` (filed 08-19)

Both were written from a `pyauto-heart smoke autolens_test` run against the same
failing gate. Both name the same three scripts. The 08-19 filing was verified and
retired on 08-26 (`complete/2026/08/jax-likelihood-smoke-pins-stale.md`); the
08-14 filing kept rendering as pickable backlog until a dashboard-drift audit
found it on 08-27 (`complete/2026/08/jax-likelihood-pins-duplicate-filing.md`).

**No existing guard sees this.** `lifecycle.py check`, `orphans` and
`index --check` all pass — the prompt was never `active/`, so no invariant
touches it. `intake reconcile` did not flag it either: the record that covers it
was written under a slug (`jax-likelihood-smoke-pins-stale`) whose tokens do not
overlap this prompt's (`jax-likelihood-pins-stale-by-1e4` shares `jax`,
`likelihood`, `pins`, `stale` — so the *slug* overlap is actually high, but the
reconcile signals compare prompt text to record text, and the record's own
`## Original prompt` section is the twin's text, not this one's).

## The signal

For each unordered pair of live prompts under `draft/` and `active/`, score:

1. **Shared file paths.** Source paths quoted in both bodies (e.g.
   `interferometer/jax_likelihood/mge.py`). This is the strongest signal — two
   prompts naming the same three source files are almost never independent work.
2. **Shared identifiers.** Reuse the existing identifier extractor that
   `shared-identifiers` already runs against records; point it at prompt pairs.
3. **Shared issue/PR references.** Two prompts citing the same
   `PyAutoFit#1473`-shaped reference.

Report as a new `duplicate-candidate` bucket, pair-wise, with the shared
artefacts listed so a human can adjudicate in one read. Like every other
reconcile output this is **advisory** — retiring or merging a prompt stays human.

## Sibling

`draft/feature/pyautobrain/intake_reconcile_absence_signal.md` (filed 2026-08-27,
PyAutoMind#353) proposes a different missing signal for the same tool: a prompt
quoting a source line that no longer exists in the file it names. That one
catches *shipped-with-no-Mind-trace*; this one catches *filed twice*. They share
the corpus walk, so implementing them together is likely cheaper than either
alone — but they are independent findings and either can ship first.

## Done when

- `pyauto-brain intake reconcile` emits a `duplicate-candidate` bucket.
- Run against the current backlog, its output is reviewed and any true
  duplicates it finds are filed as their own retirement work.
- The pair above is used as the regression fixture (both prompts are in
  `complete/`, so the fixture reconstructs them from the records' `## Original
  prompt` sections).
