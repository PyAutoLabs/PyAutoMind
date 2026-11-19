`jax.grad` of `mp.Sersic` CSE deflections made finite, merged 2026-11-19 (PyAutoGalaxy#728, merge f99518af; closes PyAutoGalaxy#727).


- Fix: the JAX branch of `MassProfileCSE._decompose_convergence_via_cse_from` (`autogalaxy/profiles/mass/abstract/cse.py`) solves the CSE least-squares amplitudes by `jnp.linalg.qr` + `jax.scipy.linalg.solve_triangular` instead of SVD-based `jnp.linalg.lstsq`, whose reverse-mode derivative was NaN on the ill-conditioned 80×50 matrix. NumPy path (scipy `lstsq`) unchanged. Shared mixin, so `SersicGradient` and the elliptical NFW CSE path also get finite gradients. JAX deflections move ~1e-5 relative.
- Test: `test__jax_grad__deflections_finite_and_match_finite_differences` (`test_autogalaxy/profiles/mass/stellar/test_sersic.py`).
- Witness (run by the independent close-out session on head 275d7904): the PR test fails on main with a NaN gradient and passes on head; the science reproducer `stars_dm_slope/scripts/scratch/repro_sersic_cse_grad_nan.py` goes from nan to d/d(M/L) = 0.483146349 (= value / M/L); an independent finite-difference check (different parameters, grid and ellipticity) agrees to ≤3e-11 on head. That independent config also gave finite gradients on main, so the NaN depends on configuration; the PR test's config is the one that discriminates.
- Gate: tests (PyAutoGalaxy 1555 passed, PyAutoLens 1032 passed + 1 xfail), smoke 213/0, review CLEAN, Heart scoped green, public-names CLEAN, CI GREEN (one skipped non-test leg: Refresh the Heart feed).
- Merged by the shift 2026-11-19-am close-out session (claude-opus-5-5).

## Original prompt

# jax.grad of Sersic stellar-mass deflections is NaN with respect to mass_to_light_ratio…

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `jax.grad` of summed `mp.Sersic` deflections with respect to each of mass_to_light_ratio, intensity, effective_radius and sersic_index is finite and matches finite differences to 1e-4
Review-minutes: 3
Unattended: ready
Verified: 2026-11-19 b9232172 (PyAutoGalaxy)
Lane: any

Found 2026-11-16 in the science project stars_dm_slope. `jax.grad` of `al.mp.Sersic` / `al.lmp.Sersic` deflections with respect to `mass_to_light_ratio` is NaN although the deflections are exactly linear in it; intensity, effective_radius, sersic_index and ellipticity gradients are NaN too. The cored-steep-ellipsoid amplitudes come from a `jnp.linalg.lstsq` solve (`_decompose_convergence_via_cse_from`, `autogalaxy/profiles/mass/abstract/cse.py`) on an ill-conditioned matrix whose reverse-mode derivative is NaN. The gNFW (MGE) deflection gradient is finite. Any gradient-based search or optimiser on a stellar Sersic mass model therefore fails. Reproducer: `/home/jammy/Science/Science/development/stars_dm_slope/scripts/scratch/repro_sersic_cse_grad_nan.py`.
Fix: make the decomposition differentiable (e.g. solve the regularised normal equations or use a custom JVP/VJP for the least-squares solve; take the mass_to_light_ratio and intensity factors outside the solve since the amplitudes are linear in them), and add a test that the gradient with respect to each Sersic parameter is finite and matches finite differences.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Science/4543c7f0-9e90-432b-a76f-76d0789fa7b1/scratchpad/intake/4_sersic_cse_gradient_nan.md -->
