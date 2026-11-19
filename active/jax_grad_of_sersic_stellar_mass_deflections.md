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
