Review verdicts now record a **disposition per lifted claim** — the one change
the falsified-by efficacy review ([[falsified-by-checkpoint-efficacy-review]],
2026-08-18) recommended, moving mitigation 6 from remind-shaped to
detect-shaped: a rote adversarial pass is now visible ledger drift instead of
being indistinguishable from a healthy one.

- completed: 2026-08-18 (same-day follow-up to the efficacy review, same
  dashboard-work session, branch `claude/automind-falsified-by-checkpoint-cmsqsi`)
- target: PyAutoBrain

## The change

When the ReviewSurface lifts any `claims to falsify`, the reviewing agent's
verdict must carry one line per claim:

```
claim: "<lifted line>" → basis-cited: <the test/measurement/diff that shows it> | idle | FINDING (unverified-claim)
```

written by the **reviewer at verdict time**, never by the author (the
reader-enforced shape mitigation 6 was designed around). A bare CLEAN over a
non-empty claims surface is malformed evidence, not CLEAN — the ship
checkpoint reader can see the omission. An empty surface requires nothing, so
the 74–95% of ships that lift no claims gain no busywork.

Surfaces touched (all PyAutoBrain):

- `agents/faculties/review/AGENTS.md` — step 2a gains the disposition format;
  step 3's verdict mapping gains the malformed-evidence rule.
- `agents/faculties/review/_review.py` — the human-emit epilogue prints the
  disposition instruction, guarded to fire only when claims were lifted.
- `AUTONOMY.md` — autonomous-ship-gate review leg carries the requirement.
- `skills/ship_library/reference.md` — the `--auto` validation-checklist gate
  line shows where dispositions go in the PR body.
- `docs/agent_failure_modes.md` — item 6 Outcome updated from "filed" to
  "implemented".
- 2 new pinning tests in `tests/test_review_claims.py` (instruction present
  with claims, absent without); suite 351 passed.

No trigger-vocabulary change — the efficacy review measured the current
vocabulary as neither empty nor saturated and recommended none.

## Dogfood note

The faculty was run on the shipping branch itself: surface produced, zero
claims lifted from the commit message, and — per the new guard — no
disposition demand printed on the empty surface. Verdict CLEAN with no
dispositions owed, which is exactly the no-busywork path.

## Original prompt

# Review verdicts record a disposition per lifted claim

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

## What this is

The one change the falsified-by efficacy review
(`complete/2026/08/falsified-by-checkpoint-efficacy-review.md`, 2026-08-18)
recommended: make the reviewing agent's engagement with each `claims to
falsify` line **part of the recorded verdict**, so a rote pass becomes
ledger-visible drift instead of looking identical to a healthy one.

## The finding this fixes

Across the 22 review-leg ship gates since mitigation 6 went live
(2026-07-17 → 2026-08), zero `unverified-claim` findings were raised and only
2 gates left any evidence the claim pass was exercised — the other ~20
recorded a bare "review CLEAN". The ReviewSurface is ephemeral, so a healthy
adversarial pass and a skipped one write the identical ledger row. The stage
is remind-shaped; per the campaign ranking (deleting beats detecting beats
reminding) it should be detect-shaped.

## The change

In `agents/faculties/review/AGENTS.md` (procedure step 2a→3) and the ship
skills' evidence format: when the surface lists N > 0 `claims to falsify`,
the verdict must carry one line per claim:

```
claim: "<lifted line>" → basis-cited: <test/measurement/diff that shows it> | idle | FINDING (unverified-claim)
```

- CLEAN with a non-empty claims surface and **no disposition lines** is
  malformed evidence — the ship checkpoint reader (human on supervised runs,
  the autonomy-log row on `--auto` runs) can see the omission.
- Empty surface → nothing new is required (no per-ship busywork on the
  74–95% of ships where nothing lifts).
- This is documentation + evidence-format only; `_review.py` already prints
  the per-claim prompt. Optional: a `--json` consumer hint, no behaviour
  change.

## Constraints

- Do not turn it into an author checklist: the dispositions are written by
  the *reviewer* at verdict time, about lines the surface routed it to — the
  reader-enforced shape mitigation 6 was designed around.
- Keep it to the lifted claims only; no new trigger vocabulary (the efficacy
  review measured the current vocabulary as neither empty nor saturated and
  recommended no change).

<!-- filed 2026-08-18 by the falsified-by efficacy review (dashboard-work session) -->
