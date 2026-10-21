# autolens_workspace point_source/plot.py crashes: residual_map (4,2) vs (5,2) broadcast; the model solves 5 images for 4 observed

Type: bug
Consequence: judge
Autonomy: human-required

@autolens_workspace @PyAutoLens

## Finding (2026-10-21, smoke run during point-fit-source-plane-panel, PyAutoLens#790)

`autolens_workspace/scripts/point_source/plot.py` gets far enough to draw `aplt.subplot_fit_point`, then crashes at line ~129, `print(fit.positions.residual_map)`, with a (4,2) vs (5,2) broadcast error. The line was not touched by #790.

The same symptom showed up in the source-plane prototype: at the true model, the image-pair point_source fit solves **5 model images for 4 observed** (uninvestigated).

## Intent

- Determine whether the 5th image is a demagnified central image that `magnification_threshold` should have removed, a duplicate root, or a real fifth image.
- Determine whether the residual_map path of the image-pair fits mishandles an unequal number of model and observed positions, given that the pairing fits handle it.
- Fix the root cause in the library or the script, and add a regression test.
