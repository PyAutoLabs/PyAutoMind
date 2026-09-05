# magnification latent is inf/0.0 for any pixelized source: Galaxy.image_2d_from returns zeros for a Pixelization-only galaxy

Type: bug
Target: autolens
Repos:
- PyAutoLens
- PyAutoGalaxy
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- pixelization
- latent
Difficulty: small-medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: euclid-dr1-prep
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-09-04

## The finding

`autolens/analysis/latent.py::magnification` (`PyAutoLens/autolens/analysis/latent.py:218-229`)
is `total_lensed_source_flux_mujy / total_source_flux_mujy`. The denominator,
`total_source_flux` (`:121-139`, via `total_source_flux_mujy` at `:189-215`), calls
`tracer.galaxies[-1].image_2d_from(grid=fit.dataset.grids.lp)` on
`fit.tracer_linear_light_profiles_to_light_profiles`. `Galaxy.image_2d_from`
(`PyAutoGalaxy/autogalaxy/galaxy/galaxy.py:245-278`) returns `xp.zeros((grid.shape[0],))`
at `:278` whenever the galaxy has no non-linear `LightProfile` — and a `Pixelization` is
not a `LightProfile`. So for any pixelized source the source flux is a hard `0.0`, then
`ab_mag_via_flux_from(0.0, magzero=25) = inf` and `flux_mujy_via_ab_mag_from(inf) = 0.0`
exactly, so `magnification = lensed / 0.0 = +inf`. PyAutoFit's latent writer
(`autofit/non_linear/analysis/latent.py:258-263`, the `np.isfinite(all_values[:, i]).any()`
guard) then drops the whole `magnification` column.

Confirmed empirically, not only by reading. A real `al.FitImaging` built on the
pipeline's shipped `dataset/simulated/euclid_dr1_like` (magzero 24.6) with the truth lens
from `truth.json` and a Delaunay source with `zeroed_pixels=30` — the `vis_pix` /
`full_model` configuration — gives `total_source_flux = 0.0`,
`total_source_flux_mujy = 0.0`, `magnification = inf`. The Sersic control (the `vis_lp`
configuration) on the same fit gives `total_source_flux = 0.8679858287`,
`total_source_flux_mujy = 0.4555254383` and `magnification = 15.146299`, reproducing
`truth.json`'s `15.146298766165936` **bit-for-bit** — so the latent's *definition* is
sound and only the pixelized-source route is broken.

Production evidence: 9/9 archived `initial_lens_model/vis_pix` `latent_summary.json`
files record `magnification = 0.0` alongside `total_source_flux = 0.0` — a meaningless
sentinel that a downstream catalogue would silently ingest — while the matching
`initial_lens_model/vis_lp` results record real values (6.2727, 10.0782, 18.4297, …). The
`vis_pix` key set is otherwise complete (9 keys, same as `vis_lp`), so the NaN-drop
signature does not fire on those particular files; absence of the key is the signature
under current code and `0.0` under whatever version produced the archive. Either way the
Euclid pixelized stages have no magnification.

Note this defect is **independent** of the Delaunay area defect, now shipped as
`complete/2026/09/delaunay-dual-area-magnification.md` (PyAutoArray#524, PR #525): the latent
never touches `areas_for_magnification` at all, and neither bug masks the other.

## Impact

Every Euclid pixelized stage — `vis_pix` and `full_model` — has no magnification.
`catalogue/scripts/magnitudes.py` maps `latent.magnification` into the catalogue at
`:305`, so the sentinel propagates. The docstring of
`scripts/tools/diagnose_latent_vis_pix.py`, which claims that the library latents not
depending on the source reconstruction (`magnification` among them) are "identical
between the two stages", is **false** — magnification depends on the source *model*,
which is exactly what changes at `vis_pix`, and the production numbers (6.27/10.08/18.43
vs 0.0/0.0/0.0) disprove it directly. That docstring must be corrected.

## Proposed fix (for the implementer to verify, not to take on trust)

Preferred: for a pixelized source, define the source-plane flux as the reconstruction
integrated with the mesh's **exact quadrature areas** — the barycentric dual areas for
Delaunay (see the sibling prompt above), the transformed cell areas for rectangular
meshes (whose own correctness is an open lead in the cluster epic's
`draft/test/workspaces/mesh_magnification_correctness.md`) — so that `magnification` =
image-plane mapped flux / source-plane integrated flux.

Alternative, if that is judged out of scope for the latent layer: make the latent return
**NaN explicitly** for pixelized sources, and stop the `0.0` sentinel from reaching the
catalogue. What must not survive is a `0.0` that reads as a measurement.

Tests: a unit test that a pixelization-only galaxy's `magnification` latent is finite (or
explicitly NaN, per whichever route is chosen), and a Euclid pipeline test-mode assertion
on the `vis_pix` latent keys so a silently-dropped or sentinel column fails loudly.

## Provenance

Proven by the euclid-dr1-prep phase 8 audit, PyAutoArray#522 (audit posted on the issue),
scripts `part3_latent_reach.py`, `part3b_fit_latent.py`.

## Gate note

This directly affects Cortex phase 4's witness ("catalogue numerics match the 20260623
reference") for the `vis_pix` magnification column, and Mind phase 9's magnification
layer. Neither can be scored on the `vis_pix` magnification until this is fixed.

## Implementation design (architect, 2026-09-04 — approved plan; execute from this)

**Sequence:** the PyAutoArray dual-area fix is **merged** (2026-09-05, PyAutoArray#524 / PR #525,
record `complete/2026/09/delaunay-dual-area-magnification.md`), so the Delaunay accuracy test may
be written against `main` in-worktree. `/start_dev` this prompt → task
`pixelized-source-magnification-latent`; classification **both**: library PyAutoLens first
(PyAutoGalaxy read-only), workspace follow-up in `euclid_strong_lens_modeling_pipeline` behind the
library-first gate.

**Facts (do not re-derive):** latents run inside a per-sample JAX jit (`LatentLens.BATCH_MODE =
"jit"`, `autolens/analysis/latent.py:304-336`, `xp = analysis._xp`) — new code must be trace-safe.
`total_lensed_source_flux` (`:106-115`) reads `fit.galaxy_image_dict[fit.tracer.galaxies[-1]]`, which
already includes the inversion's mapped image — the numerator is sound. `total_source_flux`
(`:121-139`) / `total_source_flux_mujy` (`:189-215`) call
`fit.tracer_linear_light_profiles_to_light_profiles.galaxies[-1].image_2d_from(...)`, zeros for a
pixelization-only galaxy (`autogalaxy/galaxy/galaxy.py:278`). Per-mapper reconstructions:
`fit.inversion.reconstruction_dict` (`autoarray/inversion/inversion/abstract.py:667`); mapper →
galaxy: `fit.tracer_to_inversion.mapper_galaxy_dict` (`autolens/lens/to_inversion.py:394`;
`fit.tracer_to_inversion` at `fit_imaging.py:184`). **Caveat:** the converted tracer's galaxies are
new objects — key lookups must use whichever galaxy object actually keys `mapper_galaxy_dict`
(verify against `galaxy_image_dict`'s keys).

**Library changes (PyAutoLens):**
1. `autolens/analysis/latent.py` — add `_pixelized_source_flux(fit, xp)`: `inv = fit.inversion`;
   None or no `Pixelization` on the source galaxy → `0.0`; else for each `(mapper, gal)` in
   `fit.tracer_to_inversion.mapper_galaxy_dict.items()` belonging to the source galaxy,
   `xp.sum(inv.reconstruction_dict[mapper] * mapper.mesh_geometry.areas_for_magnification)`. A mesh
   geometry with no `areas_for_magnification` (DelaunayNN, KNN, KNNBarycentric) → `xp.nan` with a
   one-time-per-process warning (no silent zero). `total_source_flux` and `total_source_flux_mujy` =
   light-profile flux (existing path) + pixelized flux; `magnification` unchanged in form.
   Trace-safe: `reconstruction_dict` values are `xp` arrays; Delaunay dual areas are `xp` after the
   autoarray fix; rectangular `areas_transformed` already is.
2. Tests in `test_autolens/analysis/` (existing latent test file, else `test_latent.py`): FitImaging
   with a Delaunay pixelized source → `magnification` finite and equal to
   `Σ galaxy_image[-1] / Σ reconstruction·areas`; same with `RectangularBilinearAdaptDensity`; linear
   light profile + pixelization sums both; light-profile-only fit numerically unchanged; a KNN mesh →
   NaN. Numpy path (JAX only if the file already has a JAX pattern).
3. `ship_library` → PR-open. API Changes: Changed behaviour — `total_source_flux`,
   `total_source_flux_mujy`, `magnification` now include pixelized sources (were 0 / inf). The PR body
   states that end-to-end Delaunay accuracy needs the autoarray fix merged; these tests assert
   internal consistency and hold on either PyAutoArray.

**Workspace follow-up (euclid_strong_lens_modeling_pipeline, `/start_workspace` → `ship_workspace`):**
4. `scripts/tools/diagnose_latent_vis_pix.py:42` docstring — `magnification` is NOT stage-invariant;
   state the new definition.
5. `tests/test_compute_latent_variable.py` (or `test_latent_run_level.py`) — assert the `vis_pix`
   Delaunay stage's `magnification` is present and finite when `LatentEuclid.variables` is evaluated
   directly on a test-mode Delaunay fit of the committed `dataset/simulated/euclid_dr1_like` (a direct
   call — test-mode CI skips latents at every level, so run-level summaries can only be structural).
6. Ledger note for Mind phase 9 / Cortex phase 4: archived `vis_pix` rows carry a `0.0` sentinel and
   must be re-derived; `catalogue/scripts/magnitudes.py:305` ingests the latent unchanged.

**Acceptance (human, after both merges):** the audit's `part3b_fit_latent.py` construction (Delaunay
fit on `euclid_dr1_like`, magzero 24.6) reports a finite `magnification` close to the Sersic
control's 15.146; record it on the issue.


<!-- formalised by the Intake (Conception) Agent on 2026-09-04 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/4974a870-2ecf-47c9-9592-6a344294c707/scratchpad/raw_prompt2.md -->
