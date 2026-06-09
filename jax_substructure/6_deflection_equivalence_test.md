Context: PyAutoLens issue #542 follow-up (Gap 2, deferred during the original
4-prompt substructure-simulator series). Prompt 1
(`1_vmap_subhalo_deflections.md`) asked for a standalone integration test that
compares the existing Python-loop deflection path against the new vmapped path
for *all four* dark-matter profile types, plus a masked-slot-zero check. That
dedicated test was never authored — deflection correctness is only exercised
indirectly inside the scan / e2e tests. This prompt fills the gap. Workspace
script change → `/ship_workspace`.

## Background

The shipped vmapped path lives in:

- `PyAutoGalaxy/autogalaxy/profiles/mass/abstract/abstract.py` —
  `vmapped_deflections_from(cls, grid, params_batch, mask, xp=None)`: a generic
  classmethod that centres the grid, calls `cls.radial_deflection_from(r, params[2:], xp)`,
  rebuilds (y, x) components, and sums over the batch with `xp.where(mask, ...)`.
- `PyAutoLens/autolens/lens/substructure_util.py` — `galaxies_to_halo_arrays`:
  packs a list of `ag.Galaxy` halos into `(params, mask, sheet_kappas)`. It
  currently branches only on `cNFWSph` (extract `centre, kappa_s, scale_radius,
  core_radius`) vs. everything-else (extract `centre, kappa_s, scale_radius,
  truncation_radius`).

Only two profiles implement `radial_deflection_from`
(`autogalaxy/profiles/mass/dark/cnfw.py` and `.../nfw_truncated.py`); the four
MCR-Ludlow variants (`cNFWMCRLudlowSph`, `NFWMCRLudlowSph`,
`NFWTruncatedMCRLudlowSph`) subclass these and inherit the radial math, only
deriving `kappa_s` / `scale_radius` differently in `__init__`. So two radial
implementations cover all four profile *types*.

## What to build

A new script
`autolens_workspace_test/scripts/jax_substructure/test_deflections_equivalence.py`.

For each of the four profile types — `NFWTruncatedSph`, `cNFWSph`,
`NFWTruncatedMCRLudlowSph`, `cNFWMCRLudlowSph`:

1. Build ~10 halos on a single plane (shared redshift) as `ag.Galaxy` objects
   with realistic-but-distinct centres/masses via the normal Galaxy/profile API.
2. **Old path:** sum their deflections the existing way — e.g. via
   `tracer_util.traced_grid_2d_list_from(...)` or by summing
   `g.mass.deflections_yx_2d_from(grid=...)` over the galaxies (whichever the
   substructure path is meant to reproduce). Run with `xp=jnp`.
3. **New path:** `params, mask, _ = galaxies_to_halo_arrays(halos, [z], max_n, profile_cls)`
   then `profile_cls.vmapped_deflections_from(grid, params[0], mask[0])`.
4. Assert `jnp.allclose(deflections_old, deflections_new, atol=1e-8)` (loosen
   atol only if a profile's math genuinely needs it — document why).

Then a **masked-slot-zero** test: pad to `max_n > n_halos`, set the extra
`mask` entries `False`, and assert those padded slots contribute exactly zero to
the summed deflection (and that the result equals the unpadded sum).

## Known risk to verify first

`galaxies_to_halo_arrays` extracts `prof.kappa_s` / `prof.scale_radius` /
`prof.truncation_radius` / `prof.core_radius` directly off the built profile.
Confirm the MCR-Ludlow variants actually expose those attributes after
construction (they compute `kappa_s`/`scale_radius` from `mass_at_200` in
`__init__`, so they should — but `truncation_radius` vs `core_radius` naming and
the `else` branch must match each class). If an MCR class doesn't fit the
existing two-way branch, add a small explicit branch (or attribute-based
dispatch) to `galaxies_to_halo_arrays` — that's a tiny PyAutoLens library tweak
bundled into the same task and shipped alongside the workspace script.

## Tests / validation

This *is* the test — it runs under the `jax_substructure` smoke/integration set.
Run it locally with the JAX env (`NUMBA_CACHE_DIR` / `MPLCONFIGDIR` overrides)
and confirm all four profiles pass plus the masked-zero assertion. Keep it
consistent in structure with the existing `test_scan_multiplane.py` /
`test_simulate_e2e.py` in the same directory.

## Scope boundaries

- Deflections only (mass profiles) — no source light, PSF, or noise here.
- Single plane — multi-plane equivalence is already covered by
  `test_scan_multiplane.py`.
- Reuse the existing `galaxies_to_halo_arrays` + `vmapped_deflections_from`; only
  extend `galaxies_to_halo_arrays` if the MCR-variant risk above materialises.
