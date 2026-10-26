# Matrix-free interferometer inversion, phase 5b: profiling note (Pulse); 5c workspace example dropped until the verdict

Type: research
Target: autolens_profiling
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_profiling
- autolens_workspace
Difficulty: large
Autonomy: supervised
Priority: medium
Parent: active/matrix_free_interferometer_inversion.md
Community: https://github.com/PyAutoLabs/.github/discussions/39
Status: formalised
Consequence: judge
Witness: a results note under autolens_profiling/results/notes/ with a dense-vs-matrix-free table (time, peak memory, evidence difference) at 50², 64², 128², 192² on one synthetic and one real interferometer dataset, ingested by PyAutoPulse, plus a workspace example running under the smoke harness
Review-minutes: 20
Unattended: needs-slicing
Filed: 2026-10-21
Blocked-by: none for the profiling leg (runs against checkouts; phases 1-4 on main) — only the workspace example waits for the release. Part of the human's PyAutoPulse profiling programme (anchor Pulse#62); not to be started before that programme.

## What

1. Wiring: DONE 2026-10-26 as phase 5a — `complete/2026/10/matrix-free-interferometer-wiring.md` (PyAutoArray#657 → #658 + Galaxy#670, pending release; an `InversionInterferometerMatrixFree` class behind `Settings(interferometer_route="matrix_free")`). 5b = item 2 below, 5c = item 3; both depend on 5a.
2. Profiling campaign in autolens_profiling (laptop CPU + RAL `ral` partition CPU legs; A100 only if a JAX leg exists by then): dense sparse-path vs matrix-free (unconstrained and positive) at 50², 64², 128², 192²; record time, peak RSS, evidence difference; note with decision rules for the assistant ([[AssistantReadsProfiling]]); summary in the Pulse `profiling-summary` contract.
3. Workspace example: DROPPED 2026-10-26 by the human until the 5b profiling verdict says the route is useful (the `Settings` docs in `autoarray/settings.py` are the only user-facing text until then).
4. Thread update with the table; this is the human's lead-in to the full PyAutoPulse profiling programme.

## 5b pickup note (posted to autolens_profiling#468 on 2026-10-26, for the running campaign)

The matrix-free inversion is on PyAutoArray `main` as of 2026-10-26 (PyAutoArray#658, pending release; PyAutoGalaxy#670 tests). It is opt-in and reachable from any `FitInterferometer` / likelihood function with no other code change:

```python
settings = al.Settings(
    interferometer_route="matrix_free",   # new; None/"fft"/"numba" unchanged
    use_positive_only_solver=True,        # interior point + active-set polish
    use_edge_zeroed_pixels=False,         # REQUIRED with positive-only on this route (raises otherwise)
)
pixelization = al.Pixelization(
    mesh=al.mesh.RectangularUniform(shape=(n, n)),   # only RectangularUniform
    regularization=al.reg.MaternSparse(coefficient=..., scale=...),  # only MaternSparse
)
# dataset after dataset.apply_sparse_operator(use_jax=False)  -- NumPy backend only
```

Constraints (the class raises `InversionException` on each): JAX backend; linear light profiles / func lists; more than one mapper; non-rectangular mesh; any regularization other than `MaternSparse`; positive-only with edge-zeroing; dataset without a sparse operator. Over-sampling and a primary beam are supported. `reconstruction_noise_map` / `curvature_matrix` / `curvature_reg_matrix` are unavailable (raise); the fit visualizer skips the noise-map panel.

What to measure (dense `"fft"` route vs `"matrix_free"`, unconstrained and positive-only), the 5b deliverable from the phase-5 draft:
- wall time per likelihood call and peak RSS at 50², 64², 128², 192² mesh pixels, on one synthetic and one real interferometer dataset;
- `log_evidence` difference: the only approximate term is `ln det(F+H)` by stochastic Lanczos quadrature (10 probes, 40 steps, fixed seed; 0.10% of dense on the test case, documented bound 0.5%). Report the per-probe spread when `W~` is far from diagonal (few visibilities, broad fringes), where it degrades;
- PCG iteration counts (`inversion.pcg_rtol=1e-10`, `pcg_maxiter=5000`; a non-converged solve raises) and interior-point steps (`inversion.positive_result`).

Diagnostics on the inversion: `inversion.operator` (sparse `M`, `curvature_matvec`), `regularization_matrix_sparse`, `positive_result`. The dense route cannot run above ~100²; a matrix-free-only row there is expected, not a failure.

Decision rule the note should produce for the assistant: the mesh size (and visibility count) above which `matrix_free` beats `fft` on time and memory, and whether the SLQ evidence error is below the sampler's resolution there. Workspace example (5c) is **dropped until this verdict**; the Settings docs in `autoarray/settings.py` are the only user-facing text.
