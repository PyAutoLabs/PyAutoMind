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
