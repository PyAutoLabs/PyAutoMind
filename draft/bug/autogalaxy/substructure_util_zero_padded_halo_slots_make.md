# substructure_util zero-padded halo slots make jax.grad NaN for every halo

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: A unit test builds padded halo arrays with `galaxies_to_halo_arrays` for a population in which at least one plane has unused slots, takes `jax.grad` of a scalar function of the source-plane grid from `traced_grids_via_scan` with respect to `halo_params`, and asserts every gradient entry of a real (unmasked) halo is finite and every masked slot's gradient is exactly zero; the forward traced grids are unchanged to 1e-12 against the current values.
Review-minutes: 3
Unattended: ready
Verified: 2026-11-24 1ba51f32 (PyAutoGalaxy), dbc63e65 (PyAutoLens)
Lane: any

## Finding

`@PyAutoLens/autolens/lens/substructure_util.py` `galaxies_to_halo_arrays` fills unused halo slots
with zeros. For `NFWTruncatedSph` a zero slot has `scale_radius = 0`, so inside
`@PyAutoGalaxy/autogalaxy/profiles/mass/abstract/abstract.py` `Profile.vmapped_deflections_from`
the slot's radial deflection evaluates `r / 0` and `tau = 0 / 0`. The forward pass is saved by the
final `xp.where(mask, all_defl, 0.0)`, but in reverse mode JAX multiplies the zero cotangent of the
masked branch by the NaN partial derivative, and the NaN flows back into the shared grid and from
there into every halo.

Measured 2026-11-20 on PyAutoLens `main` aa02375fa and PyAutoGalaxy `main` 5b85fbf0: a
line-of-sight population of 146 halos on 9 planes, padded to the fullest plane (214 unused slots),
100 grid points. `jax.grad` of `sum(traced_grids[-1]**2)` with respect to `halo_params` is NaN in
1800 of 1800 entries, 730 of them belonging to real halos. The forward value is finite. Replacing
the padding by finite values (`kappa_s = 0`, `scale_radius = 1`, `truncation_radius = 2`) gives 0
NaN of 1800.

## Why it matters

The scan path exists to be differentiated and batched under JAX. As it stands any gradient-based
use of it (HMC or variational inference over halo parameters, Fisher or Jacobian diagnostics,
gradient checks) returns NaN whenever one plane has fewer halos than `max_n`, which is every
realistic realisation. Nothing warns, because forward values are correct.

## Ask

1. Make masked slots safe before the profile is evaluated, not after: either pad with finite,
   zero-deflection parameters in `galaxies_to_halo_arrays` (per profile class; the extractor
   already knows the parameter layout), or substitute safe parameters for masked slots inside
   `vmapped_deflections_from` with `xp.where(mask[:, None], params, safe)` before the `vmap`.
   The second fixes every caller and every profile with a `radial_deflection_from`; choose it
   unless a profile has no parameter set that is both finite and deflection-free.
2. Check the other profile classes the extractor supports (`cNFWSph`, the Kaplinghat and Yang SIDM
   profiles) for the same zero-slot NaN.
3. Add the witness test.

Related: `draft/feature/jax_substructure/6_deflection_equivalence_test.md`.

## Provenance

[from: dm_sightlines science project, phase 2A, 2026-11-20] Found while testing the project's own
render layer, which pads with finite values. Reproduction script and log in the project:
`Science/development/dm_sightlines/results/phase2a_render/library_grad_nan.py` and
`library_grad_nan.log` (the script uses project helpers to build the population; the library
calls are `galaxies_to_halo_arrays(..., max_n=None)` and `traced_grids_via_scan`).

<!-- formalised by the Intake (Conception) Agent on 2026-11-20 from file:/tmp/claude-1000/-home-jammy-Science/4c8e2ded-c0f1-44a2-878a-797321efeaa7/scratchpad/raw/b6.md -->

## Answers from the human
- Q30 (2026-11-26, shift 2026-11-24-am question on PyAutoLens#871): retire https://github.com/PyAutoLabs/PyAutoLens/issues/871#issuecomment-7127151259
