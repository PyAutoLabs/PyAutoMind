# JAX positive-only (PDIP NNLS) solve does not converge on the SLaM source_lp[1]…

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoFit
- PyAutoLens
- autolens_profiling
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: high
Memory: reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/lensing/sources/lens-modeling-methods.md
Status: formalised
Consequence: glance
Witness: A PyAutoArray regression test builds the 2-basis SLaM MGE model (2 x 20 lens Gaussians with sigma_min = pixel_scale/10 plus 20 source Gaussians) and, at every one of a fixed set of >= 48 near-truth parameter vectors, the JAX positive-only reconstruction reports converged=True and its log-likelihood agrees with NumPy fnnls within 1 nat on CPU fp64; the test fails red on current main (14/48 unconverged).
Review-minutes: 3
Unattended: needs-slicing

# JAX positive-only (PDIP NNLS) solve does not converge on the SLaM source_lp[1] MGE model and returns wrong log-likelihoods

Type: bug
Priority: high
Repos:
- PyAutoArray
- autolens_profiling
Witness: A PyAutoArray regression test builds the 2-basis SLaM MGE model (2 x 20 lens Gaussians with sigma_min = pixel_scale/10 plus 20 source Gaussians) and, at every one of a fixed set of >= 48 near-truth parameter vectors, the JAX positive-only reconstruction reports converged=True and its log-likelihood agrees with NumPy fnnls within 1 nat on CPU fp64; the test fails red on current main (14/48 unconverged).

Target: PyAutoArray

## Witness (2026-09-24 audit, autolens 2aaa1c1a8 / autoarray 681938ae, jax 0.10.2, CPU fp64)

The SLaM `source_lp[1]` imaging model (autolens_workspace `scripts/imaging/features/pixelization/slam.py:66-116`: lens light = 2 bases x 20 Gaussians, `sigma_min = pixel_scale/10`; source = 20 Gaussians; free Isothermal + ExternalShear; 60 linear columns, 17 free parameters) was evaluated at 48 parameter vectors within +/-0.005 of the simulated truth on the HST-like `simple__no_lens_light`-style dataset used by autolens_profiling.

- 14/48 points hit the `max_iter=50` cap of `solve_nnls_primal` (jaxnnls primal-dual interior point, `lax.while_loop`, `autoarray/util/jax_nnls.py:33-78`, called from `reconstruction_positive_only_from` in `autoarray/inversion/inversion/inversion_util.py:391-466` after Jacobi preconditioning) and return log-likelihoods from -2e5 down to -1e138. NumPy fnnls on the same curvature/data vector gives sane values (15k-22k).
- Raising the cap to 200: 9 of the 14 converge (72-195 iterations), 5 never converge and return NaN.
- Converged results are not always right either: one GPU point was 1 nat off fnnls.
- Results differ between CPU, GPU, single and vmap evaluation and under 1e-16 perturbations of the images. The Jacobi-preconditioned curvature matrix has condition number ~1.5e11. Suspect: near-collinear narrow Gaussians across the two lens bases.
- The autolens_profiling `imaging/mge` cell (20+20 Gaussians, mass FIXED) hides this: 1/32 bad points. Any regression test must use the 2-basis SLaM model.
- Under Nautilus `use_jax_vmap=True` (default, `autofit/non_linear/search/nest/nautilus/search.py:198`, n_batch=50) one failing lane makes every batch run all 50 iterations: NNLS is ~28% of a GPU vmap batch and ~44% of a single A100 evaluation, so convergence is also the largest remaining GPU speed lever (~15-17% of a batch).
- Lowering the cap is not safe: 15 iterations already moves the objective by 2e-8 at converging points.
- The certified active-set solver (`autoarray/util/jax_active_set.py`, PyAutoArray#566/#567) is refused whenever the inversion contains `AbstractLinearObjFuncList` (`autoarray/inversion/inversion/abstract.py:578-598`), so the MGE path cannot opt into it today.

## Ask

1. Reproduce with a regression test on the 2-basis SLaM MGE model (compare the JAX positive-only reconstruction / log-likelihood against fnnls at a set of near-truth vectors; assert agreement within a nats tolerance and that `converged` is true).
2. Isolate the root cause (conditioning of the collinear 2-basis block vs PDIP tolerance/`nnls_target_kappa` vs cap) and fix convergence: candidates are better preconditioning, a tolerance/adaptive-cap policy, a fallback when the loop hits the cap (never return the unconverged iterate as a likelihood), or extending the certified active-set solver dispatch to linear-object-function inversions.
3. Numerics: converged points must stay within fp tolerance of current results; only the failing points may change (towards fnnls).
4. Report the CPU and GPU timing impact on the SLaM model single and vmap16 (autolens_profiling `imaging/mge` runtime cell is NOT representative; measure the 60-column model).

Audit scripts and JSON artefacts (nnls_fail.py, nnls_fail_slam_cpu.json, lanes.py) exist in the 2026-09-24 session scratch dir; regenerate rather than rely on them.

<!-- formalised by the Intake (Conception) Agent on 2026-09-24 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/4c46534e-38b6-47fd-9021-8040da7c7d92/scratchpad/mge_audit/prompt_nnls.md -->
