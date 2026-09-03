# Mapping overlay follow-ups: forward regions= through the autogalaxy plot wrappers, fix degenerate…

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace
Difficulty: medium
Autonomy: safe
Priority: medium
Epic: image-source-mappings
Status: formalised
Consequence: judge
Witness: `aplt.plot_array(array=fit.data, regions=[mapping.image_contours])` draws the overlay with no TypeError, and `Mapper.mappings_from(pix_indexes=[[0]])` on a `RectangularBilinearAdaptDensity` mapper returns a mapping with at least one image region or raises.
Review-minutes: 20
Unattended: ready

# Mapping overlay follow-ups: forward regions= through the autogalaxy plot wrappers, fix degenerate adapt-mesh edge cells, per-region labels

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace
Epic: image-source-mappings
Difficulty: medium
Priority: medium
Witness: `aplt.plot_array(array=fit.data, regions=[mapping.image_contours])` draws the overlay with no TypeError, and `Mapper.mappings_from(pix_indexes=[[0]])` on a `RectangularBilinearAdaptDensity` mapper returns a mapping with at least one image region or raises.

Mapping overlay follow-ups surfaced by image-source-mappings Phase 3 (issue #525 on the lens workspace). None were patched around in the workspace beyond an `import autoarray.plot as aaplt`.

1. `autogalaxy/util/plot_utils.py` `plot_array` / `plot_grid` (re-exported by the downstream `plot` namespaces that every workspace imports as `aplt`) do not forward `regions=` / `region_colors=` / `region_alpha=` / `region_labels=` (plot_array) or `indexes=` (plot_grid) to `autoarray.plot`, so `aplt.plot_array(array=..., regions=[...])` raises `TypeError` and every workspace script drawing a mapping imports `autoarray.plot as aaplt` instead. Add the pass-through in PyAutoGalaxy, then drop the `aaplt` imports from the Phase 3 scripts (the target workspace's guides/plot/visuals.py, guides/mappings.py and its four pixelization scripts; the sibling workspaces' and HowTo tutorials' twins in their own follow-ups).
2. `RectangularBilinearAdaptDensity` mesh cells on the outer top row and left column have zero-extent contours, and `Mapper.mappings_from` returns zero image regions for them, so a colour group vanishes from a `regions=` figure silently. Fix the degenerate cells, or make `mappings_from` warn or raise on an empty mapping.
3. `region_labels` writes one label per polygon, so a source-plane clump made of many mesh cells is stamped once per cell and unreadable. Label once per connected region (or once per region when its polygons tile a single area) while keeping the per-multiple-image labelling that PyAutoArray#518 introduced for image-plane regions.
4. `plot_mapper` with `solution_vector=None` cannot zoom (a single adaptive-mesh cell draws as a speck) and swallows every exception into `logger.info`, hiding source-panel failures.

<!-- formalised by the Intake (Conception) Agent on 2026-09-03 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/8b332beb-02ad-447e-966b-0514e2ac32f5/scratchpad/intake_mappings_followup.txt -->
