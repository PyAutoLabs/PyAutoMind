# Multi-dataset shared-state — Phase 2: core library API

Autonomy: safe
(feature, difficulty medium — mirrors the shipped PyAutoArray#344 / PyAutoLens#566
consumer pattern; sized at issue by the launching session, --auto granted by the
user 2026-07-10 with the H-removal amendment.)

Phase 2 of 4 of `feature/autolens/multi_shared_state_examples.md`. Phase 1
design is **locked** (PyAutoLens#599, design-note comment, decisions D1–D6) —
implement it, do not re-open it.

## Scope (locked by Phase 1 — see #599 D1/D5/D6)

- **PyAutoArray:** new field on `aa.AbstractPreloads` (dataset-type-agnostic,
  per D5): `source_plane_mesh_grid` (traced mesh centres + triangulation via
  the existing mesh-geometry objects). **NO `regularization_matrix` preload**
  (user amendment 2026-07-10: regularization may be data-dependent, e.g.
  adaptive regularization — each factor builds its own `H`).
  New `PreloadsImaging` sibling whose docstring records the
  invariance contract: the mesh geometry is shareable across exposures under
  one lens model; the mapper, curvature matrix, blurred mapping matrix and
  regularization matrix are NOT
  (unlike the datacube, whose channels share one grid — its whole-mapper +
  `F` preload stays untouched). JAX pytree registration.
- **PyAutoLens:** `AnalysisImaging.shared_preloads` flag + `shared_state_from`
  (lead factor, per D6): apply the lead's `aa.DatasetModel` offset → trace the
  lead image-mesh once → return `PreloadsImaging(source_plane_mesh_grid=...)`.
  `shared=` threaded through `log_likelihood_function` → `fit_from` →
  `FitImaging` → `TracerToInversion` (mirror PR#566's threading). NEW reuse
  path in `TracerToInversion`: when `preloads.source_plane_mesh_grid` is set,
  skip `image_plane_mesh_grid_pg_list` + mesh tracing and build this dataset's
  mapper (its own offset grid) onto the preloaded mesh. Each factor's own
  `DatasetModel` offset applies to its data grid as today.
- **Out of scope (D2):** the literal same-λ joint stacked inversion (one solve,
  `F = Σ LᵢᵀWᵢLᵢ`) — that is the separate `multi_joint_stack_inversion`
  follow-up prompt; this phase ships shared-mesh-per-factor only.
- **Unit tests:** numpy-only (never JAX in library unit tests) — shared-vs-
  unshared `figure_of_merit` parity, opt-in default-off, non-multi path
  byte-for-byte unchanged. JAX/jit validation goes in the workspace_test parity
  script (Phase 3), mirroring
  `autolens_workspace_test/scripts/jax_likelihood_functions/datacube/shared_preloads.py`.

## References

- Interferometer consumer as the pattern: PyAutoArray#344 + PyAutoLens#566.
- Mechanism: PyAutoFit#1308 (`Analysis.shared_state_from`, `shared=` kwarg,
  lead-factor compute-once forwarding).
