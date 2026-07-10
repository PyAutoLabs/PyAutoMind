# Multi-dataset shared-state — Phase 2: core library API

Phase 2 of 4 of `feature/autolens/multi_shared_state_examples.md`. **Blocked on
Phase 1** (`multi_shared_state_examples_phase_1_design.md`) — implement the
locked design, do not re-open it. Update this prompt with the Phase 1 decisions
before issuing.

## Scope (subject to Phase 1 lock-in)

- **PyAutoArray:** `PreloadsImaging` (sibling of `PreloadsInterferometer`) —
  carrying whatever the design locked as the shared object (expected: shared
  source-plane mesh / mapper geometry; explicitly NOT the curvature matrix or
  blurred mapping matrix, which are per-dataset for imaging). JAX pytree
  registration.
- **PyAutoLens:** `AnalysisImaging.shared_preloads` flag + `shared_state_from`
  building the shared object from the lead factor's instance; `shared=`
  threaded through `log_likelihood_function` → `fit_from` → `FitImaging` →
  `TracerToInversion` (mirror the interferometer consumer's threading from
  PR#566). Same-wavelength joint-reconstruction path per the Phase 1 decision.
  Composition with `aa.DatasetModel` per-dataset offsets.
- **Unit tests:** numpy-only (never JAX in library unit tests) — shared-vs-
  unshared `figure_of_merit` parity, opt-in default-off, non-multi path
  byte-for-byte unchanged. JAX/jit validation goes in the workspace_test parity
  script (Phase 3), mirroring
  `autolens_workspace_test/scripts/jax_likelihood_functions/datacube/shared_preloads.py`.

## References

- Interferometer consumer as the pattern: PyAutoArray#344 + PyAutoLens#566.
- Mechanism: PyAutoFit#1308 (`Analysis.shared_state_from`, `shared=` kwarg,
  lead-factor compute-once forwarding).
