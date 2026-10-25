# Mirror point-visualization keys into autolens_assistant

Consequence: glance
Autonomy: safe-capped
Status: planned
Builds-on: complete/2026/10/point-plots-yaml-keys.md

@autolens_assistant

## Remaining scope

The HowToLens half shipped in PR99. HowToLens issue98 is a closed parent, not a tracking issue for this remaining assistant work. Live main still has only point_dataset.subplot_dataset and an empty fit_point_dataset block on 2026-10-25.

Mirror only the point_dataset and fit_point_dataset blocks from the released PyAutoLens configuration into config/visualize/plots.yaml, retaining the canonical comments and defaults. Verify the release of PyAutoLens#794 before shipping, as the original prompt requires. Recheck active claims and file a separate issue when starting implementation. Do not mark this planned task complete merely because its parent issue is closed.

## Acceptance

Compare the parsed two blocks and their comments with the released library; preserve all other configuration. Run the applicable assistant configuration checks. Missing keys currently fall back to on, so this is configuration consistency rather than proven runtime breakage.

## Original scope, preserved

Mirror image_with_points, fit_image_with_points, subplot_point_solver, fit_per_image, subplot_dataset_combined, image_with_points_combined, subplot_fit_combined, fit_per_image_combined and fit_image_with_points_combined. The original two-repository request is retained in complete/2026/10/point-plots-yaml-keys.md.
