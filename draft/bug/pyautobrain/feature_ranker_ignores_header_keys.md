# The Feature Agent's ranker ignores the prompt header keys it is documented to act on

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

## Why this is a bug and not a feature request

`REFERENCE.md` ("Optional metadata header") states the contract outright — the
Intake Agent writes `Difficulty:` from the shared sizing faculty

> so the value shown up front is the one the Feature Agent later acts on.

It does not act on it. `agents/conductors/feature/_feature.py` mentions
`Difficulty` exactly once, at line 258, where it **prints** its own freshly
derived score. It reads no header key from the prompt at all — not `Difficulty:`,
not `Status:`, not `Priority:`, not `Blocked-by:` / `Closes-when:`. So a value
Intake persisted is silently discarded by the one consumer it was persisted for.

The gate keys make it worse, because they already have a grader: PyAutoMind's
`scripts/lifecycle.py issues --drafts` reports a satisfied `Closes-when:` as
*likely shipped* and a satisfied `Blocked-by:` as *ready to start* (Mind #168).
The Brain's ranker, which is the thing actually choosing what to work on next,
sees none of it.

## Observed, in one run

`bin/pyauto-brain feature select` ranked
`draft/feature/autonomy/10_scheduled_runs.md` **first** and emitted it as the
recommended pick. That prompt carries:

```
Difficulty: medium
Priority: low
Status: blocked
...
Blocked-by: 7_queue_runner.md (and transitively 1–5). Do not start before the
queue runner has completed several supervised interactive runs cleanly.
```

Three independent declarations that it must not be picked, and a fourth
disagreement: the ranker scored it `small` against its declared
`Difficulty: medium`.

Second symptom from the same run:
`draft/feature/pyautomind/draft_staleness_detection_signals.md` ranked
`too-large` (score 13, #26 of 28) on total file length — but legs 1 and 2 of
that prompt are shipped and annotated as such in its own § Acceptance, and the
only remaining work (leg 3) is one medium leg. Length is being used as a proxy
for size, and it is a bad one: a prompt grows as it accumulates *findings*, and
a well-documented prompt is not a large task.

## Scope

1. Parse the header keys already defined in `REFERENCE.md` and honour them in
   `select` mode:
   - `Status: blocked` and an unsatisfied `Blocked-by:` — exclude from the
     shortlist, or list in a clearly separated "blocked" band. Never the
     recommended pick.
   - `Priority:` — an ordering input, not merely display.
   - `Difficulty:` — prefer the **declared** value over the re-derived one when
     present. That is what "the value the Feature Agent later acts on" means; the
     derived score becomes the fallback for prompts with no header.
2. Report the disagreement rather than hiding it: when a declared `Difficulty:`
   and the derived score differ, say so in the decision. The disagreement is
   evidence about the sizing heuristic and is worth surfacing, not silently
   resolving.
3. Decide what `select` does with a satisfied `Closes-when:` — a prompt whose own
   exit condition has closed is a candidate for retirement, not for development,
   so at minimum it should not be recommended. `lifecycle.py issues --drafts`
   already grades this; the ranker can consume that reading rather than
   re-implement it.

Out of scope: changing the sizing faculty's derivation itself. This is about the
consumer honouring what is declared.

## Acceptance

- `feature select` does not recommend a prompt declaring `Status: blocked` or an
  unsatisfied `Blocked-by:`; a regression test pins `10_scheduled_runs.md`'s
  header shape (as a fixture, not the live file).
- A prompt with a declared `Difficulty:` is sized by that value, and a
  declared/derived disagreement appears in the decision output.
- `Priority:` measurably changes shortlist order in a fixture with two otherwise
  equal prompts.
- Existing `select` behaviour for header-less prompts is unchanged.

<!-- filed 2026-08-10, found while planning
     draft/feature/pyautobrain/samplers_surface_autolens_tiers.md — the ranker's
     top pick had to be rejected by hand against the registry. Classified by the
     Intake Agent as feature/ (medium confidence) and re-homed to bug/: the
     REFERENCE.md contract above makes this incorrect behaviour, not a missing
     capability. Sizing kept from that intake pass. -->
