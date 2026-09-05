## pixelized-source-magnification-latent
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/726
- completed: 2026-09-05
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/727
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/728
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/51
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/727
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/728
- epic: euclid-dr1-prep (follow-up to phase 8; second of the audit's two defects)

Fixed the `magnification` latent for pixelized sources. `total_source_flux` /
`total_source_flux_mujy` read the source galaxy's `image_2d_from`, which is zeros for a
galaxy whose only light model is a `Pixelization`, so every pixelized fit had
`total_source_flux = 0.0` and `magnification = inf` (dropped by PyAutoFit's NaN guard, or
archived as a `0.0` sentinel in 9/9 Euclid `vis_pix` results). The Sersic control on the
same fit reproduced `truth.json` bit-for-bit, so only the pixelized route was broken.

## What shipped

- **PyAutoLens #727** (`609338f`, merge `633c8e0`) — `autolens/analysis/latent.py` gains
  `_pixelized_source_flux(fit, xp)`: for every mapper `inversion.linear_obj_galaxy_dict`
  assigns to the source galaxy, `Σ_i s_i A_i` with `A_i = mesh_geometry.areas_for_magnification`.
  `total_source_flux` and `total_source_flux_mujy` = light-profile flux + that term;
  `magnification` unchanged in form. A mesh geometry without areas gives NaN + one warning,
  never a silent zero. Branching on Python structure only, so the per-sample `jax.jit` path
  is unaffected. 7 tests. 617 passed.
- **PyAutoLens #728** (`5d6eda3`, merge `1f5b1e9`) — correction: divide by the data pixel
  area (`fit.dataset.grids.lp.pixel_area`, a Python float) so the term sits in the module's
  per-data-pixel flux convention. 3 tests, one at 0.5"/pixel pinning the division
  (4.561 → 1.140), one fixed-field-of-view scene stable across pixel scales. 620 passed.
- **euclid_strong_lens_modeling_pipeline #51** (`48d6b45`+`d2457e1`, merge `7067e59`) —
  `scripts/tools/diagnose_latent_vis_pix.py` docstring: `magnification` and the source
  fluxes are NOT stage-invariant (the source model is what `vis_pix` replaces); a new
  `__Which latents are stage-invariant__` section states the definition now in force.
  `tests/test_compute_latent_variable.py`: Delaunay `vis_pix`-style fixture (Hilbert 150 +
  30 circle-edge points, `AdaptImages`, truth lens) and two tests — `magnification` present,
  finite, positive, equal to lensed/source µJy; lens-side latents equal the Sersic control to
  1e-6 while source-side ones differ. 71 passed, CI 9/9 legs.

## Measured

| fit on `euclid_dr1_like` (0.1"/px) | magnification | total_source_flux |
|---|---|---|
| Sersic control (= truth.json) | 15.146 | 0.868 |
| Delaunay 150+30, PyPI autoarray 2026.9.4.1 (Voronoi areas), after #728 | 10.95 | 1.257 |
| same, before #728 | 1095.4 | 0.01257 |

## Traps

- **Unit convention hid a 100× error.** Every flux latent is a *sum over data pixels*
  (`∫ I d²θ / A_pix`), and the reconstruction `s_i` is in those units, so `Σ s_i A_i`
  (arcsec²) must be divided by `A_pix`. PyAutoLens' fixtures use 1" pixels, so #727's
  internal-consistency tests (`Σ image / Σ s·A`) passed while the number was wrong; the
  Euclid workspace test at 0.1"/pixel exposed it. Any new flux-like latent needs a test at
  a non-unit pixel scale.
- **`fit.tracer_to_inversion` is an uncached property** that rebuilds mappers, so its keys
  never match `inversion.reconstruction_dict`. Use `inversion.linear_obj_galaxy_dict`
  (set in `to_inversion.py`); its galaxy values are the tracer's own objects.
- **kNN / DelaunayNN meshes do not hit the NaN branch**: they inherit
  `InterpolatorDelaunay.mesh_geometry`, so they expose `areas_for_magnification` and get a
  number. Whether kNN areas are the right quadrature for those interpolants is the open
  lead in `draft/test/workspaces/mesh_magnification_correctness.md`.
- **`magnification` is NaN whenever the regularized reconstruction has net-negative flux**
  — `total_source_flux_mujy` takes `log10` of a negative flux. Pre-existing µJy behaviour,
  unchanged here; the #728 scale-stability test had to pick a mesh/regularization where the
  reconstruction stays positive.
- **Feature/Bug agents scored the prompt "too-large" (17) on length and repo count** and
  proposed a 4-phase split; the declared small-medium with the architect design was right.
- **Merging a `Fixes #N` library PR auto-closes the issue** while a workspace half is still
  pending — edit the body to `Part of #N` before merging.

## Follow-ups filed

- `draft/bug/euclid/delaunay_edge_ring_never_zeroed.md` — `scripts/initial_lens_model.py`
  passes the appended grid length as `Delaunay(pixels=…)` with `zeroed_pixels=30`;
  `Delaunay.__init__` adds `zeroed_pixels` itself, so the zeroed indices land past the mesh
  and the edge ring is never zeroed (latents bit-identical either way on the test scene).
- Human acceptance still open on #726: `part3b_fit_latent.py` (500-point mesh, PyAutoArray
  `main` dual areas) should report a finite `vis_pix` magnification near 15.15. Archived
  `vis_pix` rows carry the `0.0` sentinel and must be re-derived (epic item 8, Cortex
  phase 4 note). `catalogue/scripts/magnitudes.py:305` ingests the latent unchanged.

## Session notes

Shipped from a web session (no worktree, no `gh`): shallow clones of PyAutoLens and the
Euclid pipeline, GitHub via the MCP surface; a Fable session planning with three Opus
subagents executing (library fix, workspace leg, pixel-area correction).

## Original prompt

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
Issued: 2026-09-05

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
