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
