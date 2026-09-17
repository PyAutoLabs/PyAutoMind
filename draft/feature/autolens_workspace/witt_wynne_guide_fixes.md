# Witt–Wynne guide: apply the 2026-09-17 numerical-review fixes and correct its claims

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- point-source
- guides
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 15
Unattended: never
Filed: 2026-09-17

Supersedes draft/test/autolens_workspace/witt_wynne_tests_and_review.md (the review
it asked for was carried out on 2026-09-17; this prompt ships its consequences).

## Original request (verbatim)

> We recently implemented the Witt-Wynne thing (although I now cant find its guide
> in the autolens_workspace). So find all that, do a review that it is definitely
> numerically sound and implement correctly [...]

## Context

Independent numerical review of `scripts/guides/misc/witt_wynne.py` (2026-09-17;
report attached to the issue). SOUND: quartic solver to 1e-13 off-axis, PA map
`(θ_ccw + 90) mod 180`, e conversion, minus sign on shear, b from
`LensCalc.einstein_radius_from`, `.in` field order and h handling, time-lag constant
(0.12 % low from the C++'s own rounded literals — keep, document). FINDINGS:

1. SEVERE — `_mass_and_shear_from` (lines 551–555) returns an MGE light `Basis`
   (a `MassProfile` subclass) as the mass profile on an MGE + SIE + shear model:
   84° PA error, silent.
2. HIGH — `find_intersections` (142–155) keeps wrong-branch quartic roots; the
   solver never returns 1 image (0/24 at 4× the caustic scale) and 175/4860 images
   fail the lens equation by a median 2.4".
3. HIGH — sources on the potential axes (p=0 or q=0), at the centre, at e=0 or
   e≥1 return finite wrong positions, ±inf, NaN or silently nothing (lines 213–214).
4. HIGH — `witt_wynne_vector_sum` (668–672): e collapses to 1e-17 when e_pot = γ
   aligned, giving 5.7e6" positions and 1e8-day lags without an exception.
5. MEDIUM — the Wrap Up (944–946, 960–965) generalises a 5/5 verdict; on a 136-case
   grid the outside-caustic agreement is 51/68 (caustic-matched) vs 22/68
   (vector-sum); astroid fit residual −10 %/+11 % at q=0.5.
6. Unguarded: sub-critical lens → IndexError (597–601); shear-only galaxy →
   AttributeError (590); `centre` is (x,y) but `source_centre` is (y,x) (574–587).

## Deliverables

1. Fix 1–4 and 6 in the guide (guards return NaN rows with an `n_images=-1`
   sentinel; never raise, never a silent number). Keep the pure-numpy port and the
   `.in`/CSV writers' interface unchanged so the pipeline copy stays in step.
2. Extend the validation section with the review's grid (q × γ × misalignment,
   inside and outside the caustic; an MGE + SIE + shear case) and rewrite the Wrap Up
   and `__Conventions__` to state the measured agreement, the recommended
   projection (caustic-matching), and the on-axis behaviour.
3. Regenerate the notebook per the workspace convention; keep the `smoke_tests.txt`
   entry and the `ENV: full_datasets` assertion; runtime stays under ~30 s.
4. Note in the guide that the compiled Zenodo C++ round-trip could not be re-run in
   this workspace (the `.cpp` is not present) and how to reproduce it.
