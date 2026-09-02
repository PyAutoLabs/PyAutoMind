# Precompute fixed-geometry Gaussian deflection angles and rescale by the free mass-to-light ratio (numpy + JAX)

Type: feature
Target: autogalaxy
Repos:
- @PyAutoGalaxy
- @PyAutoLens
- @autolens_profiling
Themes:
- numba-cpu
- mass-profiles
- jax
- profiling
Difficulty: large
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: with every Gaussian's centre/ell_comps/sigma fixed and only mass_to_light_ratio free, the second and later likelihood evaluations call no Faddeeva/`wofz` kernel (asserted by a call-count probe) and the deflections equal the per-evaluation path to rtol 1e-12 on the `scripts/lens/deflections/` pins.
Review-minutes: 25
Unattended: needs-slicing
Parent: draft/feature/autogalaxy/numpy_deflections_cpu_speedup.md
Filed: 2026-09-02

> Successor to the `numpy-deflections-cpu` epic (ledger at the Parent path; phase 1 = autoarray issue #514,
> PRs autoarray #516 / autogalaxy #595 / autolens #718 / autolens_profiling #210). **Start only after
> that epic's three phases are complete** — it is a separate follow-up, not an epic member, because it
> changes how a model's fixed vs free parameters reach the profile code and is likely to be complex.

## Idea (user, 2026-09-02, verbatim)

"we should intake a follow up issue which exploits the fact that if all of the Gaussian light profile
values are fixed and thus only their mass to light ratio is free in a model, we can precompute the
deflection angles and scale them up and down by a constant factor. This could be quite complex and
thus should be a separate follow up issue after this deflection speed up stuff is complete. Also likely
that JAX doesn't use this so would help there."

## Context

The Gaussian mass profile (`autogalaxy/profiles/mass/stellar/gaussian.py`, Faddeeva closed form via
`wofz`) and every MGE-decomposed mass profile (`autogalaxy/profiles/mass/abstract/mge.py`) evaluate the
full per-Gaussian deflection field on every likelihood call, even when the Gaussians' centres,
`ell_comps` and `sigma`s are fixed — the common SLaM case where an MGE lens light was fitted in an
earlier stage and the mass follows the light with a single free `mass_to_light_ratio`. The deflection
field is linear in the Gaussian amplitude, so a fixed-geometry Gaussian's deflections are a constant
vector (per grid) times the free scalar; a stack of N fixed Gaussians sharing one ratio collapses to one
precomputed summed field times the ratio.

Baseline (autolens_profiling `scripts/lens/deflections/`, hst grid 15,361 points, numpy,
`OMP_NUM_THREADS=1`, after phase 1): Gaussian 11 ms / call; gNFW via MGE-30 293 ms / call. Pins and the
`--repin` policy live there (PR #210).

## Levers to scope

1. Detect fixed geometry from the model: prior vs constant (the model's own parameter kinds) on each Gaussian's centre,
   `ell_comps`, `sigma` (and, for MGE-decomposed profiles, the parent's geometry); the free scalar is
   `mass_to_light_ratio` (or the MGE amplitude prefactor).
2. Cache the unit-amplitude deflection field per (grid identity, Gaussian geometry) across likelihood
   evaluations — same cross-evaluation memo shape as `nnls_memo.py` / the operated-matrix memo; key on
   the grid's shape/mask fingerprint and the fixed parameters, kill-switch env var.
3. Rescale by the free ratio per evaluation; N fixed Gaussians with one shared ratio sum once.
4. JAX: a cached unit field becomes a constant folded into the trace (the deflection subgraph
   disappears), so the win is likely larger there than on numpy — measure both.
5. Where the geometry is *not* fixed, nothing changes.

## Gates

Deflections bit-identical (the rescale is one multiply; pins rtol 1e-6 in `scripts/lens/deflections/`);
likelihood pins on the numba cells unchanged; measure numpy and JAX before/after; `test_autogalaxy` /
`test_autolens` green; no new public API beyond what the cache needs.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/d3971bba-0e8d-4c4f-bc59-7808e6bfa6cd/scratchpad/intake_gaussian_precompute.md -->
