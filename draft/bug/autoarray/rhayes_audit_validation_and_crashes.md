# @rhayes777's 2026-05-23 API audit — all 16 findings re-verified, still reproduce

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
- @PyAutoGalaxy
- @PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

## Why this exists

Richard Hayes (@rhayes777 — a **PyAutoFit author**, not an outside user) filed five
detailed issues on 2026-05-23 while auditing released `2026.5.21.1` against the
documented public API. Each carries reproducible snippets and environment info.

**They sat for 66 days with zero comments on any of them.** Surfaced by the
2026-07-27 `/wake_up` community scan; replied to on 2026-07-28.

Every claim was **re-run against current `main`** (PyAutoArray@616e8b4c,
PyAutoGalaxy@f0b65f39, PyAutoLens@6567b3b1c — all clean, zero ahead/behind).
**All 16 still reproduce** — nothing has been fixed by two months of intervening
work. Evidence below so this does not need re-deriving.

## The five issues

| Issue | Claims | Verified |
|---|---|---|
| [PyAutoArray#332](https://github.com/PyAutoLabs/PyAutoArray/issues/332) | Delaunay + KNNBarycentric `FitImaging` error; `ConstantSplit` broken on `RectangularUniform` | 3/3 reproduce — **but see the correction below** |
| [PyAutoArray#333](https://github.com/PyAutoLabs/PyAutoArray/issues/333) | B6, B7, B8, B5, B13 — input validation | 5/5 reproduce |
| [PyAutoGalaxy#440](https://github.com/PyAutoLabs/PyAutoGalaxy/issues/440) | B9, B10, B11, B12 — profile validation | 4/4 reproduce |
| [PyAutoLens#531](https://github.com/PyAutoLabs/PyAutoLens/issues/531) | `PointSolver.solve` AxisError + IndexError | 2/2 reproduce |
| [PyAutoLens#532](https://github.com/PyAutoLabs/PyAutoLens/issues/532) | B4 + Bonus — `Tracer` validation | 2/2 reproduce |

## ⚠️ CORRECTION to the 2026-07-27 reading of #332

**An earlier revision of this prompt recorded #332 part 1 as "Delaunay and
KNNBarycentric are unusable in a released wheel". That is FALSE.** It was carried
over from the reporter's headline without testing the other branch. Verified
2026-07-28:

```
Delaunay(pixels=100)       + Constant + adapt_images  ->  log_evidence 5084.7513   OK
KNNBarycentric(pixels=100) + Constant + adapt_images  ->  log_evidence 5211.7226   OK
Delaunay(pixels=100)       + Constant, NO adapt       ->  AttributeError 'NoneType'
Delaunay(pixels=100)       + ConstantSplit + adapt    ->  log_evidence 5096.4420   OK
RectangularUniform(15,15)  + ConstantSplit            ->  AttributeError            BROKEN
```

Both adaptive meshes **work correctly**. They require an image-plane mesh grid
supplied via:

```python
adapt_images = al.AdaptImages(
    galaxy_image_plane_mesh_grid_dict={source: image_plane_mesh_grid}
)
fit = al.FitImaging(dataset=dataset, tracer=tracer, adapt_images=adapt_images)
```

which is the idiom at `autolens_workspace/scripts/imaging/features/pixelization/delaunay.py:246`.
Omitting it leaves the grid `None` three frames above the failure site.

**The real defect is the error, not the mesh:** a missing required precondition
surfaces as `AttributeError: 'NoneType' object has no attribute 'array'` from deep
inside `border_relocator.py`, naming nothing the caller controls.

**This changes the fix direction.** The previous revision instructed: *"Any fix must
land with a regression test built the reporter's way, not the examples' way."*
Followed literally that would assert bare construction **succeeds** — enshrining the
wrong expectation. The correct fix is the opposite: bare construction must **fail
fast and legibly**, naming `adapt_images`. The regression test asserts a clear
`ValueError`/`TypeError` is raised, *not* that a fit is produced.

## Verification output (2026-07-28, libraries at the SHAs above)

```
[REPRO] B6    Array2D pixel_scales   0.0 accepted; -0.1 accepted; nan accepted
              (ps=0 then ZeroDivisionError on first derive_grid)
[REPRO] B7    Mask2D.circular_annular(inner=0.8, outer=0.3)   pixels_in_mask = 0
[REPRO] B8    Grid2D.uniform((0,0)) and ((0,5))               shape_slim = 0
[REPRO] B5    Imaging(data 10x10, noise_map 5x5)              built, shape_native (10,10)
[REPRO] B13   reg.Constant(coefficient=-1.0)                  accepted, stored as -1.0
[REPRO] B9    NFW(scale_radius=0.0)                           NaN count 3200 of 3200
[REPRO] B10   Isothermal(ell_comps=(0,0)) vs IsothermalSph    max|diff| = 2.357e-06
[REPRO] B11   Sersic(sersic_index=0.0)                        ZeroDivisionError
[REPRO] B12   Sersic(ell_comps=(2.0,0.0))                     finite image, sum 1296.0498
[REPRO] B4    Tracer(galaxies="not a list")                   constructed; later
                 AttributeError: 'str' object has no attribute 'redshift'
[REPRO] Bonus z_lens=1.0 > z_source=0.5  image sum 64.97;  redshift=-0.5 and 1e-12 accepted
[REPRO] 531-1 source outside caustic, precision 0.001         numpy AxisError
[REPRO] 531-2 source inside caustic, precision 0.1            IndexError
              (control: same source at precision 0.001 returns 4 images)
[REPRO] 332-1 Delaunay + Constant, NO adapt_images   AttributeError: 'NoneType' has no 'array'
                 autoarray/inversion/mesh/border_relocator.py  (~line 446-450)
[REPRO] 332-2 KNNBarycentric + Constant, NO adapt_images        same site
[REPRO] 332-3 RectangularUniform + ConstantSplit    AttributeError:
                 'InterpolatorRectangularUniform' has no '_mappings_sizes_weights_split'
                 autoarray/inversion/regularization/constant_split.py:67
[OK]    ctl   RectangularUniform + Constant                   log_evidence = 4779.4288
[OK]    ctl   Delaunay / KNNBarycentric WITH adapt_images      fit cleanly (see above)
```

## Sharpened finding on B13 (not in the original report)

`constant.py:43` does `regularization_coefficient = coefficient * coefficient`,
which is why `log_evidence` is identical for `+1.0` and `-1.0`. **But
`regularization_weights_from` (`constant.py:127`) returns the raw, un-squared
`self.coefficient`** — so a negative coefficient does leak negative regularization
weights into every consumer of that method. A negative value is not inert. This
strengthens the case for rejecting it at construction.

## The work splits into five classes

**1. Genuine crash bugs (start here — real user impact, no workaround)**
- **`Split` regularization on rectangular meshes (#332-3).** DESIGN INTENT (confirmed
  by @Jammy2211 2026-07-28): **rectangular does not support Split.** The fix is a
  clear "unsupported" exception, NOT implementing the missing capability. Scope is
  **9 combinations in 2 failure modes**, not the 1 reported:
  - `RectangularUniform` → `AttributeError` (`InterpolatorRectangularUniform` has no
    `_mappings_sizes_weights_split`)
  - `RectangularAdaptDensity` / `RectangularAdaptImage` → `IndexError: index 4 is out
    of bounds` (`InterpolatorRectangular._mappings_sizes_weights_split` at
    `rectangular.py:460` is a pass-through returning `self._mappings_sizes_weights`;
    its comment claiming split "reuses the same mappings" is FALSE — `reg_split_from`
    expects the split-cross structure and crashes one frame later). DELETE it.
  - x3 regularizations: `constant_split.py:67`, `adapt_split.py:104`,
    `adapt_split_zeroth.py:105`
  - Control: `Delaunay + ConstantSplit` works (`log_evidence 5096.4420`).
- `PointSolver` single-image source → `AxisError` (#531-1). Should return the one
  image it finds.
- `PointSolver` loose `pixel_scale_precision` → `IndexError` (#531-2). Should raise
  a clear error naming `pixel_scale_precision`.

**2. Constructor validation (one mechanical sweep, 9 findings)**
B5, B6, B7, B8, B13, B9, B11, B12, B4. All are "raise a clear `ValueError` at
construction instead of a confusing NumPy/numba traceback three calls later".
**Decide where the shared `_validate_*` helper lives before writing it** (PyAutoArray
is the natural floor — Galaxy and Lens both depend on it) or the three repos get
inconsistent messages.

**Constraint:** these constructors sit on JAX-traced paths. Guards must stay correct
under tracing and cost nothing when traced — do not use Python `if` on values that
may be tracers without checking.

**3. Error-message quality (1 finding)**
The `adapt_images` precondition (#332-1, #332-2). Either the mesh wires the grid up
itself, or construction fails immediately naming `adapt_images`. Regression test
asserts the *clear failure*, per the correction above.

**4. Warning-only judgement call (1 finding) — HELD**
`z_lens > z_source` (#532 Bonus). Multi-plane genuinely supports geometries that
look wrong under two-plane naming, so this should **warn**, not raise. A negative
redshift can raise outright. **In the posted reply we asked @rhayes777 whether even
a warning would be noise in a real multi-plane setup — hold this sub-item until he
answers.** Everything else is unblocked.

**5. Regression test only (1 finding)**
B10, the `2.357e-06` Isothermal/IsothermalSph difference at the degenerate point.
Pin at an explicit tolerance. **Do not chase bit-identity** between the elliptical
and spherical evaluation paths.

## State as of 2026-07-28

- **All five replies are POSTED** (this supersedes the 2026-07-27 note that they
  were drafted but withheld):
  - PyAutoArray#333 — `#issuecomment-5105855009`
  - PyAutoArray#332 — `#issuecomment-5105855203`
  - PyAutoGalaxy#440 — `#issuecomment-5105855357`
  - PyAutoLens#531 — `#issuecomment-5105855611`
  - PyAutoLens#532 — `#issuecomment-5105855829`
- **The #332 reply publicly corrects the reporter's headline** while crediting the
  underlying finding. Keep that framing consistent in any follow-up.
- **Decided by the human 2026-07-28: we implement in-house.** @rhayes777's "Happy to
  PR if useful" offer was declined warmly in all replies, on the grounds that the
  constructors are JAX-traced hot paths. This supersedes the earlier
  "agree the helper shape with him first" instruction — do not route to
  `start_dev_for_user`.
- **All five replies promise a tracking issue.** That is a public commitment with a
  clock on it.

## Verification recipe

Re-run any claim straight from the issue bodies; they are self-contained. Gotchas:

- The PSF constructor is `al.Convolver.from_gaussian` (**not** `al.Kernel2D` — the
  PyAuto API gate correctly rejects that; `Kernel2D` no longer exists).
- Run from a workspace root with `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1`,
  `NUMBA_CACHE_DIR=/tmp/numba_cache`, `MPLCONFIGDIR=/tmp/matplotlib`,
  `PYAUTO_DISABLE_JAX=1`.
- **Always test the `adapt_images` branch as well as the bare one** — testing only
  the reporter's construction is what produced the wrong reading on 2026-07-27.

---

## Phase 1 completion record — 2026-07-28

**Shipped:** PyAutoArray#417 (`9411904d`) + PyAutoLens#662 (`2a3f1a63`), both merged.
PyAutoArray#416 (phase-1 tracker) closed 2026-07-29; PyAutoLens#531 closed.
Epic PyAutoArray#415 stays **open** for phases 2-4, as do #332, #333,
PyAutoGalaxy#440 and PyAutoLens#532.

**Delivered (3 of 16 findings — the crash class, no workaround):**

- `Split` regularization on any rectangular mesh now raises an explicit "unsupported"
  exception at construction, covering all **9** mesh x regularization combinations, not
  the 1 reported. The false pass-through at `rectangular.py:460` — which claimed split
  "reuses the same mappings" and produced the second (`IndexError`) failure mode on
  `RectangularAdaptDensity` / `RectangularAdaptImage` — was deleted, not patched.
- `PointSolver.solve` returns the single image it finds when the source is outside the
  caustic, instead of raising numpy `AxisError`.
- `PointSolver.solve` raises a clear error naming `pixel_scale_precision` when the
  precision is too coarse to resolve any image, instead of `IndexError`.
- Regression tests built from the reporter's own snippets; `Delaunay` + `ConstantSplit`
  (`log_evidence 5096.4420`) kept as the control that Split itself is not broken.

**Validation:** smoke clean across 6 workspaces, **zero regressions**. The 5
`jax_likelihood` failures observed during the run were baselined sequentially against
unmodified `main`, confirmed pre-existing, and fixed separately via
autolens_workspace_test#231 / PR#232.

**Worktree released:** `~/Code/PyAutoLabs-wt/api-validation-and-crash-fixes` removed;
`feature/api-validation-and-crash-fixes` deleted in PyAutoArray and PyAutoLens, local and
remote. Nothing from this campaign holds a repo claim.

**Remaining (this prompt returns to `draft/` until phase 2 is started):**

| Phase | Scope | Covers | Blocker |
|---|---|---|---|
| 2 | 9 constructor-validation guards | #333 (B5-B8, B13), PyAutoGalaxy#440 (B9, B11, B12) | needs the shared `_validate_*` home decision — PyAutoArray is the natural floor; PyAutoGalaxy not yet claimed |
| 3 | `adapt_images` precondition error legibility + B10 tolerance regression test | #332, PyAutoGalaxy#440 (B10) | none |
| 4 | `z_lens > z_source` warning | #532 | HELD on @rhayes777's answer, asked on #532 2026-07-28 |

Phase 2 carries two binding constraints from phase 1: constructors are **JAX-traced**, so
no Python `if` on a possible tracer; and the negative-redshift half of #532 is *not*
blocked on the phase-4 question — it rides with phase 2.

---

## Split into per-issue prompts — 2026-08-09

Phases 2-3 above spanned three repos and four issues, which is more than one PR
and so violated *one prompt = one task = one PR*. They were split into four
issue-shaped prompts, one per still-open issue. **This file is now the campaign
record, not a work item** — do not `$start-dev` it; start one of the four.

| Prompt | Issue | Phase | Blocker |
|---|---|---|---|
| `draft/bug/autoarray/rhayes_333_input_validation_guards.md` | PyAutoArray#333 | 2 | none — **anchor: owns the shared `_validate_*` home decision** |
| `draft/bug/autogalaxy/rhayes_440_profile_validation_guards.md` | PyAutoGalaxy#440 | 2 + B10 of 3 | the #333 helper |
| `draft/bug/autolens/rhayes_532_tracer_validation_guards.md` | PyAutoLens#532 | 2 (B4 + negative redshift) | the #333 helper |
| `draft/bug/autoarray/rhayes_332_adapt_images_precondition_error.md` | PyAutoArray#332 | 3 | none — can start immediately |

**Ship #333 first.** The other two validation prompts import its helper and
message template; started out of order, the three repos emit inconsistent errors
for the same class of mistake, which is the failure the phase-2 note warned about.
#332 is independent of all three and can run in parallel.

**Phase 4 stays HELD and is deliberately in none of the four** — the
`z_lens > z_source` warning waits on @rhayes777's answer to the question put on
#532 on 2026-07-28, still unanswered as of 2026-08-09. The #532 prompt carries a
control test pinning today's permissive behaviour so phase 4 cannot regress it
silently.
