Keep a dataset-only point-image figure; the after-fit figure becomes `fit_image_with_points.png` (PyAutoLens#781). Follow-up to complete/2026/10/point-source-image-overlay.md.


## What shipped
- **PyAutoLens#782:**
  - `plot_image_with_points` writes `image_with_points.png` without a fit (observed positions only, for display before lens modeling) and `fit_image_with_points.png` with a fit (model positions on image-plane fits, plus critical curves). Both coexist.
  - `plots.yaml` fit key: `fit_point_dataset.fit_image_with_points`.
- **autolens_workspace#592:** five point-source script docstrings describe both figures; notebooks regenerated.
- **autolens_visualization#7:** both point domains keep both figures (gallery 66 → 68).
- **PyAutoEyes:** `dashboard_refresh` run 39591165754 (a4cc7da); all four figures are listed.

## Decisions
- The human chose `fit_image_with_points.png` over `model_image_with_points.png`, because the background pixels are the observed data, not a model image.

## Gotchas
- The autolens_visualization lint runs `ruff format --check`. Run `ruff format` on the producers before shipping.

## Original prompt

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
