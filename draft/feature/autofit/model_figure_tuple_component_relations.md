# Model figures: annotate relations on tuple components

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- visualization
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Epic: model-figures
Filed: 2026-09-11

Follow-up to phase 2 (`complete/2026/09/model-figures-renderer.md`), found in phase 3
(PyAutoLens#736). A relation on **one component of a tuple parameter** —
`mass.centre.centre_0 = bulge.centre.centre_0 + 0.1` in the lens cookbook's Model Customization
stage — is carried by the spec (`ParamRow.components[0].provenance.kind == "relation"` with the
expression) but `autofit/model_figure/presentation.py` draws the tuple as an ordinary free `centre`
pill: the tuple is only expanded into per-component pills when the components differ in
*sampling/sharing*, not in provenance. Scalar relations show their expression correctly.

## Ask
- In `presentation.py`, treat a differing `provenance.kind` among tuple components as a mixed state
  too, expanding into `centre_0 = bulge.centre.centre_0 + 0.1` (cream relation pill) and `centre_1`
  (free), each with the `2D` context preserved (e.g. a `centre` group label or the pill names).
- Test in `test_autofit/model_figure/test_presentation.py` with the catalogue's tuple construct; add
  the lens cookbook's case to `test_autolens/model_figure` once released.
- Remove the "not yet annotated" caveat from the PyAutoLens `model_cookbook.md` page and the
  autolens_workspace cookbook prose when it lands.
