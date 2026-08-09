# rectangular-adapt-constant-split-guard

- shipped: 2026-07-28 (phase 1 of the @rhayes777 audit epic; the prompt never left `draft/`)
- epic: https://github.com/PyAutoLabs/PyAutoArray/issues/415 (open — phases 2-4 remain)
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/332 (the reporter's finding), tracker #416 closed
- prs: PyAutoArray#417 (`9411904d`) + PyAutoLens#662 (`2a3f1a63`), both merged
- repos:
  - PyAutoArray
- see-also: `draft/bug/autoarray/rhayes_audit_validation_and_crashes.md` § "Phase 1 completion record — 2026-07-28"

## Summary

A duplicate prompt for work that shipped as phase 1 of the @rhayes777 API-audit
epic. The Mind already held the completion record — inside the *sibling* prompt
`rhayes_audit_validation_and_crashes.md`, which planned.md tracks — but this
second, independently-filed prompt for the same surface never learned about it.

Recorded 2026-08-09 by the draft/ sweep. No work is owed on the library leg;
one leg of the prompt's § Verification is noted below as unconfirmed.

## Verified against PyAutoArray main (`efaf3041`), 2026-08-09

The prompt asks for "an explicit validation guard which rejects this unsupported
configuration early, with an error message that tells users what to do instead".
That guard is on main:

- **Guard**: `Pixelization.__init__` (`autoarray/inversion/pixelization.py:154`)
  raises `exc.PixelizationException` when a split regularization meets a mesh
  that does not support it. The message names both classes and tells the user
  the two ways out — an adaptive mesh (`Delaunay`/`KNNBarycentric`) with the same
  regularization, or a non-split scheme (`Constant` for `ConstantSplit`, `Adapt`
  for `AdaptSplit`) with the same mesh. Substantively the prompt's suggested text.
- **Mechanism**: two capability flags rather than a type blacklist —
  `AbstractMesh.supports_split_regularization` (default `True`, set `False` on
  the rectangular family) × `AbstractRegularization.is_split_regularization`
  (default `False`, set `True` on `ConstantSplit`/`AdaptSplit`/`AdaptSplitZeroth`).
- **The false pass-through is gone**: `InterpolatorRectangular`'s claim that split
  "reuses the same mappings" — the source of the `IndexError: index 4 is out of
  bounds for axis 0 with size 4` this prompt reproduces — no longer stands;
  `interpolator/rectangular.py:466` now records that the combination is rejected
  at construction instead.

Against the prompt's § Verification:

1. **Criterion 1 (concrete construction raises) — MET.**
   `test_autoarray/inversion/pixelization/test_split_regularization_support.py`
   parametrizes all **9** rectangular × split combinations (the prompt reported
   1) and asserts both class names appear in the message.
2. **Criterion 2 (`af.Model` composition form fails before Nautilus starts) —
   NOT CONFIRMED.** The guard sits in `Pixelization.__init__`, so it fires
   whenever the model is instantiated rather than at composition time. A search
   for `supports_split_regularization` in PyAutoLens returns nothing, so no
   separate pre-fit model-inspection guard was added. In practice the concrete
   guard is reached on the first instantiation, which is early — but that this
   precedes sampling was not verified here and would need a run to settle. The
   prompt itself allowed this ordering ("add the concrete PyAutoArray guard
   first and add a companion AutoLens / analysis guard where the prior model can
   be inspected"), so this is a possible residue, not a regression.
3. **Criterion 3 (allowed combinations still work) — MET.** Rectangular +
   `Constant`, adaptive + split, and rectangular + no regularization all have
   passing parametrized tests.
4. **Criterion 4 (low-level regression test) — MET in the form the fix took.**
   Because the capability is deliberately absent rather than repaired, the tests
   assert the *clear failure*; the test module says so explicitly. The prompt's
   "do not paper over this by clipping indices" instruction was honoured.

## Why it was missed

Two prompts described one surface. `rhayes_audit_validation_and_crashes.md` came
in through the audit and is tracked by `planned.md`, so it was updated when phase
1 shipped; this one came in separately from a user repro
(`z_help/jacob/HerBS-28…`) and, sitting in `draft/`, was graded by nothing. The
related `draft/feature/autoarray/regularization_jax_gradient_gaps.md` § 3 flagged
the same surface a third time and asked "merge at intake if so" — that merge is
now moot, and its leg 3 has been marked done in place.

## Original prompt
# Users keep combining `RectangularAdaptDensity` meshes with `ConstantSplit`

Type: feature
Target: PyAutoArray
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

Users keep combining `RectangularAdaptDensity` meshes with `ConstantSplit`
regularization in pixelized source models, for example:

```python
pixelization = af.Model(
    al.Pixelization,
    mesh=af.Model(al.mesh.RectangularAdaptDensity, shape=(28, 28)),
    regularization=al.reg.ConstantSplit,
)
```

This must be flagged as an error before the fit runs. The combination is
currently invalid and can produce a pathological all-zero pixelized source in
the output products instead of failing clearly.

Concrete repro:

- Data/script context: `@z_help/jacob/HerBS-28.ms.shifted_fits/jax_modelling_template.py`
- Verbatim capped reproduction: `@z_help/jacob/HerBS-28.ms.shifted_fits/jax_modelling_template_verbatim_nlike1000.py`
- Pixelization output path from the repro:
  `output/interferometer/verbatim_nlike1000/pixelization/01c465702e769ad81c9c0e35b3d232d0`

Observed behavior from that run:

```text
source_plane_images.fits HDU 0: sum_abs=0.0 nonzero=0
source_plane_images.fits HDU 1: sum_abs=0.0 nonzero=0
fit_dirty_images.fits DIRTY_MODEL_IMAGE: sum_abs=0.0 nonzero=0
Maximum Log Likelihood = -12395933.858
```

Rebuilding the reported max-likelihood fit eagerly and accessing the inversion
reconstruction crashes in the split regularization path:

```text
IndexError: index 4 is out of bounds for axis 0 with size 4
```

The exception occurs in:

```text
@PyAutoArray/autoarray/inversion/regularization/regularization_util.py
reg_split_np_from()
```

called from:

```text
@PyAutoArray/autoarray/inversion/regularization/constant_split.py
ConstantSplit.regularization_matrix_from()
```

Root cause:

`ConstantSplit` assumes split-point interpolation rows have enough padded
mapping slots to append the parent pixel when the parent pixel is not already
present. With `RectangularAdaptDensity`, the split mappings can have only four
slots. If all four are already occupied and the parent pixel is absent,
`reg_split_np_from()` tries to write to slot `j + 1 == 4`, which is out of
bounds for an array with size 4. In JAX/vectorized modeling this can surface as
a silently bad inversion / zero source output rather than a clear exception.

Desired fix:

Add an explicit validation guard which rejects this unsupported configuration
early, with an error message that tells users what to do instead.

The guard should catch both concrete and model-composition forms:

```python
al.Pixelization(
    mesh=al.mesh.RectangularAdaptDensity(...),
    regularization=al.reg.ConstantSplit(...),
)
```

and:

```python
af.Model(
    al.Pixelization,
    mesh=af.Model(al.mesh.RectangularAdaptDensity, ...),
    regularization=al.reg.ConstantSplit,
)
```

Suggested error text:

```text
ConstantSplit regularization is not supported with RectangularAdaptDensity
meshes. This combination can produce invalid split regularization stencils and
all-zero pixelized source outputs. Use al.reg.Constant with
RectangularAdaptDensity, or use ConstantSplit with a Delaunay mesh.
```

Likely implementation locations to assess:

- `@PyAutoArray/autoarray/inversion/pixelization.py` if concrete
  `Pixelization` construction can validate mesh / regularization types.
- The inversion / mapper construction path if concrete construction is too
  early or incomplete.
- The AutoFit model-analysis pre-fit validation path may be needed to catch
  `af.Model(al.Pixelization, ...)` before sampling begins. If the validation
  naturally belongs outside PyAutoArray for `af.Model` objects, add the concrete
  PyAutoArray guard first and add a companion AutoLens / analysis guard where
  the prior model can be inspected.

Verification:

1. Add unit tests for concrete `Pixelization` construction or first use:
   `RectangularAdaptDensity + ConstantSplit` must raise the clear error.
2. Add a model-composition test, or an analysis pre-fit test, showing that
   `af.Model(al.Pixelization, mesh=af.Model(al.mesh.RectangularAdaptDensity),
   regularization=al.reg.ConstantSplit)` fails before Nautilus starts.
3. Confirm allowed combinations still work:
   - `RectangularAdaptDensity + Constant`
   - `Delaunay + ConstantSplit`
4. If touching the split regularization utility itself, add a low-level
   regression test for a split mapping row where the parent pixel is absent and
   all four slots are occupied, so the code cannot silently write out of bounds
   or produce invalid stencils.

Do not paper over this by clipping indices or returning an all-zero
reconstruction. This should be a hard, user-facing configuration error until
the split-regularization stencil code is redesigned to support rectangular
adaptive meshes.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
