## matrix-free-interferometer-wiring
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/657
- completed: 2026-10-26
- parent: matrix-free-interferometer-inversion (PyAutoArray#638, phase 5a)
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/658
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/670
- summary: `aa.InversionInterferometerMatrixFree` (subclass of `InversionInterferometerSparse`) selectable via `Settings(interferometer_route="matrix_free")`; factory dispatch before the numba gate, no silent fallback; dense attributes raise `InversionException`; inversion plotter skips the noise map on the route. PyAutoGalaxy `FitInterferometer` reaches it through Settings with no source change (tests only). Parity vs FFT route: reconstruction ~1e-11, SLQ ln det 0.10% of dense, evidence within 0.09–0.14 nats of a 0.55 tolerance.
- decisions: over-sampling and primary beam SUPPORTED (prompt listed them unsupported; sparse triplets already fold them in); positive-only + `use_edge_zeroed_pixels=True` RAISES, so packaged defaults need `use_edge_zeroed_pixels=False` (5c example must say so); only `MaternSparse` accepted; mesh must be `RectangularUniform`.
- heart-red-override: live human 2026-10-26 ("I approve of the overrider", "approve" on the plan); development shipping + a separate human `/prm` merge; exact RED reasons and gates on issue #657 and in autonomy_log.md (red-override row). No release.
- traps: Galaxy CI (`lib-tests.yml`) clones dependency libraries on the matching branch name, so a stacked same-name branch tests green before the upstream merges; Mind commit hook wants an explicit file list under a dirty shared checkout.
- next: 5b profiling note + 5c workspace example in `draft/research/autolens_profiling/matrix_free_interferometer_phase5.md`, after the release carrying #658; uncertainty maps / multiple mappers / linear light profiles / JAX out of scope.

## Original prompt

# Matrix-free interferometer inversion, phase 5a: make it selectable from a fit

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
Autonomy: supervised
Priority: high
Parent: active/matrix_free_interferometer_inversion.md (PyAutoArray#638)
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/657
Community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
Consequence: judge
Heart-override: human approved "Human override for Heart RED (development only)" on 2026-10-26 (RED set = release integrate, workspace smoke, worktree drift; none touch PyAutoArray/PyAutoGalaxy)

## Context
Phases 1–4 of #638 are merged (PyAutoArray #645, #650, #651, #652). They are released in
2026.10.23.1 and later. They exist only as utility functions in
`autoarray/inversion/inversion/interferometer/inversion_interferometer_matrix_free_util.py`:
- the operator data term and Powell-preconditioned PCG;
- `aa.reg.MaternSparse`;
- the evidence log-dets via exact sparse LU + stochastic Lanczos quadrature;
- positivity via primal-dual interior point with active-set polish.

The module docstring says: "None of it is wired into fits and there is no `Settings` flag."
This task wires it in. It is the "wiring" item of
`draft/research/autolens_profiling/matrix_free_interferometer_phase5.md`. Split that draft:
this task is 5a; the profiling note and the workspace example stay in phase 5 as 5b/5c.

## What
1. A new inversion class `InversionInterferometerMatrixFree` (next to `sparse.py` in
   `autoarray/inversion/inversion/interferometer/`). It holds `M` (scipy.sparse mapping matrix),
   the W~ kernel FFT action and the sparse regularization. It provides:
   - `reconstruction` (PCG, or interior point when `use_positive_only_solver`);
   - `log_det_curvature_reg_matrix_term` / `log_det_regularization_matrix_term`
     (phase 3 functions);
   - `mapped_reconstructed_data` / `mapped_reconstructed_image`.
   Dense-only attributes (`curvature_matrix`, `curvature_reg_matrix`, its inverse, `errors`)
   raise a clear `InversionException` naming the matrix-free route. Do not silently build them.
2. A `Settings` option in `autoarray/settings.py`, extending the existing
   `interferometer_route` (`None` / `"fft"` / `"numba"`) with `"matrix_free"`. Document it like
   the existing values and add a packaged config default (off). Dispatch it in
   `autoarray/inversion/inversion/factory.py` around line 228 (the
   `dataset.sparse_operator is not None` branch). Where the matrix-free route can't represent the
   inversion, raise rather than fall back silently. Those cases are: multiple mappers, linear light
   profiles / func lists, over-sampling, a non-trivial primary beam, a non-rectangular mesh, the
   JAX backend.
3. PyAutoGalaxy: `FitInterferometer` reaches it through `Settings` with no other API change. Check
   that `log_evidence`, `figure_of_merit` and the visualizer don't touch the dense attributes on
   this route. Where they do, skip or guard them.
4. Tests (PyAutoArray + PyAutoGalaxy):
   - on a small rectangular `MaternSparse` interferometer case, `FitInterferometer` via
     `interferometer_route="matrix_free"` matches the FFT sparse route: reconstruction to 1e-6
     of its max, log evidence within the documented SLQ tolerance;
   - positive-only parity, as in phase 4;
   - the unsupported cases raise;
   - a nojax leg needs `importorskip` where relevant.
5. Update the module docstring's "Remaining work (phase 5)" list to say wiring is done.

## Out of scope
- The profiling campaign. Matrix-free rows are being added as `experiments/` cells in the
  likelihood-lifecycle 2b interferometer campaign in autolens_profiling, owned by another session.
  Don't touch autolens_profiling.
- The workspace example.
- Uncertainty maps (stochastic diagonal).
- Multiple mappers and linear light profiles.
- A JAX path.

## Witness
In CI: `FitInterferometer` with `Settings(interferometer_route="matrix_free")` on a rectangular
MaternSparse case agrees with the FFT sparse route (reconstruction 1e-6 relative, log evidence
within the SLQ tolerance stated in the module docstring), and every unsupported configuration
raises `InversionException`.
