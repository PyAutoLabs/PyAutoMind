# Remove the dead `fits_dataset` key from the remaining `config/visualize/plots.yaml` copies

Type: maintenance
Target: config
Repos:
- euclid_strong_lens_modeling_pipeline
- autolens_assistant
- autogalaxy_assistant
- HowToLens
- HowToGalaxy
Themes:
- config
- hygiene
Difficulty: trivial
Autonomy: safe
Priority: low
Status: active
Consequence: judge
Review-minutes: 5
Unattended: ready
Filed: 2026-09-08
Issued: 2026-09-10
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/62

Follow-up to PyAutoGalaxy#608 (`dataset-fits-image-only`): the library no longer reads
`visualize/plots.yaml` `dataset.fits_dataset` — `dataset.fits` is always written once, to the
search's `image/` folder, by `save_attributes`. The key was removed from the packaged configs
and from `autolens_workspace`, `autogalaxy_workspace`, `autolens_workspace_test` and
`autogalaxy_workspace_test` in that task. Five more copies still carry the dead key plus its
two comment lines (L8 and L18 of each file):

- `euclid_strong_lens_modeling_pipeline/config/visualize/plots.yaml`
- `autolens_assistant/config/visualize/plots.yaml`
- `autogalaxy_assistant/config/visualize/plots.yaml`
- `HowToLens/config/visualize/plots.yaml`
- `HowToGalaxy/config/visualize/plots.yaml`

A stale key is harmless (nothing reads it), so this is parity hygiene, not a bug. Mirror the
`autolens_workspace/config/visualize/plots.yaml` header wording from that task's PR. One PR
per repo; no notebook regeneration (config only).
