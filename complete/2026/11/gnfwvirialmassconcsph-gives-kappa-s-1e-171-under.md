# gNFWVirialMassConcSph gives kappa_s ~1e-171 under JAX because jax.scipy.special.hyp2f1 is wrong for z < -1

Completed 2026-11-18. Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/721

`kappa_s_and_scale_radius` in `autogalaxy/profiles/mass/dark/gnfw_virial_mass_conc.py` now evaluates 2F1(a, a; a+1; -c) on the JAX path through Pfaff's transformation, (1 + c)^-a 2F1(1, a; a+1; c/(1+c)), which keeps the argument in (0, 1) where `jax.scipy.special.hyp2f1` is accurate. The NumPy path keeps the direct SciPy call, unchanged. Two tests added: NumPy kappa_s against the closed form, and jitted kappa_s against NumPy over inner_slope 0 to 1.99 and c_2 2 to 2000. No other dark profile calls `hyp2f1`. The upstream jax defect was not reported in this task.

## Merge receipts

- PyAutoGalaxy#722: c2050ac34dbb0f1721e6cec4298ec8489502a6ad (head 0fd5e97546a1fca489cdfb9a44ae6c9feaed9952)

## Validation and authorization

Consequence `glance`, merged unattended by the 2026-11-18-pm shift close-out session (independent of the author). Witness re-run by the close-out at the PR head: jitted kappa_s equals NumPy over inner_slope 0 to 1.99 and c_2 / concentration 2 to 20 (420 cases), worst relative difference 5.6e-14; control: raw `jax.scipy.special.hyp2f1(2, 2, 3, -10)` returns 2.7e242. Dark-profile tests 228/228 at the PR head. public-names CLEAN; Heart scoped dev-ship verdict green; ci-verdict GREEN (4 success, 1 skipped: Refresh the Heart feed, not a test leg); Heart freeze clear.

pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/722

## Original prompt

# gNFWVirialMassConcSph gives kappa_s ~1e-171 under JAX because jax.scipy.special.hyp2f1 is wrong for z…

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: kappa_s of `gNFWVirialMassConcSph` built inside `jax.jit` equals the NumPy value to 1e-8 for inner_slope 0 to 2 and concentration 2 to 20
Review-minutes: 3
Unattended: ready
Issued: 2026-11-18
Verified: 2026-11-18 5515c4da (PyAutoGalaxy)
Lane: any

Found 2026-11-16 in the science project stars_dm_slope. `kappa_s_and_scale_radius` in `autogalaxy/profiles/mass/dark/gnfw_virial_mass_conc.py` calls `hyp2f1(a, a, a + 1.0, -c)` on the JAX path. `jax.scipy.special.hyp2f1` (jax 0.12) returns inf or ~1e167 for z < -1, and z = -c < -1 for any concentration above 1, so inside `jax.jit` the profile gets kappa_s = 3.8e-171 where the NumPy path gives 0.048: a silent wrong answer for every JAX fit using `gNFWVirialMassConcSph`. Reproducer: `/home/jammy/Science/Science/development/stars_dm_slope/scripts/scratch/repro_jax_hyp2f1_negative_z.py`.
Fix: apply the Pfaff transformation 2F1(a, b; c; z) = (1 - z)^-b 2F1(c - a, b; c; z / (z - 1)), which maps the argument into (0, 1) and agrees with SciPy to 1e-15 (working version: `hyp2f1_pfaff` in `/home/jammy/Science/Science/development/stars_dm_slope/scripts/parameterisations.py`). Add a test comparing the NumPy and jitted kappa_s over inner_slope 0 to 2 and concentration 2 to 20, and check the other callers of jax hyp2f1 in the dark profiles. Consider reporting the jax defect upstream.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Science/4543c7f0-9e90-432b-a76f-76d0789fa7b1/scratchpad/intake/3_gnfw_virial_mass_conc_jax_hyp2f1.md -->
