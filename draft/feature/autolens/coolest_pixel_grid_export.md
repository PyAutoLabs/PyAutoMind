# COOLEST: export MGE lens light and pixelized sources as pixel grids

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- euclid_strong_lens_modeling_pipeline
Themes:
- coolest
- interop
- euclid
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Filed: 2026-09-16

Follow-up to `coolest_observation_grid_and_euclid_output.md`, which made `to_coolest` skip
and record components COOLEST has no analytic profile for. The Euclid DR1 fits use an MGE
(`Basis` of Gaussians) for the lens light and a Delaunay pixelized source, so today their
COOLEST templates carry the mass model and Sersic light only, with the rest listed under
`meta.skipped_profiles`.

## Scope

- `Basis` lens light → evaluate the fitted MGE on the observation grid and export it as a
  COOLEST `PixelatedRegularGrid` light profile (FITS file beside the JSON, `fits_path` set,
  `check_external_files` honoured).
- Pixelized source (Delaunay / Voronoi / rectangular mesh) → export the source-plane
  reconstruction as a COOLEST `IrregularGrid` (or `PixelatedRegularGrid` for rectangular
  meshes) light profile of the source entity.
- `from_coolest` round-trips both back to `al.Galaxy` objects where a PyAutoLens
  equivalent exists; otherwise documents the one-way export.
- The Euclid pipeline's `files/coolest.json` then carries the full model; the
  `skipped_profiles` record stays for anything still unsupported.
- Guide `scripts/guides/coolest_interop.py`: a section on the grid exports.
