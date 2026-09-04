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

Note this defect is **independent** of the Delaunay area defect filed as
`draft/bug/autoarray/delaunay_magnification_uses_voronoi_not_dual_areas.md`: the latent
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

<!-- formalised by the Intake (Conception) Agent on 2026-09-04 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/4974a870-2ecf-47c9-9592-6a344294c707/scratchpad/raw_prompt2.md -->
