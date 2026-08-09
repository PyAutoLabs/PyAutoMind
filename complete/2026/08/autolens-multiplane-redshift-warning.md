Phase 4 — the last open item of the @rhayes777 API audit. **The campaign is complete
and epic PyAutoArray#415 is closed.**

**Shipped:** PyAutoLens#697, squash-merged `13a4655` 2026-08-09.

## The decision

@rhayes777 was asked on PyAutoLens#532 (2026-07-28) whether warning on
`z_lens > z_source` would be noise in a real multi-plane setup. **No answer after 12
days.** The human directed closure and chose to implement the warning behind its own
**filterable category**, `MultiPlaneRedshiftWarning`:

```python
warnings.filterwarnings("ignore", category=MultiPlaneRedshiftWarning)
```

That settles the noise question by construction rather than by guessing — a user for
whom it is noise silences exactly it and nothing else.

**It warns, never raises.** Multi-plane genuinely supports geometries that look
inverted under two-plane naming.

## The rule

Fires only when **no lensable thing lies behind any mass**, across more than one
redshift plane — i.e. nothing in the tracer can be lensed at all. Mass at z=1.0 with
light at both 0.5 and 1.5 stays quiet, because some of its light is genuinely lensed.

## Three false-positive classes — the real work of this task

The first implementation counted only `LightProfile` and fired in **~10 existing
legitimate tests**. Each is now regression-tested:

| Class | Why it broke |
|---|---|
| Pixelized source | carries no `LightProfile` — and pixelized source modelling is core PyAutoLens |
| Point source | carries neither light profile nor pixelization |
| Empty placeholder galaxy | `al.Galaxy(redshift=1.0)` with nothing in it — a model mid-composition |

Resolved with `LENSABLE_CLS = (LightProfile, Pixelization, Point, PointSolved)` plus a
stand-down when a galaxy is entirely empty.

**Evidence:** suite warning count went 18 (baseline) → 44 (naive rule) → 18 (final),
with zero triggers outside its own regression module. That is the empirical answer to
"would a warning be noise": it would have been, and this is what stops it.

## A mistake worth recording

The first version referenced `ag.MassProfile`, which does not exist, inside a broad
`except (AttributeError, TypeError): return`. The exception was swallowed, the warning
never fired, and **the whole suite stayed green** — a passing suite proved nothing
because the feature was silently inert. Caught only by explicitly testing that the
*reported* case warns. The broad `except` was removed.

**Lesson: a guard that fails open needs a positive test that it fires, not just tests
that it stays quiet.**

## Validation

Full suite **532 passed / 1 skipped** (+13 on the branch), zero regressions, CI green
on 3.12/3.13/docs. Tracer-safe via the same `is_concrete_scalar` gate as the rest of
the campaign.

---

# Campaign closed — all four phases

| Phase | Issue(s) | PR |
|---|---|---|
| 1 | PyAutoArray#332 (part 2), PyAutoLens#531 | PyAutoArray#417, PyAutoLens#662 |
| 2 | PyAutoArray#333, PyAutoGalaxy#440, PyAutoLens#532 | PyAutoArray#440, PyAutoGalaxy#566, PyAutoLens#696 |
| 3 | PyAutoArray#332 | PyAutoArray#442 |
| 4 | PyAutoLens#532 | PyAutoLens#697 |

All 16 findings addressed. All five reporter issues closed. Epic #415 closed. The
campaign prompt is archived to `complete/archive/epics/`.

## Shared artefact the campaign leaves behind

`autoarray/validate.py` — `is_concrete_scalar`, `validate_positive_finite`,
`validate_non_negative_finite`, `validate_pixel_scales`, `validate_shape_native`,
`validate_radii_ordered`. Message shape: name the parameter, state the rule, show the
value. Tracer-safe form: gate on `is_concrete_scalar`, pass non-concrete through.
PyAutoGalaxy adds only per-parameter explanations in `autogalaxy/profiles/validate.py`.
**Reuse this for any future guard in any of the three repos.**

---

# CORRECTION: the Ell/Sph potential finding was overstated

Earlier records from this campaign (the PyAutoGalaxy#566 PR body, the comment on
PyAutoGalaxy#440, and `planned.md`) said the `Isothermal(ell_comps=(0,0))` vs
`IsothermalSph` **potential** agrees only to `1.9e-03` relative, "three orders of
magnitude worse" than deflections, framed as a real accuracy defect. **Investigated
properly 2026-08-09; that framing is wrong in two ways.**

**1. The number was normalised misleadingly.** `1.9e-03` divided by the *global
maximum* potential. The worst single pixel actually disagrees by **7%** (`0.0707` vs
`0.0761`) — worse than reported.

**2. But it is not an accuracy defect — it is an over-sampling artefact at the
profile's singular centre.** Measured on a 40x40 grid at `pixel_scales=0.1`:

| `over_sample_size` | potential max\|diff\| | max local relative |
|---|---|---|
| 1 (off) | **3.2e-06** | 1.7e-06 |
| 4 (default) | 5.4e-03 | 7.1e-02 |

With over-sampling off the potential agrees to `3.2e-06` — the same order as the
deflections (`2.4e-06`). The whole discrepancy appears only under over-sampling and is
concentrated at the **central pixel**, where the isothermal profile is formally
singular. Over-sampling averages sub-pixel values across that cusp and the two forms
diverge there.

**Root cause of the benign ~1e-6 baseline** (this part stands): the elliptical form
clips `axis_ratio` to `0.99999` rather than exactly `1.0` — a numerical-stability
clamp — while `IsothermalSph` overrides `axis_ratio()` to a hard `1.0`. That
propagates into `einstein_radius_rescaled` (`0.5000025` vs `0.5`).

**Retracted:** the guess that this shares a root cause with
`draft/bug/autogalaxy/nfw_truncated_potential_accuracy.md` (MGE decomposition). It
does not — this has nothing to do with MGE.

**Still worth a prompt, for a narrower reason:** the `1e-2` tolerance pinned in
`test_autogalaxy/profiles/test_validate.py` papers over a 7% local disagreement at the
cusp, and the same over-sampling-at-a-singularity behaviour may affect other singular
profiles. Not filed yet.
