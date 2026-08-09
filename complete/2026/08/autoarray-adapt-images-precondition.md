Phase 3 of the @rhayes777 API audit —
[PyAutoArray#332](https://github.com/PyAutoLabs/PyAutoArray/issues/332), error
legibility for the missing-`adapt_images` precondition.

**Shipped:** PyAutoArray#442, squash-merged `5dedb5e` 2026-08-09. #332 closed.
Epic PyAutoArray#415 stays open for phase 4 only.

## Delivered

Omitting `adapt_images` with `Delaunay` / `KNearestNeighbor` / `KNNBarycentric` used
to surface as `AttributeError: 'NoneType' object has no attribute 'array'` from inside
`border_relocator.py` — naming nothing the caller controls, in a file they have never
opened. It now raises `exc.MeshException` naming `adapt_images`, showing the
`AdaptImages` idiom, and noting the rectangular family needs none.

Guard sits at `Delaunay.interpolator_from`, inherited by `KNearestNeighbor` and
`KNNBarycentric`, so one check covers all three adaptive meshes.

## The decision this task had to make, and record

The issue offered two routes and the reporter raised the first himself ("the wiring
... probably needs to move inside the mesh classes themselves"):

1. the mesh wires the image-plane grid up itself
2. fail fast, naming `adapt_images`

**Chose 2.** Building an image-plane mesh grid requires a *weighting policy* — which is
exactly what `adapt_images` carries. Inventing one inside the mesh would silently make
a science choice on the user's behalf, in precisely the case where they have signalled
nothing. Matches phase 1's handling of the rectangular/split combination (#417): an
explicit "you must supply X" rather than implementing a missing capability. The
reasoning is stated in the PR body and in the reply on #332, and the reporter is
invited to push back.

## The trap this prompt existed to avoid — avoided

The campaign prompt carried an explicit warning: an earlier revision said "any fix must
land with a regression test built the reporter's way", which followed literally would
assert that bare construction **succeeds** — enshrining the misreading in the issue
headline.

The tests assert the **clear failure** instead, plus controls that each adaptive mesh
*does* build when given its grid. So if these meshes ever genuinely break, the controls
fail and the public correction gets revisited rather than quietly becoming wrong.

Re-verified the headline correction on the branch (integration level, real
`FitImaging`): `Delaunay + Constant + adapt_images`, `KNNBarycentric + Constant +
adapt_images`, `Delaunay + ConstantSplit + adapt_images` all fit, and
`RectangularUniform + Constant` fits with no `adapt_images`.

## Correction to the recorded diagnosis

The prompt (and `planned.md`) stated the `None` was the `grid` argument at
`border_relocator.py:446`. It is actually **`mesh_grid`** at line 450. Same fix, but
the note was wrong and is now corrected in both places.

## Validation

- Full suite **991 passed / 51 skipped**, **+10 new tests**
  (`test_autoarray/inversion/pixelization/mesh/test_adapt_images_precondition.py`).
- The 3 `test_transformer.py` pynufft failures are **pre-existing on main** (baselined
  by stashing and re-running), tracked by
  `draft/bug/autoarray/pynufft_scipy_pinv2_dev_extra.md`.
- CI green on 3.12 and 3.13. **Zero regressions.**

## Not in scope, confirmed untouched

Part 2 of #332 (`ConstantSplit` on `RectangularUniform`) shipped in phase 1 (#417,
`9411904d`) covering all 9 rectangular × split combinations. The recorded phase-1
residue — that the guard fires at `Pixelization` instantiation rather than `af.Model`
composition time, so "fails before Nautilus starts" was never confirmed — remains an
open follow-up, unaddressed here.

## Original prompt

# PyAutoArray#332: make the missing-`adapt_images` precondition fail legibly

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

## Why this exists

[PyAutoArray#332](https://github.com/PyAutoLabs/PyAutoArray/issues/332), filed
2026-05-23 by @rhayes777. The issue reported two things; **one is already fixed
and one is a misreading that must not be implemented as written.** What remains
is a single error-legibility defect. Answered on the issue 2026-07-28
(`#issuecomment-5105855203`); tracking epic is
[PyAutoArray#415](https://github.com/PyAutoLabs/PyAutoArray/issues/415).

Unlike the other three audit prompts, this one has **no blocker** — it does not
need the shared `_validate_*` helper and can start immediately.

## ⚠️ Read this before touching anything

The issue's headline says `Delaunay` and `KNNBarycentric` are *"unusable in
`FitImaging`"*. **That is false.** Verified 2026-07-28:

```
Delaunay(pixels=100)       + Constant + adapt_images  ->  log_evidence 5084.7513   OK
KNNBarycentric(pixels=100) + Constant + adapt_images  ->  log_evidence 5211.7226   OK
Delaunay(pixels=100)       + ConstantSplit + adapt    ->  log_evidence 5096.4420   OK
Delaunay(pixels=100)       + Constant, NO adapt       ->  AttributeError 'NoneType'
```

Both adaptive meshes work correctly. They **require** an image-plane mesh grid:

```python
adapt_images = al.AdaptImages(
    galaxy_image_plane_mesh_grid_dict={source: image_plane_mesh_grid}
)
fit = al.FitImaging(dataset=dataset, tracer=tracer, adapt_images=adapt_images)
```

which is the idiom at
`autolens_workspace/scripts/imaging/features/pixelization/delaunay.py:246`.
Omitting it leaves the grid `None` three frames above the failure site.

**This inverts the fix direction.** An earlier revision of the campaign prompt
instructed *"any fix must land with a regression test built the reporter's way"* —
followed literally, that would assert bare construction **succeeds**, enshrining
the wrong expectation. The regression test must assert a **clear failure**.

The public reply on #332 corrects the headline while crediting the underlying
finding. **Keep that framing in any follow-up comment** — the correction is
already on the record and should not be re-litigated or softened.

## The actual defect

A missing required precondition surfaces as:

```
File "autoarray/inversion/mesh/border_relocator.py", line 446, in relocated_mesh_grid_from
    grid.array[self.border_slim], xp=xp
AttributeError: 'NoneType' object has no attribute 'array'
```

The `Optional[BorderRelocator]` guard at `mesh/abstract.py:90` is in place — the
problem is that the `grid` passed *into* `BorderRelocator.relocated_mesh_grid_from()`
is `None`, so the failure lands one level deeper and **names nothing the caller
controls**. A user gets `NoneType` and a file they have never opened, with no
mention of `adapt_images`.

## Wanted

Either:

1. the mesh wires the image-plane grid up itself (if that is the intended API
   now that `Delaunay(pixels=N)` / `KNNBarycentric(pixels=N)` no longer take an
   explicit image-plane mesh); **or**
2. construction fails immediately with a clear error **naming `adapt_images`**
   and pointing at the workspace idiom above.

Option 2 is the smaller, safer change and matches how phase 1 handled the
Split-on-rectangular case — an explicit "you must supply X" exception rather than
implementing a missing capability. Pick deliberately and record the reasoning in
the PR; the reporter raised option 1 himself ("the wiring ... probably needs to
move inside the mesh classes themselves") so if it is declined, say why.

## Already shipped — not in scope

Part 2 of #332, `ConstantSplit` broken on `RectangularUniform`, **is done**.
Phase 1 shipped an explicit unsupported-combination exception at
`Pixelization.__init__` covering all **9** rectangular-mesh x split-regularization
combinations (PyAutoArray#417 `9411904d`, merged 2026-07-28). Do not re-open it.

One residue is recorded in
`complete/2026/07/rectangular-adapt-constant-split-guard.md`: the guard fires at
`Pixelization` instantiation rather than at `af.Model` composition time, so
"fails before Nautilus starts" was **never confirmed**. That is a possible
follow-up, not part of this prompt.

## Binding constraint — JAX

This path is **JAX-traced**. The guard must stay correct under tracing and cost
nothing when traced.

## Verification

- Regression test asserting bare `Delaunay` / `KNNBarycentric` construction (no
  `adapt_images`) raises a **clear** error whose message contains `adapt_images`.
  Assert on the message, not just the exception type.
- Control assertions that must keep passing, with the exact values from the
  2026-07-28 run so a drift is visible:
  - `Delaunay(pixels=100) + Constant + adapt_images` → `log_evidence 5084.7513`
  - `KNNBarycentric(pixels=100) + Constant + adapt_images` → `log_evidence 5211.7226`
  - `Delaunay(pixels=100) + ConstantSplit + adapt_images` → `log_evidence 5096.4420`
  - `RectangularUniform(15,15) + Constant` → `log_evidence 4779.4288`
- **Always test the `adapt_images` branch as well as the bare one.** Testing only
  the reporter's construction is exactly what produced the wrong reading on
  2026-07-27.
- Library unit tests stay **numpy-only** (no JAX).

Repro gotchas: `al.Convolver.from_gaussian` is the PSF constructor (`al.Kernel2D`
no longer exists); run from a workspace root with
`PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1`, `NUMBA_CACHE_DIR=/tmp/numba_cache`,
`MPLCONFIGDIR=/tmp/matplotlib`, `PYAUTO_DISABLE_JAX=1`.

## Do not route to `start_dev_for_user`

The reporter's PR offer was declined warmly on 2026-07-28. We implement in-house.

## Provenance

- Epic: PyAutoArray#415 (open — phases 2-4); this prompt is phase 3's main half
- Campaign prompt: `draft/bug/autoarray/rhayes_audit_validation_and_crashes.md`
- Registry: `planned.md` § `rhayes-audit-validation-phases-2-4`
- B10, the other phase-3 item, rides with
  `draft/bug/autogalaxy/rhayes_440_profile_validation_guards.md`
