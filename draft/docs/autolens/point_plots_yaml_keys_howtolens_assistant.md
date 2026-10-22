# Mirror PyAutoLens point visualization keys into HowToLens + autolens_assistant plots.yaml

Consequence: glance
Autonomy: safe-capped
builds-on: complete/2026/10/cluster-point-figures.md (PyAutoLens#794; autolens_workspace#594 and autolens_workspace_test#347 already mirrored)

@HowToLens @autolens_assistant

## Intent

The `config/visualize/plots.yaml` point keys are stale in HowToLens and autolens_assistant. Mirror the library `autolens/config/visualize/plots.yaml` entries for `point_dataset` and `fit_point_dataset`, using the same comments and defaults as autolens_workspace#594:
- `image_with_points`, `fit_image_with_points`, `subplot_point_solver`
- `fit_per_image`, `subplot_dataset_combined`, `image_with_points_combined`, `subplot_fit_combined`, `fit_per_image_combined`, `fit_image_with_points_combined`

Missing keys fall back to on, so this is consistency, not breakage. Library is released first: wait for the PyAutoLens#794 release before shipping.
