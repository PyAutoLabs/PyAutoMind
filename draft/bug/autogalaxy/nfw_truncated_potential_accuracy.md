# `NFWTruncatedSph.potential_2d_from`: MGE potential fails `grad(psi)=alpha` self-consistency

Type: bug
Target: PyAutoGalaxy
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

Pre-existing accuracy bug surfaced while fixing the missing dark-matter
potentials (PyAutoGalaxy `feature/dark-matter-potentials`, the
`NFW`/`gNFW`/`gNFWSph` + `NFWSph` work). `NFWTruncatedSph` already *has* a
`potential_2d_from` (it is not missing), but the value it returns is not
self-consistent with its own deflection field.

## Symptom

`autolens_workspace_test/scripts/mass/dark.py` runs the source-independent
self-consistency checks `div(alpha)=2 kappa`, `grad(psi)=alpha`,
`lap(psi)=2 kappa` by finite differencing. With all the
`feature/dark-matter-potentials` fixes in place the sweep is:

```
| Profile          | div(a)=2k | grad(p)=a            | lap(p)=2k |
| NFW              | PASS      | PASS med=8.1e-04     | PASS      |
| NFWSph           | PASS      | PASS med=7.6e-04     | PASS      |
| gNFW             | PASS      | PASS med=8.5e-04     | PASS      |
| gNFWSph          | PASS      | PASS med=8.1e-04     | PASS      |
| cNFW             | PASS      | PASS med=7.9e-04     | PASS      |
| cNFWSph          | PASS      | PASS med=6.9e-04     | PASS      |
| NFWTruncatedSph  | PASS      | FAIL med=7.1e-02 max=1.4e-01 | PASS (med=3.3e-02) |
```

Every NFW/gNFW/cNFW variant passes `grad(psi)=alpha` at med ~8e-4 except
`NFWTruncatedSph`, which is ~100x worse (med 7.1e-2). `div(alpha)=2 kappa`
passes, so the deflection field is fine; only the potential is off.

## Where the code lives

`autogalaxy/profiles/mass/dark/nfw_truncated.py`, `potential_2d_from`
(currently ~line 137). It uses the MGE decomposition exactly like `cNFW`:

```python
radii_min = self.scale_radius / 1000.0
radii_max = self.truncation_radius * 5.0
sigmas = xp.exp(xp.linspace(xp.log(radii_min), xp.log(radii_max), 30))
mge_decomp = MGEDecomposer(mass_profile=self)
return mge_decomp.potential_2d_via_mge_from(
    grid=grid, xp=xp, sigma_log_list=sigmas,
    ellipticity_convention="major", three_D=True,
)
```

## Likely cause / where to look

The MGE sigma range is the prime suspect. `cNFW` uses
`scale_radius/1000 .. scale_radius*200` (20-30 Gaussians); the truncated
profile caps `radii_max` at `truncation_radius * 5`, which is much
narrower and may not capture the deflection-relevant range, biasing the
radial potential integral. The convergence/deflection MGE for the same
profile presumably uses a different (wider) range — compare them.

## Plan

1. Reproduce on clean `main` first (this is pre-existing — confirm it is
   not a regression from the `feature/dark-matter-potentials` merge).
2. Widen / refine the `sigma_log_list` for the potential to match the
   range used by `NFWTruncatedSph`'s convergence/deflection decomposition,
   re-run `dark.py` (full mode, `rtol=1e-2`) until `grad(psi)=alpha` and
   `lap(psi)=2 kappa` both PASS at the same ~1e-3 med as the other NFW
   variants.
3. Cross-check the corrected potential against the spherical truncated-NFW
   analytic potential if a closed form exists (Baltz, Marshall & Oguri
   2009 give the BMO/truncated-NFW lensing potential).
4. Add a `test__potential_2d_from` assertion to
   `test_autogalaxy/profiles/mass/dark/test_nfw_truncated.py`.

## Validation

`PYAUTO_MASS_MODE=full python scripts/mass/dark.py` in
`autolens_workspace_test` — the `NFWTruncatedSph` row must flip
`grad(p)=a` from FAIL to PASS, joining the other dark profiles at ~1e-3.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
