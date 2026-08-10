## feature-ranker-ignores-header-keys
- issue: (none — shipped directly from the draft prompt in the same session that filed it)
- completed: 2026-08-10
- brain-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/217 (squash-MERGED as e099383; pytest 3.12 + 3.13 green, 291 passed / 0 failed)
- prompt: draft/bug/pyautobrain/feature_ranker_ignores_header_keys.md (folded below)
- summary: the Feature Agent's ranker now reads the prompt metadata header it was
  always documented to act on. `declared_header()` lands in the SIZING FACULTY
  (beside the derivation it overrides, so declared and derived stay in one place
  and the bug/refactor conductors get the same reading for free); `_feature.py`
  honours it — declared `Difficulty:` overrides derived, `Priority:` orders the
  shortlist above the difficulty term, and `Status: blocked` / an unresolved
  `Blocked-by:` sinks a prompt below everything so it can never be recommended.
- root cause, stated exactly: REFERENCE.md promises Intake persists `Difficulty:`
  "so the value shown up front is the one the Feature Agent later acts on".
  `_feature.py` mentioned `Difficulty` ONCE, where it PRINTED its own re-derived
  score. It read no header key at all. A documented round-trip with no consumer.
- TRAP that would have broken the fix on its own bug report: the fenced-block
  skip is load-bearing, not tidiness. The bug prompt QUOTES the offending header
  in a ```-block, so a naive line scan makes the bug report declare ITSELF
  blocked. Same rule, same reason, as PyAutoMind `lifecycle.py:draft_gate_refs`
  — which had already hit this and solved it. Two smaller ones: trailing
  `# note` comments must be split on " #" so a `Repo#123` ref survives (the live
  backlog has both on one line), and an unrecognised `Difficulty:` value must be
  ignored rather than trusted.
- deliberate conservatism: `declared_blocked()` treats an unresolved `Blocked-by:`
  as blocked, because this agent is offline and cannot tell whether the gate has
  since closed — `lifecycle.py issues --drafts` is what resolves refs against
  GitHub, and the output points at it. Being wrongly held back is cheap and
  visible (still listed, own labelled band); being wrongly recommended is the
  failure the fix exists to stop.
- measured on the live backlog: the offending prompt
  (`draft/feature/autonomy/10_scheduled_runs.md`) drops rank 1 -> LAST of 27;
  TWO further blocked prompts surfaced that had NOT been spotted by hand
  (`ep_analytic_updates`, `oversampled_psf_dataset_adoption`);
  `draft_staleness_detection_signals` moves `too-large` #26 -> `medium` #5; five
  declared/derived disagreements became visible instead of silent.
- why length was a bad size proxy (recorded because it will recur): the derived
  score weights prompt size, and a prompt GROWS AS IT ACCUMULATES FINDINGS — so
  a long, well-documented prompt derives `too-large` for work that is not. That
  is precisely what a declared `Difficulty:` is for, now documented in the
  Feature Agent's AGENTS.md.
- evidence the tests bite: reverting ONLY `_feature.py` fails 7 of the 10 new
  tests; the 3 survivors are pure `declared_header` unit tests, which is
  coherent since they exercise `_sizing.py`. The regression case pins the
  offending prompt's HEADER SHAPE as a fixture, not the live file, so fixing the
  backlog cannot silently retire it. Fixtures use invented repo names, so the
  new test file adds no tenant-firewall instance facts (verified).
- CI-vs-local note worth keeping: `tests/test_skill_install.py` fails 2 tests in
  a cloud/web session (the installer reports "Environment: web-github / ci-only"
  and skips the Codex leg the assertions expect) but passes in GitHub CI — CI
  reported 291 passed / 0 failed. Do not chase those two locally.
- SECOND INSTANCE OF THE SAME DEFECT CLASS, found while doing this and NOT fixed:
  `pyauto-brain bug <this very prompt>` returned "Fix strategy: defer/re-home
  (looks like a feature/ task, not a bug)" — because the prompt says "Feature
  Agent" repeatedly and the Bug Agent classifies on prose keywords while
  ignoring the declared `Type: bug` header. Same family as the ranker bug just
  fixed, different conductor. Unfiled.

## Original prompt

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
