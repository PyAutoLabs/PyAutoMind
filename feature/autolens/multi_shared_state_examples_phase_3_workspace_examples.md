# Multi-dataset shared-state — Phase 3: workspace examples + parity test

Phase 3 of 4 of `feature/autolens/multi_shared_state_examples.md`. **Blocked on
Phase 2** (the imaging shared-state API must be on `main`). Update with the
locked API before issuing.

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
