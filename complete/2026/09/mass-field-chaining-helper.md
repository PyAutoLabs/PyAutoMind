## mass-field-chaining-helper
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/624 (closed completed 2026-09-19)
- completed: 2026-09-19
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/625 (merge 1652a0e8)
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/745 (merge 50c0046b)
- epic: mass-field (follow-up to the released flat fields API)
- summary: Added `mass_and_fields_from(mass, mass_result, *, fields_result, unfix_mass_centre=False)` in PyAutoGalaxy. It keeps `mass_from` mass-only and its return contract unchanged, while requiring callers to select a field explicitly and returning `(updated_mass, fields_result)`. PyAutoLens reexports the helper and tests both a carried field prior and a fixed instance field through a two-stage lens model; the model cookbook documents the route. The galaxy-attached identifier pin remains unchanged. Local suites: PyAutoGalaxy 1238 passed; PyAutoLens 740 passed, 1 expected failure. Every reported PR Docs and Tests leg passed for Python 3.12, 3.13 and no-JAX. Both PRs merged in library order on 2026-09-19. Publication remains pending before dependent workspace PRs may merge.

## Original prompt

# Carry a field with the mass through a chained stage

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Themes:
- cluster
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Decision: 2026-09-19 — keep `mass_from` mass-only; add a companion `mass_and_fields_from(mass, mass_result, *, fields_result, unfix_mass_centre=False)` that returns both components and requires the field explicitly
Consequence: judge
Witness: a chained two-stage test (stage 1 `Isothermal` + a `MassField` shear, stage 2 `PowerLaw` built through the chaining helper) asserts stage 2's model carries the field — `fields.shear.gamma_1` in `unique_prior_paths` and `tracer.fields` length 1 on the composed instance — and FAILS on unfixed `main` (the field is absent, prior_count short by 2) before the change; the galaxy-attached identifier pin is unchanged.
Review-minutes: 20
Unattended: needs-slicing
Epic: mass-field
Filed: 2026-09-18
Issued: 2026-09-19

## The gap

`PyAutoGalaxy/autogalaxy/analysis/chaining_util.py::mass_from(mass, mass_result,
unfix_mass_centre=False)` takes **no `fields` argument**, and there is **no `fields`
handling anywhere in `PyAutoLens/autolens/util/`** (AST sweep, 2026-09-18). The helper
exists precisely to carry a previous search's mass model forward into the next stage.
Under the `fields=` API the external field is no longer part of the galaxy, so the
helper carries the mass and leaves the field behind.

Every chained consumer that migrates to `fields=` therefore has to hand-write a
per-stage `fields=` decision, and the failure mode is **silent**: a stage that carries
`galaxies` forward but omits `fields=` loses the external shear with **no error and no
log line**. The model simply has two fewer priors and the fit is of a different system.

This is not hypothetical. The completed flat-`fields=` sweep found exactly that bug
live on `main` in
`autolens_workspace/scripts/multi_dataset/features/one_by_one/modeling.py` — a chained
stage inheriting result galaxies with the shear dropped. It was fixed in
autolens_workspace#562 as a by-product; nothing in the library would have caught it,
and nothing today stops the next one.

## Why `feature` and not `bug`

Argued, because it is borderline. The library behaves exactly as written: `mass_from`
is documented as a *mass* helper and does what it says. Nothing regressed — the gap
opened when `fields=` became the user-facing API (epic `mass-field`, human ruling
2026-09-17), which is a new capability the helper never grew an argument for. So:
**`feature`**, a missing argument on a public helper.

The counter-argument, recorded so nobody re-litigates it: the *observable* is a wrong
model composed with no diagnostic, which is bug-shaped, and one instance of it shipped
to `main`. If the chosen design turns out to be "`mass_from` should always have
threaded the field", re-classify on the issue rather than re-filing.

## The design question (do not presume the answer)

**Resolved after source inspection (2026-09-19).** `mass_from` receives only a
mass profile/model and returns that mass model. Adding `fields=` to it cannot
put a field in the next stage's top-level collection without changing its
return type or mutating the mass model into an invalid shape. Keep its public
contract and identifiers unchanged. Add a companion `mass_and_fields_from`
which delegates mass prior passing to `mass_from` and returns
`(updated_mass, fields_result)`; make `fields_result` a required keyword-only
argument so a caller using this route cannot silently omit the field. The
caller chooses `result.model.fields` (free with posterior priors) or
`result.instance.fields` (fixed). A warning in `mass_from` is impossible from
its current inputs: `mass_result` contains no reference to the result's
top-level field. The chained-stage witness will exercise the companion helper.

Chaining is **shape-transparent** — free versus fixed rides on `.model` versus
`.instance` of the previous result, not on the helper. Measured on the flat form
(report A of the 2026-09-18 audit): stage 2 taking `result.model.fields` gives
prior_count 15, `result.instance.fields` gives 13, in *both* the collection and flat
forms, with `tracer.fields` length 1 either way. So threading the field through is a
plumbing decision, not a semantics one, and the question is where the plumbing belongs:

- **(a) `mass_from(mass, mass_result, fields=None, unfix_mass_centre=False)`** — one
  call site per stage, the field travels with the mass it belongs to. Cheapest for
  callers; widens a helper whose name says "mass".
- **(b) a sibling `fields_from(fields_result, ...)` helper** — honest naming, mirrors
  the model slot, composes with `mass_from` at each stage. Two calls per stage instead
  of one, and the silent-drop mode survives for anyone who writes only the first.
- **(c) both** — `fields_from` as the primitive, `fields=` on `mass_from` as the
  convenience that calls it.

Whatever is chosen, the value of the change is that the **default is not silence**.
Consider whether the helper should *refuse* (or at minimum warn) when the previous
result carried a field and the new stage was given none, since that is the exact shape
of the shipped bug. That is a public-API/error-contract call — hence
`Consequence: judge`.

## Scope

- PyAutoGalaxy: `autogalaxy/analysis/chaining_util.py` (the helper itself, its
  docstring, its unit tests).
- PyAutoLens: `autolens/util/chaining.py` re-export surface and any lens-side wrapper,
  plus the SLaM chaining docs if they quote the signature.
- **Witness must include a chained stage that would silently drop the field today** —
  written red against unfixed source first (memory `WitnessRed`), not asserted after
  the fix.
- Backwards compatibility: the galaxy-attached form is undeprecated and unwarned
  (epic invariant). Existing `mass_from(mass, result)` calls keep their identifier;
  the identifier pin is part of the witness.

## Blocks

**This prompt blocks the remaining-code-consumer sweep**
`draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md`, whose
riskiest file (`autolens_inference/scripts/misc/slam/_runner.py`) is a live staged SLaM
pipeline chaining `Isothermal+ExternalShear` into `PowerLaw` through this very helper.
It also bears on `autolens_workspace_developer`'s three live SLaM pipelines
(`draft/maintenance/autolens_workspace_developer/mass_field_flat_adoption_developer.md`),
if the human rules that repo in scope.

Filed 2026-09-18 from the flat-`fields=` adoption sweep's follow-up audit
(issue autolens_workspace#561; PRs autolens_workspace#562 + autolens_workspace_test#322,
both DRAFT pending the PyAutoGalaxy/PyAutoLens release).
