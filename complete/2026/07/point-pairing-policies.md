## point-pairing-policies
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/585 (closed)
- completed: 2026-07-09
- prs: PyAutoLens#586 + autolens_workspace#248 (merged)
- notes: unmatched_model_policy on FitPositionsImagePairRepeat (magnification_filter default —
  demagnified-central convention, |mu|<0.1 exempt; penalize/ignore via class-attr pattern);
  Hungarian under-prediction reward fixed (all-caps warning retired); no_image_residual finite
  floors; n_unmatched_model_positions diagnostic; guides/point_source_pairing.py with the
  "search source-plane, validate image-plane" workflow. magnification_filter default stood at merge.
