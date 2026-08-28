# Claude Development Prompt: Joint `ell_comps` Disk Constraint

Type: feature
Target: PyAutoGalaxy
Themes:
- jax-gradient
- samplers
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Issued: 2026-08-27

## Goal

Give the elliptical-components parametrisation a constraint the searches can
actually honour, so a gradient MAP optimizer cannot spend its budget — or
finish — outside the physical region.

`ell_comps = (e1, e2)` is physical only inside the unit disk `|e| < 1`. Every
profile's default priors are two INDEPENDENT box priors on `e1` and `e2`
(typically `[-1, 1]` each), which is a SQUARE. The disk covers `pi/4` of that
square, so **21.5% of the prior box is non-physical by area**, and nothing in
the search stops a lane from sitting there.

## What was measured (autolens_profiling, 2026-08-27 harvest, issue #182)

- **The existing validation is a no-op where it matters.** `validate_ell_comps`
  fires on standalone profile construction, but not on the tracer-mode path a
  MultiStart lane actually evaluates — so a lane at `|e| >= 1` is never told.
- **20.1% of MultiStart lane best points end at `|e| >= 1`** (1,252 of 6,240
  lane best points across the recorded campaign).
- **0 of 246 lanes that HIT the target basin end there.** The two populations
  are cleanly separated: ending outside the disk is a property of failed lanes,
  never of successful ones. That is what makes this a searchability defect
  rather than a cosmetic one — the wasted 20% is wasted budget, not a wasted
  answer.
- **Positions-on roughly DOUBLES the out-of-disk fraction** (17% -> 29% of best
  points on the Phase-4 diagnostic arms). The positions penalty pushes lanes
  into the corners the box permits and the geometry does not.

Full write-ups: `autolens_profiling/results/notes/inference/
phase_03_prodigy_reliability/RESULTS.md` and `phase_04_positions/RESULTS.md`.

## Options to weigh (this prompt does not pick one)

1. **A joint disk assertion the clipper honours.** Express `e1^2 + e2^2 < 1` as
   a constraint the search's prior-box clipper can project onto, rather than as
   a post-hoc validation that raises. The clipper already insets a box; a
   ball projection is the same operation in a different norm. Cheapest change,
   keeps the existing parameter names and every recorded identifier stable, and
   is the only option that helps a search already in flight.
2. **Reparameterise.** Sample in a coordinate whose whole domain is physical —
   e.g. `(magnitude, angle)` with a bounded magnitude, or a squashing map onto
   the disk. Removes the problem by construction, but changes the model's
   parameter set, and therefore every `target_id`, prior config and recorded
   posterior that names `ell_comps_0`/`ell_comps_1`. It needs a migration story
   before it needs an implementation.

## Hard constraint

**Never make `validate_ell_comps` fire on tracers.** Raising from the
tracer-mode path turns a 20%-of-lanes condition into a 20%-of-lanes crash in
the middle of multi-hour GPU fits, and would make a MultiStart search die on
exactly the lanes it is supposed to clip and move on from. The fix belongs in
the search's constraint handling (option 1) or in the parametrisation (option
2) — not in a validator that converts a survivable state into an exception.

## Requirements

- Decide between the two options above with the evidence in the write-ups
  named, and record the decision before implementing.
- Whatever lands, add a test that a lane placed at `|e| >= 1` is handled by the
  chosen mechanism (projected, or unrepresentable) rather than merely detected.
- Quantify the effect on the measured 20.1% figure on at least one cell before
  claiming the defect is closed.
- Do not change `validate_ell_comps`'s standalone-construction behaviour.

## Out of scope

- The positions-penalty scaling question (Gate B pt 2, `autolens_profiling`
  issue #182) — the doubling is evidence FOR this task, not a task itself.
- Re-running any autolens_profiling campaign.
