# Workspace config cleanup: remove orphan config keys the Nerves board flags

Type: maintenance
Target: workspaces
Repos:
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
- autocti_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: after the change, a local Nerves board render (`python3 scripts/board.py --json` in PyAutoNerves) reports 0 workspace files with orphan keys (down from 14 files / 79 keys), except any key this task keeps with a recorded reason; each touched workspace's start_here/smoke scripts still load their config with no config-key error.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-27
Epic: organ-cockpit
Lane: local-dev

## Why

The Nerves board (PyAutoNerves#175, shipped 2026-09-27 in the cockpit-followups bundle) now lists
workspace config keys that no library in the stack defines. On the 2026-09-27 render
(https://pyautolabs.github.io/PyAutoNerves/) the board is YELLOW with **14 workspace config files
carrying 79 orphan keys**. They are dead settings that mislead users who edit them expecting an effect.

## The orphan keys (workspace side — in scope)

- autofit_workspace/config/general.yaml (L14, 6): hpc.live_visual_update, hpc.quick_update_background, test.check_preloads, test.preloads_check_threshold, version.minimum_library_version, version.workspace_version_check
- autofit_workspace/config/visualize/plots_search.yaml (L6, 1): mle.corner_cornerpy
- autogalaxy_workspace/config/general.yaml (L26, 5): hpc.live_visual_update, hpc.quick_update_background, test.disable_positions_lh_inversion_check, version.minimum_library_version, version.workspace_version_check
- autogalaxy_workspace/config/notation.yaml (L24, 2): label.label.contribution_factor, label_format.format.contribution_factor
- autogalaxy_workspace/config/visualize/general.yaml (L14, 14): subplot_shape.1, subplot_shape.100, subplot_shape.12, subplot_shape.16, subplot_shape.2, subplot_shape.20, subplot_shape.36, subplot_shape.4, subplot_shape.49, subplot_shape.6, subplot_shape.64, subplot_shape.81, subplot_shape.9, subplot_shape_to_figsize_factor
- autogalaxy_workspace/config/visualize/plots.yaml (L30, 1): fit_imaging {}
- autolens_workspace/config/general.yaml (L25, 5): hpc.live_visual_update, hpc.quick_update_background, version.minimum_library_version, version.python_version_check, version.workspace_version_check
- autolens_workspace/config/notation.yaml (L24, 10): label.label.contribution_factor, label.label.ra, label.label.rs, label.label.sigma_scale, label.superscript.hyperbackgroundnoise, label.superscript.hypergalaxy, label.superscript.hyperimagesky, label_format.format.contribution_factor, label_format.format.ra, label_format.format.rs
- autolens_workspace/config/priors/mesh/delaunay.yaml (L2, 1): delaunay.areas_factor
- autolens_workspace/config/visualize/general.yaml (L14, 14): subplot_shape.1, subplot_shape.100, subplot_shape.12, subplot_shape.16, subplot_shape.2, subplot_shape.20, subplot_shape.36, subplot_shape.4, subplot_shape.49, subplot_shape.6, subplot_shape.64, subplot_shape.81, subplot_shape.9, subplot_shape_to_figsize_factor
- autocti_workspace/config/general.yaml (L2, 6): analysis.n_cores, analysis.preload_attempts, profiling.should_profile, test.check_preloads, test.disable_positions_lh_inversion_check, test.preloads_check_threshold
- autocti_workspace/config/visualize/general.yaml (L5, 2): general.subplot_ascending_fpr, general.symmetric_cmap_value
- autocti_workspace/config/visualize/plots.yaml (L1, 11): combined_only, dataset.data, dataset.data_binned, dataset.data_logy, dataset.fpr_non_uniformity, dataset.subplot_dataset_regions, fit.data_logy, fit.fits_fit, fit.residual_map_logy, fit.subplot_fit_regions, subplot_format
- autocti_workspace/config/visualize/plots_search.yaml (L6, 1): mle.corner_cornerpy

Before deleting each key, grep the workspace itself (scripts, notebooks, `start_here.py`, any
workspace-local helper) for a reader: the board only checks library code, so a key read by the
workspace's own code (possibly the `version.*` keys via the version handshake in autonerves, or
`subplot_shape.*` read by an integer lookup) is not an orphan. Keep any such key and record why.
Mirror the removals into the matching notebooks/markdown only if they carry config snippets.

## The typo

`autogalaxy_workspace/config/visualize/plots.yaml:30` has `fit_imaging {}:` — a malformed key (the
`{}` looks like a leftover flow-mapping), so the `fit_imaging` section it was meant to open is not
read. Fix it to the intended `fit_imaging:` section (compare with autolens_workspace's plots.yaml),
not just delete it.

## Separate, human-review-gated: library-side unused keys (NOT in scope to remove without review)

The same scan flags library config keys no library code reads. These need a human to confirm
before removal, because a key may be read dynamically (string-built lookups the scan cannot see):
- PyAutoLens `config/non_linear.yaml`: a dead 57-key `nest.DynestyStatic` / `nest.DynestyDynamic`
  block (Dynesty searches live in PyAutoFit's config; PyAutoLens's copy is not read).
- PyAutoLens `general.yaml`: `output.fit_dill`.
- PyAutoFit `general.yaml`: `output.log_level`, `output.log_to_file`, `output.log_file`,
  `output.search_internal`, `profiling.repeats` (may be read dynamically — needs review);
  `non_linear/GridSearch.yaml`: `parallel`, `parallel.number_of_cores`, `parallel.step_size`.
- PyAutoArray `general.yaml`: `numba.use_numba`; PyAutoGalaxy `general.yaml`: `adapt.adapt_noise_limit`.
- PyAutoCTI `general.yaml`: `fits.flip_for_ds9`, `hpc.iterations_per_update`, `model.ignore_prior_limits`,
  `output.log_file`, `output.log_level`, `output.log_to_file`.

Present this list to the human; remove only what they confirm, as a library change shipped before
the workspace edits (library-first), or re-file it as its own library prompt.

## Related prompts

- `draft/maintenance/workspaces/config_key_mirror_drift.md` — the opposite direction (library keys
  missing from workspace configs); do both in one pass if picked up together, and do not re-add a
  key this task removes.
- `draft/maintenance/workspaces/sync_remaining_workspace_config_priors_copies.md`.

<!-- formalised by the Intake (Conception) Agent on 2026-09-27 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/3d063f57-b2ec-4cbe-af26-06bb6719f5e5/scratchpad/intake_raw.md -->
