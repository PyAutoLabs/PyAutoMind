# How robust are magnification estimates? Model-match vs mismatch across the 10 Euclid lenses

Type: research
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoLens
- PyAutoArray
Themes:
- euclid
- pixelization
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: euclid-dr1-prep
Phase: 6
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28

Phase 6b of 10 in the Euclid DR1 preparation epic. **Gate: phase 5.** Runs in parallel
with 6a and 6c (6c is the source-code half of the same question and does **not** gate on
this). Science, on RAL — human-driven, `supervised`.

User request (verbatim):

"""
6b) How robust are our magnification estimates? There are known systematics in magnifciation estimation in some
previous research I did. General vibe is when the lens light and source model match the simulate ddata (e.g. Sersics fitted to Sersics)
its ok, but when there is mismatch (E.g. an MGE is used) it breaks. This can be due to two reasons: if the source becomes an MGE
its because the source model is mismatched from the simualtion. If the lens light becomes an MGE its the same but the lens light
"leaks" into the source model messing up the magnification. We have also never really validated or tested the magnifcitations using
the Delaunay source model, and this could even have bugs (E.g due to pixel areas not being quite right). So, for this
Euclid epic do all of the magnification comparisons you can on the 10 lenses in this spirit, but also have a follow up issue
which checks if the soruce code itself looks like it might have a bug or issue with the Delaunay area and thus magnification calculations.
"""

## The comparison matrix

The 10 phase-5 simulations have **Sersic lens light + Sersic source** and a recorded true
magnification. Fit each with a ladder of models and compare recovered μ against truth:

1. **Matched** — Sersic lens light, Sersic source. The control. Expected to be fine; if
   it is not, nothing below is interpretable.
2. **MGE source, Sersic lens light** — isolates *source*-model mismatch.
3. **MGE lens light, Sersic source** — isolates the **lens-light leakage** channel: lens
   light absorbed into the source model corrupts μ. This is a different failure mode from
   (2) and the two must be separated, not lumped as "MGE breaks it".
4. **MGE both** — the combination, to see whether the effects add.
5. **Delaunay source** (with Sersic and MGE lens light) — never validated. This is the
   novel leg.

Report per-lens and aggregate fractional μ error for each rung.

## Definitions matter

There is more than one magnification in play — the point/Hessian value and the
area-based ratio (`A_img / A_src`). State which is being compared at each rung and make
sure the truth recorded in phase 5 is the same quantity. A disagreement between the two
is itself a finding and should be handed to 6c.

## Prior art to consult before designing the runs

- `draft/test/workspaces/mesh_magnification_correctness.md` (cluster epic phase 4) covers
  simulate-and-recover magnification across every mesh variant, and its audit already
  found that `areas_for_magnification` exists for only two mesh geometries and has no
  direct test. Read it; do not duplicate it. This phase is the Euclid-data instance of
  the same question.
- The user's own earlier magnification research is the origin of the "matched is fine,
  mismatched breaks" intuition — surface it rather than rediscovering it.

## Deliverables

1. The full comparison matrix run on the 10 simulated lenses.
2. Per-rung fractional μ error, with the two mismatch channels (source-model mismatch vs
   lens-light leakage) reported separately.
3. An explicit verdict on the **Delaunay source** magnification: trustworthy, suspect, or
   broken.
4. Whatever the Delaunay leg shows, hand it to phase 6c
   (`draft/bug/autoarray/delaunay_area_magnification_audit.md`), which audits the source
   code independently.

## Acceptance / gate

- All five rungs run on all 10 lenses (or a documented, justified reduction).
- Source-mismatch and lens-light-leakage effects quantified separately.
- A written robustness verdict, including a usable statement of when Euclid DR1
  magnifications can be trusted and when they cannot.
- Feeds phase 7's magnification products.
