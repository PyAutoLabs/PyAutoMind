## slam-adapt-inversion-cascade
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/300
- completed: 2026-07-21
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/302, https://github.com/PyAutoLabs/HowToLens/pull/40
- summary: Fixed two distinct pixelized-SLaM root causes (verified green under CI smoke env; run_smoke 9/9 + 6/6). (1) Double-Einstein-ring (imaging+group): source_pix_1_source_1 pixelizes source_1 with adaptive al.reg.Adapt but the stitched galaxy_name_image_dict omitted source_1 -> adapt_data=None crash; fixed by seeding source_1's adapt image from its light-profile model image in source_lp_result_2 (which already fits source_1 as an MGE). (2) imaging/features/pixelization/slam: RectangularAdaptImage mesh + al.reg.AdaptSplit is invalid (Split reg only works on irregular Delaunay/Voronoi; rectangular interpolator's _mappings_sizes_weights_split is a non-split stub -> AdaptSplit's pixels=len/4 gave 210x210 reg vs 786x786 curvature -> broadcast TypeError); fixed by swapping to al.reg.Adapt. Cleared now-green NEEDS_FIX markers across both repos' no_run.yaml (both double-rings, pix/slam, imaging delaunay) + 6 stale/dead HowToLens markers. SPLIT OUT to new draft prompts: multi-wavelength SersicCore alpha=0 ZeroDivisionError (bug/autogalaxy/sersic_core_alpha_zero_division.md, unrelated) and interferometer delaunay non-PD FitException at analysis.py:182 (bug/autolens/interferometer_delaunay_nonpd_fitexception.md — folded-in note's "already green" claim was WRONG; kept marker, updated reason). Candidate PyAutoArray hardening follow-up: *Split reg should fail loudly on non-splittable meshes instead of a cryptic broadcast error. Did NOT bloat smoke_tests.txt (curated-subset rule). Merge pending human (both PRs open, pending-release).

## Original prompt

# SLaM / advanced-pipeline inversion+adapt-image cascade

Type: bug
Target: autolens
Repos:
- autolens_workspace
- HowToLens
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Parked cluster of advanced-pipeline SLaM fit failures (2026-07-20 sweep), reproduced and scoped on
clean main 2026-07-21. The multi-wavelength `SersicCore alpha=0` failure proved **unrelated** and was
split out to `bug/autogalaxy/sersic_core_alpha_zero_division.md`. This task covers the SLaM
inversion / adapt-image cascade only.

## Reproduction (clean main, PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1)

Two distinct signatures within the pixelized-SLaM cluster:

1. **double-Einstein-ring (imaging + group)** — `AttributeError: 'NoneType' object has no attribute
   'array'` at `PyAutoArray/.../inversion/mappers/abstract.py:476` (`self.adapt_data.array`), inside
   `pixel_signals_from` → adaptive-regularization weights. Occurs in phase `source_pix[1]_source_1`
   (imaging `slam.py:367`, group `slam.py:476`). **Same root cause in both scripts.**

2. **imaging/features/pixelization/slam** — `TypeError: add got incompatible shapes for broadcasting:
   (786, 786), (210, 210)` at `PyAutoArray/.../inversion/inversion/abstract.py:366`
   (`curvature_matrix + regularization_matrix`). A curvature/regularization **size mismatch** — needs
   phase-1 diagnosis to decide real-pipeline-bug vs synthetic-samples/test-mode artifact.

## Root cause (double-ring, confirmed real — not a test-mode artifact)

The SLaM setup uses `regularization_init = al.reg.Adapt` (adaptive regularization → needs a per-galaxy
adapt image). `source_pix_1_source_1` pixelizes `source_1`, but its stitched `galaxy_name_image_dict`
carries only `lens` + `source_0`. `source_0` obtained its adapt image from an earlier light-profile
phase; `source_1` was only ever a bare redshift galaxy, so **no adapt image can exist for it yet** →
`AdaptImages` yields no entry for source_1 → the source_1 mapper's `adapt_data` is `None` → crash.

## Chosen fix direction (phase 2)

**Seed `source_1` an adapt image** for its first pixelized fit — supply source_1 an adapt image derived
from the current tracer's lensed source-plane model image before the fit, so adaptive regularization
has data to weight on. (Alternative considered and rejected at scoping: bootstrap with `Constant`
regularization for source_1's first pix fit then switch to `Adapt`.)

## Phasing

- **Phase 1 — diagnose:** confirm double-ring root cause end-to-end; diagnose the pixelization/slam
  (786 vs 210) mismatch — is it the same adapt/synthetic-samples gap, a real mesh-size mismatch, or a
  test-mode-only artifact? Determine whether any fix is library (PyAutoArray/PyAutoGalaxy) or
  workspace-only. Reconcile the HowToLens target: the parent note's HowToLens paths
  (`imaging/features/pixelization/slam`) do not exist — HowToLens uses a `chapter_N_*` layout; find the
  real pixelization tutorial equivalents.
- **Phase 2 — fix double-ring:** seed source_1 adapt image; re-run both double-ring scripts green in
  test mode.
- **Phase 3 — fix pixelization/slam** per phase-1 verdict; update HowToLens equivalent.

Affected (remove NEEDS_FIX once green):
- autolens_workspace: `imaging/features/advanced/double_einstein_ring/slam`,
  `group/features/advanced/double_einstein_ring/slam`, `imaging/features/pixelization/slam`
- HowToLens: pixelization tutorial equivalent (verify real path in phase 1)

Split out (separate prompt): `multi/features/wavelength_dependence/modeling` → SersicCore alpha=0.

## Folded in: Delaunay NEEDS_FIX cleanup (from #301, closed 2026-07-21)

The parked 2026-04-10 **Delaunay** cluster (former `bug/autoarray/delaunay_pixelization_fit_failures.md`,
issue #301) is the same pixelization cluster and edits the same `no_run.yaml`, so it is folded here.
Reproduction on clean main (2026-07-21, `TEST_MODE=2 SMALL_DATASETS=1 DISABLE_JAX=1`) **overturned its
premise** — the bugs are already fixed (interferometer non-PD numpy path `PyAutoLens#607`, zero-fill
extrapolate, potential-correction port); no PyAutoArray change:

- `imaging/features/pixelization/delaunay.py` → exit 0 (~19s) — `FitException` gone
- `interferometer/features/pixelization/delaunay.py` → exit 0 (~34s) — `(2,2) vs (1032,1032)` broadcast gone
- HowToLens `chapter_4_pixelizations/tutorial_7_adaptive_pixelization.py` → exit 0

Cleanup checklist (do in this task's PR set):
- autolens_workspace `config/build/no_run.yaml` — remove the `imaging/features/pixelization/delaunay`
  and `interferometer/features/pixelization/delaunay` NEEDS_FIX entries.
- HowToLens `config/build/no_run.yaml` — remove the two `.../features/pixelization/delaunay` entries
  (dead paths; HowToLens has no `features/` layout).
- autolens_workspace `smoke_tests.txt` — add both delaunay scripts (regression guard; interferometer
  ~34s, heaviest entry).

## Folded in (2): HowToLens practicalities + mappers NEEDS_FIX cleanup

The parked 2026-04-10 HowToLens breakages (draft
`bug/howtolens/tutorial_repair_practicalities_mappers.md`) edit the same HowToLens
`no_run.yaml`, so they are folded here. Reproduction on clean main (2026-07-21) **overturned their
premise** — both tutorials already run green; no script/library change:

- `chapter_2_lens_modeling/tutorial_2_practicalities.py` → exit 0. The "missing ~80 lines of imports"
  was already restored by PR #14 ("restore lost setup scaffolding"); `import autofit as af` is present
  (line 95). The `NameError: af` NEEDS_FIX is stale.
- `chapter_4_pixelizations/tutorial_2_mappers.py` → exit 0 with fresh full-size data (annular mask →
  1212 image-pixels, healthy mapper). The historical `zero-size array / empty mapper` came from a
  stale 16×16 dataset reused via the `if not dataset_path.exists()` guard (line 47) giving 4 pixels;
  the `howtolens/` `PYAUTO_SMALL_DATASETS` override (unsets it → full-size simulate) plus library
  hardening already resolved it — even a 4-pixel mapper now exits 0. Marker is stale.

Cleanup checklist (do in this task's HowToLens PR — same `no_run.yaml` edit):
- HowToLens `config/build/no_run.yaml` — remove the two NEEDS_FIX entries
  `howtolens/chapter_2_lens_modeling/tutorial_2_practicalities` and
  `howtolens/chapter_4_pixelizations/tutorial_2_mappers`.
- Regenerate notebooks + navigator catalogue (the task already runs the howtolens generate step).

Out of scope (separate follow-up prompt): `tutorial_2_mappers` self-flags "VISUALS SLIGHTLY BUGGY"
(line 10) — it computes `indexes`/`pix_indexes` (lines 166/182/205/265) but never passes them to the
plot calls, so image↔source mappings aren't highlighted. Pedagogical-quality bug, not a run failure.
