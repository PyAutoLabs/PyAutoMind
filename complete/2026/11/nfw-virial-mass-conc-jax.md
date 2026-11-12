## nfw-virial-mass-conc-jax
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/695
- completed: 2026-11-06
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/696
- summary:
  - `NFWVirialMassConcSph` (m200c + free concentration) is now JAX-traceable: `kappa_s_and_scale_radius` picks `jax.numpy` when `virial_mass` or `concentration` is a JAX array/tracer (reusing `is_jax` from `gnfw_virial_mass_conc`), NumPy otherwise; NumPy values unchanged.
  - First unit tests for the profile: `test_autogalaxy/profiles/mass/dark/test_nfw_virial_mass_conc.py` (NumPy regression; jit of deflections over (m, c) vs NumPy to 1e-10). Full test_autogalaxy 1477 passed; CI green (3.12, 3.13, no-JAX, docs).
  - Shipped under a human override of the PyAutoGalaxy claim held by `magnification-maps-wiring` (disjoint files).
  - Needed by the Science project `sdssj0946_subhalo` (He et al. 2025 reproduction on RAL A100s); its stopgap `scripts/nfw_m200c.py` is retired once RAL's PyAutoGalaxy includes 830dc3e7.
  - No workspace impact: `autolens_workspace` guides/profiles/light_and_mass_profiles.py and `autolens_workspace_test` misc/mass_via_integral/gnfw_virial_mass_conc.py smoke-tested OK.

## Original prompt

# NFWVirialMassConcSph is not JAX-traceable (hard-coded NumPy in the mass→kappa_s conversion)

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Themes:
- jax
- dark-matter
- subhalo
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Issued: 2026-11-06
Consequence: glance
Witness: `jax.jit` of a function building `al.mp.NFWVirialMassConcSph(virial_mass=m, concentration=c, ...)` from traced `(m, c)` and returning its deflections runs without `TracerArrayConversionError`, and matches the NumPy result to 1e-10 (relative) on a grid; existing NumPy tests unchanged.
Review-minutes: 3
Unattended: ready

Found 2026-11-06 while setting up the `sdssj0946_subhalo` science project
(He et al. 2025, arXiv:2506.07978 reproduction: NFW subhalo with m200c and a free
concentration, fitted on RAL A100 GPUs under JAX).

`autogalaxy/profiles/mass/dark/nfw_virial_mass_conc.py`: the module-level
`kappa_s_and_scale_radius(virial_mass, concentration, virial_overdens, redshift_object, redshift_source)`
hard-codes `np` (`np.log`, `np.pi`, and the Planck15 calls with `xp=np`), so jitting over
`virial_mass` / `concentration` raises:

```
TracerArrayConversionError: The numpy.ndarray conversion method __array__() was called on traced array with shape float64[]
```

Fix: choose `xp` from the input type exactly as `mcr_util.kappa_s_and_scale_radius_for_ludlow`
(used by `NFWMCRLudlow`) does — NumPy for floats/ndarrays, `jax.numpy` otherwise — and pass it
through the cosmology calls. Add a unit test that jits deflections over
`(virial_mass, concentration)` and compares with the NumPy path.

Original request (verbatim): "Bug fix in PyAutoGalaxy: al.mp.NFWVirialMassConcSph
(autogalaxy/profiles/mass/dark/nfw_virial_mass_conc.py) is not JAX-traceable.
kappa_s_and_scale_radius hard-codes numpy (np.log, Planck15 calls with xp=np), so jax.jit over
virial_mass/concentration raises TracerArrayConversionError. Fix: pick xp from the input type
exactly as mcr_util.kappa_s_and_scale_radius_for_ludlow / NFWMCRLudlow do, and add a unit test
that jits deflections over (virial_mass, concentration) and matches the numpy result. Needed by
the sdssj0946_subhalo science project (He et al. 2025 reproduction: NFW with m200c and free
concentration on RAL A100 GPUs). Small, library-only."
