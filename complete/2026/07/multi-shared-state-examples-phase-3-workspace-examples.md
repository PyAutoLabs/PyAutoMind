## multi-shared-state-examples-phase-3-workspace-examples
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/260 (CLOSED)
- completed: 2026-07-10
- epic: multi_shared_state_examples phase 3/4 (+ the scoped-preloads library follow-up)
- library-pr:
  - https://github.com/PyAutoLabs/PyAutoArray/pull/381 (merged)
  - https://github.com/PyAutoLabs/PyAutoLens/pull/601 (merged)
- workspace-pr:
  - https://github.com/PyAutoLabs/autolens_workspace/pull/261 (merged)
  - https://github.com/PyAutoLabs/autolens_workspace_test/pull/162 (merged)
  - https://github.com/PyAutoLabs/autolens_profiling/pull/60 (merged)
- repos: PyAutoArray, PyAutoLens, autolens_workspace, autolens_workspace_test, autolens_profiling
- notes: Docstring'd shared-mesh API sections on the multi feature examples (same_wavelength headline + wavelength_dependence + imaging_and_interferometer + dataset_offsets cross-ref); multi shared_preloads parity script (identical-exposure bit-parity numpy+JAX, g+r shared-mesh vmap==jit; in smoke_tests.txt); runtime measurement 1.14x at hst x 4 exposures (mesh-only, consistency-first framing per #599 D1). REVIEW FIND: cross-dataset-type preloads hazard in merged phase 2 (lead's shared preloads reach every factor; an interferometer mapper/F would silently corrupt an imaging fit) fixed via dataset-scoped consumption (_preloads_scoped: same-type identity, cross-type mesh-only view) + interferometer shared_state_from now populates mesh fields (D5 both directions). TRAP recorded: crashed JAX runs can poison the gitignored lensed_source.fits adapt cache with in-mask NaNs (qhull NaN error) — delete + regenerate. Simulators deliberately untouched (dataset_offsets demos shifts). Same-lambda literal joint stacked inversion remains the un-issued multi_joint_stack_inversion follow-up prompt.

## Original prompt

# Multi-dataset shared-state — Phase 3: workspace examples + parity test

Autonomy: safe
(feature, difficulty medium — docstring'd sections on existing examples + parity/profiling
scripts mirroring the shipped datacube pattern; --auto granted by user 2026-07-10.)

Phase 3 of 4 of `feature/autolens/multi_shared_state_examples.md`. UNBLOCKED 2026-07-10: phase 2 merged (PyAutoArray#380 f8a32d43b + PyAutoLens#600 1513236da). Locked API: `aa.PreloadsImaging(source_plane_mesh_grid, image_plane_mesh_grid)`; `AnalysisImaging(shared_preloads=True)` + `shared_state_from`; `shared=`/`preloads=` threading. NO regularization preload (user amendment). Shared path applies to image-mesh pixelizations (Overlay via AdaptImages).

## Scope

Add **docstring'd sections to the existing examples** (per the parent prompt —
extend, don't rewrite) under `autolens_workspace/scripts/multi/features/`:

- `same_wavelength/` — the headline case: per-exposure pixel offsets, one
  shared/shifted Delaunay mesh. Per the locked Phase 1 semantics (#599 D2:
  option (b)), each exposure keeps its own reconstruction but all live on the
  **identical** source-plane mesh (pixel-by-pixel comparable; their differences
  are diagnostic of registration/PSF quality). The prose must be honest that
  this is not a literal single joint solve — that precision variant is the
  `multi_joint_stack_inversion` follow-up. Shifts default known/fixed; show the
  optional free (dy,dx) nuisance-parameter variant with Gaussian priors from
  registration residuals.
- `wavelength_dependence/` (and/or `pixelization/` if the design routed it
  there) — shared shifted mesh, independent per-dataset reconstructions.
- `imaging_and_interferometer/` — the cross-dataset-type variant.
- `simulator.py` scripts: add per-dataset shifts where needed, **default 0**.
- `dataset_offsets/` cross-references the shared-mesh sections rather than
  duplicating them.

Real-data loading prose (keep to a docstring note, not a runnable pipeline):
shifts come from PyAutoReduce frame products —
`frames/manifest.json` `target_pixel` differences are the relative shifts;
honor `residual_reliable`; check `manifest["data_units"]` (e-/s HST/Keck vs
MJy/sr JWST); record `entry["psf"]["method"]` per frame for PSF-tier
provenance (AO case especially). Do NOT use header RMS_RA/RMS_DEC. Full
semantics in the parent prompt.

- **autolens_workspace_test:** fast-assert parity script mirroring
  `jax_likelihood_functions/datacube/shared_preloads.py` — shared-vs-unshared
  likelihood equality (incl. `jit`), compute-once counter, tiny end-to-end run.
  Register in `smoke_tests.txt` (it is a curated subset — one script).
- **autolens_profiling:** shared-vs-unshared runtime measurement for the
  imaging multi case (sibling of `likelihood_runtime/datacube/shared_preloads.py`),
  result recorded in `results/` + OPTIMIZATION_NOTES — honest about how much is
  speed vs consistency, per the Phase 1 savings quantification.

Workspace config note: mirror any new library config keys into workspace
configs (`feedback_workspace_config_default_true`). Tutorial prose stays Opus.
