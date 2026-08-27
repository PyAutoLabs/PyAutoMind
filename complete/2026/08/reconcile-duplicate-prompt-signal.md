- issue: none — filed as a PyAutoMind prompt on 2026-08-27 by the dashboard-drift
  audit that found the duplicate.
  Prompt: `draft/feature/pyautobrain/reconcile_duplicate_prompt_signal.md`
  (retired by this record).
- shipped: 2026-08-27 — PyAutoBrain#307 (main 3b4eedf7). Shipped in one PR with
  its sibling `intake-reconcile-absence-signal`; both add a signal to the same
  scan and share its corpus walk.
- classification: feature (PyAutoBrain) — a new offline leg on the
  `intake reconcile` ranker.
- summary: every signal reconcile had scored a prompt against the completion
  ARCHIVE. Nothing scored the live prompts against EACH OTHER, and that blind
  spot let two filings of one finding both stay live —
  `bug/workspaces/jax_likelihood_pins_stale_by_1e4.md` (08-14) and
  `bug/autolens/jax_likelihood_smoke_pins_stale.md` (08-19), the same three
  scripts from the same failing smoke gate, five days apart, neither naming the
  other. Leg 5 pairs live prompts on shared upstream source paths, rare
  identifiers and tracking references. Reconstructed from the two records'
  `## Original prompt` sections, it pairs them at 12.0 — the regression fixture
  the filing prompt asked for.

## Precision: 36 pairs -> 2

Scoring every shared artefact flagged 36 pairs of 134 prompts, which is not a
surface anyone reads. Three filters:

- **Bare basenames never count**, and a path named by more than four prompts is
  dropped. `start_here.py`, `modeling.py`, `simulator.py`, `no_run.yaml` are
  workspace-wide conventions repeated across hundreds of example folders — two
  prompts sharing one share a convention, not a task. **This alone removed 31 of
  the 36.** It is the same discrimination `_TOKEN_COMMON_DF` and
  `_IDENT_COMMON_DF` already make against the records.
- **Mutual reference disqualifies.** A phased parent and its child name each
  other; that is a series. The measured duplicate pair named neither the other,
  which is exactly why it survived every guard.
- **A folder index naming both disqualifies.** The four
  `draft/bug/health_fixes/` prompts were split out of one health run by CAUSE,
  not by script, so they share their failing scripts and no two name each other.
  The folder's own `README.md` names all four, and that index IS the
  declaration. Without it the trio yields three pairs of already-known work.

## Key traps / findings

- **The first filter idea was wrong and the data said so.** The plan was to
  treat "both prompts cite their common folder" as a declared series. Measured:
  none of the health_fixes prompts cites the folder path at all — that sentence
  lives in the RECORDS, not the prompts. The signal that does exist is the
  folder's README. Checking beat assuming, and the wrong version would have
  fired on nothing.
- **A trio yields three pairs.** Pair-wise output is what the filing prompt
  asked for and what a human reads, but N related prompts produce N(N-1)/2 rows.
  Kept pair-wise deliberately — clustering is a bigger change than this leg
  earns — which is another reason the declared-series filters matter.
- **Index files are not filings.** `README.md` / `index.md` / `AGENTS.md` under
  `draft/` describe a folder's prompts rather than being one, and were excluded
  from pairing.

## Follow-ups

- **The two live pairs it currently reports are unadjudicated.** Neither was
  read as part of this task; they are a surface, not a finding. Deliberately not
  filed as a prompt — reading a duplicate candidate is a `/intake reconcile`
  chore, not a task with a trigger.

## Original prompt

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
