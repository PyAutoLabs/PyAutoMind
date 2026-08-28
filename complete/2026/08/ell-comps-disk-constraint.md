## ell-comps-disk-constraint
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1537
- completed: 2026-08-28
- library-pr: PyAutoFit#1538 (merged 96dad5191 -> main f466dce1a), PyAutoGalaxy#589 (merged 1d8ae08b -> main 0fbe863d)
- decision recorded before implementing: **option 1** of the prompt (a joint disk constraint the clipper honours). Option 2 (reparameterise to `(magnitude, angle)` or a squashing map) was rejected for now — it re-keys every `ell_comps_0`/`ell_comps_1` `target_id`, prior config and recorded posterior, so it needs a migration story before an implementation; option 1 is also the only one that helps a search already in flight.
- what shipped (PyAutoFit#1538): `__model_ball_constraints__` — a class-declared `((path, radius), ...)` naming a tuple prior confined to a disk, duck-typed exactly like the existing `__model_constraint__` so a profile library states its own geometry without inheriting from PyAutoFit. `AbstractPriorModel.ball_constraint_index_pairs()` resolves declarations to sorted, de-duplicated `(index_0, index_1, radius)` triples into the physical parameter vector, cached under `__dict__["_ball_constraint_index_pairs_cache"]` (the underscore-prefixed `parameterization` convention the pytree/`ModelInstance` paths skip). `af.ClipperPriorBoxJoint` — an **opt-in** `ClipperPriorBox` subclass that clips the box and then radially shrinks each declared pair onto its ball; a strict no-op on a model declaring no geometry. Plus `Model.has_ball_constraints`, `constraint.MODEL_BALL_CONSTRAINT`, `declares_ball_constraints()`, `ball_constraints_for()`.
- what shipped (PyAutoGalaxy#589): `EllProfile.__model_ball_constraints__ = ((("ell_comps",), convert.ELL_COMPS_MAGNITUDE_CLAMP),)`, declared once at `EllProfile` so it reaches every elliptical light and mass profile. Spherical subclasses inherit the declaration but pin `ell_comps` to an instance, so PyAutoFit resolves no pair and projects nothing. Also widens `AnalysisDataset.save_results`' catch to `(AttributeError, af.exc.SamplesException, af.exc.FitException)`, mirroring PyAutoLens#713 — building the galaxies materializes the max-log-likelihood sample as a model instance, which the model may reject, and writing an optional output file must never kill a completed fit before `paths.completed()` (PyAutoFit#1535).
- **radius is the CLAMP (0.999), deliberately not `1 - margin`.** Between 0.999 and 1.0 the conversion to an axis ratio saturates, so the likelihood is flat radially: a lane projected into that annulus is moved from a region the model rejects into one the optimizer cannot leave. Projecting onto the clamp puts it exactly where the radial gradient is alive again.
- jittability was designed in, not discovered: the shrink factor is a `where`, the radius is compared **squared**, and the `sqrt` argument is substituted **before** the `sqrt` (the double-`where` idiom) so `jax.grad` stays finite at the origin — the case a naive radial shrink returns a correct value and a `NaN` gradient for. Both members of a moved pair are masked, which is what lets `MultiStartGradient` zero the outward momentum in both coordinates rather than one.
- unsupported combinations raise rather than degrading silently: `AbstractBFGS._bounds_from` raises `exc.SearchException` when a `ClipperPriorBoxJoint` meets a ball-declaring model (a ball is not a `scipy.optimize.Bounds`), and `AbstractMultiStartGradient.__init__` raises `ValueError` for a joint clipper alongside a non-default `scaler` or `bijector` — neither change of variables maps a disk to a disk. Both raise **at construction**, so a multi-hour fit does not die a minute in.
- identifier safety: `ClipperPriorBox.__identifier_fields__` pinned to `("margin", "strict_epsilon")` — exactly what the identifier's argspec fallback already inferred — so existing search identifiers and output directories are byte-identical (verified hash-for-hash across `MultiStartAdam`+`ClipperNone`, `LBFGS`+`ClipperPriorBox` and `ClipperPriorBox()` alone), and a subclass adding a constructor argument cannot silently re-key stored results. `ClipperPriorBoxJoint()` hashes differently, as it must.
- quantified against the prompt's 20.1%, on one cell: 200,000 uniform draws from an `Isothermal`'s `ell_comps` prior box — **21.57% outside the disk before projection** (analytic `1 - pi/4` = 21.46%), **0.00% after**. The canonical failing point `(0.9, 0.9)` (`|e| = 1.2728`) projects to `|e| = 0.999000` with the angle preserved, mask set on both members and nothing else; the default `ClipperPriorBox` leaves it at `1.2728` with an all-false mask.
- hard constraint honoured: `validate_ell_comps` is **unchanged** and still fires only on standalone profile construction. Making it fire on the traced path would turn a 20%-of-lanes condition into a 20%-of-lanes crash mid-fit.
- validation: `test_autofit/` 2288 passed / 3 skipped; 17 new tests across `test_clipper.py`, `test_model_constraint.py` and `test_multi_start_gradient.py` (a lane seeded outside the disk is *projected*, not merely detected — the prompt's requirement). Unit tests stay numpy-only, no `import jax`; the jit/grad/vmap behaviour was checked out-of-band. Downstream `test_autogalaxy/` 1144 passed, `test_autolens/` 553 passed.
- **no workspace smoke was needed and none was run**: the clipper is opt-in and no workspace script selects it, so every existing script keeps the default `ClipperPriorBox` and its byte-identical identifiers. Adoption is one argument — `af.MultiStartAdam(clipper=af.ClipperPriorBoxJoint())`.
- heart-ack: shipped and merged under the human-acknowledged RED of 2026-08-28 — red reason verbatim "release validation FAILED (stage integrate)", the known pre-existing failure unrelated to these branches.
- follow-up (unfiled): nothing in `autolens_workspace` demonstrates the joint clipper, and the 20.1% figure has not been re-measured on a live MultiStart campaign — only on the geometric cell above. A workspace example plus a campaign re-measure are the natural next tasks, and option 2 (reparameterisation) remains open behind its migration story.

## Original prompt

# Claude Development Prompt: Joint `ell_comps` Disk Constraint

Type: feature
Target: PyAutoGalaxy
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
