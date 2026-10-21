# Separate dataset-only and fit point-image figures

@PyAutoLens @autolens_workspace @autolens_visualization @PyAutoEyes

Consequence: judge
Autonomy: human-required
Issued: 2026-10-21
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/781

Follow-up to PyAutoLens#779 (complete/2026/10/point-source-image-overlay.md).

Decisions (human, 2026-10-21): the after-fit figure is renamed `fit_image_with_points.png`; the before-fit, dataset-only
figure stays `image_with_points.png`; autolens_visualization / PyAutoEyes keep both per point domain.

## Original request (verbatim)

ok, can I check we also have a dataset-only version of this which does not include model points or critical curves? It
should be an option (E.g. for display before lens modeling). This model image is good thiugh, albeit the filename should
prob be model_image_with_points.png
