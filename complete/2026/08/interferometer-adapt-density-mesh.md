# interferometer-adapt-density-mesh

User correction after #228: the interferometer pixelization *modeling* examples should use the
density-adaptive `RectangularBilinearAdaptDensity` mesh (as the imaging counterparts and the lens
workspace do); `RectangularUniform` is reserved for `fit.py` and `likelihood_function.py`.

## Shipped
- autogalaxy_workspace #231 — `interferometer/features/pixelization/modeling.py` and
  `galaxy_reconstruction.py` switched to `RectangularBilinearAdaptDensity` (code + prose, rationale
  sentence added); `galaxy_reconstruction.py`'s "RectangularUniform mesh … which is a triangulation"
  description of its `scipy.spatial.Delaunay` call corrected. Notebook twins regenerated.

## Checked, no change needed
- autolens_workspace interferometer pixelization: Bilinear in fit / modeling / source_science / slam,
  Uniform only in likelihood_function.py — already correct.
- `RectangularBilinearAdaptDensity` needs no adapt image (used bare in the lens interferometer modeling).

## Original prompt

# Interferometer pixelization modeling examples should use RectangularBilinearAdaptDensity

Type: docs
Target: workspaces
Repos:
- autogalaxy_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Issued: 2026-08-28
Status: formalised

# Interferometer pixelization modeling examples should use RectangularBilinearAdaptDensity

Type: docs
Target: autogalaxy_workspace
Repos:
- autogalaxy_workspace
Difficulty: small
Autonomy: supervised
Priority: normal

## Problem

`scripts/interferometer/features/pixelization/modeling.py` and `galaxy_reconstruction.py` use
`RectangularUniform`; the modeling examples should use `RectangularBilinearAdaptDensity` as the imaging
counterparts and the lens workspace's interferometer modeling do. `RectangularUniform` is only for `fit.py`
and `likelihood_function.py`. `galaxy_reconstruction.py` also says the scipy.spatial code builds "a
RectangularUniform mesh … which is a triangulation" — it builds a Delaunay triangulation.

## Fix

Switch the mesh (code + prose) in both scripts, add the one-sentence density-adaptive rationale the imaging
modeling.py carries, fix the triangulation sentence, run both under the smoke env, regenerate the two
notebook twins. `fit.py` / `likelihood_function.py` unchanged. Lens workspace already correct.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b766a19b-260c-4b56-8d19-072fa9a34b28/scratchpad/intake_adapt_mesh.md -->
