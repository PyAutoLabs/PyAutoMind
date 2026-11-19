# Substructure jax.grad is NaN when a zero-padded halo slot exists

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: A test builds two planes with 2 and 5 NFWTruncatedSph halos, packs them with `galaxies_to_halo_arrays(max_n=8)` (so padded slots exist), and asserts `jax.grad` of the summed multi-plane deflection with respect to the grid and with respect to every real halo's params is finite and matches the gradient computed with no padding (max_n equal to each plane's count) to 1e-10 in float64; a second test asserts finite `jax.grad` through `cNFWSph.vmapped_deflections_from`.
Review-minutes: 3
Unattended: ready
Lane: any

## Finding

`@PyAutoLens/autolens/lens/substructure_util.py:108` pads halo params with `np.zeros` (mask False),
so a padded `NFWTruncatedSph` slot has `scale_radius = 0`. Measured by the independent adversary
review (Fable 5.2) of shift 2026-11-19-pm, on PyAutoLens main and on the PyAutoGalaxy#737 branch:

- d/dgrid through `NFWTruncatedSph.vmapped_deflections_from`
  (`@PyAutoGalaxy/autogalaxy/profiles/mass/abstract/abstract.py:62-71`) is NaN whenever any padded
  slot exists: `max_n=5` (no padding) finite, `max_n=8` NaN. d/dparams of the real halos is finite
  on the #737 branch.
- `max_n=None` (PyAutoLens#870) does not help: planes below the fullest are still padded.
- `cNFWSph` gradients through the same vmapped hook are NaN even without padding
  (d/dparams `[nan, nan, 1.86, nan, nan]`), on main and on #737.

The deflection values are correct (padded slots contribute exactly 0.0); only gradients break.

## Why it matters

Gradient-based line-of-sight / subhalo fits (HMC, gradient optimisers, Fisher forecasts) through
the batched substructure path get NaN as soon as planes hold different halo counts — which is
always.

## Ask

1. Make masked slots gradient-safe: pad with benign non-zero params (e.g. `scale_radius = 1`,
   `kappa_s = 0`) or guard them with a safe double-`where`, so a masked slot's value AND gradient
   are exactly zero.
2. Find and fix the `cNFWSph` NaN gradient in the vmapped path.
3. Add the witness tests (jax-only tests skip without jax).

## Provenance

[from: independent adversary review, Fable 5.2, shift 2026-11-19-pm] notes on PyAutoLens#870 and
finding F2 on PyAutoGalaxy#737; record `batches/2026-11-19-pm.md`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cef12910-5f37-434a-b812-60fddb7f44b6/scratchpad/intake/substructure_padded_slot_grad_nan.md -->
