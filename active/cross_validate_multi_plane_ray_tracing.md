# Cross-validate multi-plane ray tracing

Type: test
Target: PyAutoLens
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
Themes:
- ci-smoke
- notebooks
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Model: Fable (research-grade — paper reading + derivation + narrative guide prose)
Issued: 2026-08-29
Filed: 2026-08-27

Single-plane lensing quantities in this stack are cross-validated two independent ways.
Multi-plane ray tracing is not validated against anything. Build that, then publish it as
a @autolens_workspace guide.

## The analogue that already exists

@PyAutoGalaxy `test_autogalaxy/profiles/mass/total/test_isothermal.py::test__shear_yx_2d_from__matches_via_hessian`
is the pattern to copy:

```python
shear_analytic    = mp.shear_yx_2d_from(grid=grid)
shear_via_hessian = LensCalc.from_mass_obj(mp).shear_yx_2d_via_hessian_from(grid=grid)
np.testing.assert_allclose(shear_analytic, shear_via_hessian, rtol=1e-3, atol=1e-6)
```

Its docstring states the value plainly: the two paths "must agree to within
finite-difference accuracy", and the cross-check "guards against either path silently
drifting (e.g. a sign flip, a column swap, or a rotation-frame mistake)". A closed-form
formula and a numerical derivative of the deflections are wrong in *different* ways, so
agreement is evidence, where either alone is only self-consistency.

**Multi-plane has no such second opinion.** `tracer_util.traced_grid_2d_list_from` and
its scaling factors are the only implementation of the multi-plane recursion, and every
downstream quantity — `deflections_between_planes_from`, plane-bound magnification,
`plane_index_via_redshift_from` — is tested against *itself* or against pinned literals
produced by the same code.

## Why now: this cost us four months

PyAutoLens#480 (fixed 2026-08-27, `complete/2026/08/point-solver-magnification-plane-redshift.md`)
was a plane-mismatch in exactly this machinery that survived four months in a core path.
Two things about how it was finally settled motivate this task:

1. **The ray-traced Jacobian was the oracle that resolved it.** Central-differencing
   `theta -> beta_j` through `traced_grid_2d_list_from` and taking `mu = 1/det(J)` shares no
   code with the Hessian path, and it agreed with exact JAX autodiff to 1.8e-09. That
   one-off cross-check is the seed of this task; it should be a permanent, general
   fixture rather than something rebuilt by hand each time.
2. **The control arm found a second, unrelated bug.** Running the same comparison at the
   *last* plane exposed `LensCalc._hessian_via_richardson`'s hardcoded 0.01" step being
   off by 122% with the wrong sign on three of four points
   (`draft/bug/autogalaxy/lenscalc_numpy_hessian_step_is_too_coarse.md`). A systematic
   cross-validation would have caught that years ago.

## What to build

Compute the same multi-plane quantities by several genuinely independent routes and
assert they agree. Independence is the whole point: a route that reuses
`traced_grid_2d_list_from` is not a second opinion.

Candidate routes, to be settled during the task:

- **The implementation** — `tracer.traced_grid_2d_list_from` / `deflections_between_planes_from`.
- **A from-scratch multi-plane lens equation**, written directly from a paper's equations
  against explicit angular-diameter distances, deliberately NOT sharing the codebase's
  scaling-factor helper. This is the primary independent arm.
- **Numerical Jacobian** of `theta -> beta_j`, `mu = 1/det(J)` (validated on #480; stable
  across h from 1e-4 to 1e-7).
- **Exact JAX autodiff** (`jacfwd`), which needs `jax_enable_x64` to be meaningful —
  float32 gave 1.6e-02 residuals where float64 gave 1.8e-09.
- **Degenerate-case reductions**, the cheapest and sharpest checks:
  - a multi-plane tracer with all mass in one plane must reduce to the single-plane
    result, where the existing analytic closed forms apply;
  - a two-plane tracer must match the two-plane formulas exactly;
  - a deflector sitting *at* plane j must not affect the mapping *to* plane j (verified
    incidentally during #480: mu at z=1.0 was identical with and without source_0's mass).
- **Analytic multi-plane configurations** where a closed form exists (e.g. aligned
  isothermal spheres giving a double Einstein ring) — the strongest arm where available.

Quantities to cover: traced positions per plane, `deflections_between_planes_from`,
magnification at each plane, convergence/shear at each plane, and time delays if
`draft/feature/autolens/multi_plane_time_delays.md` has landed by then.

## Papers — pair against the literature, do not re-derive from the code

The point is to check the implementation against the *published* formalism, so the
equations must come from the papers, not from reading our source and transcribing it.

The one certain starting point: the codebase already cites
`https://inspirehep.net/literature/419263` for its equations 55 and 60 (Hessian and
magnification) in `autogalaxy/operate/lens_calc.py`. Start there, since it is the
reference the current code claims to implement.

Then survey the standard multi-plane formalism. Candidate references to locate and
verify — **treat this list as leads to confirm, not as established citations**:
Blandford & Narayan (1986); Schneider, Ehlers & Falco, *Gravitational Lenses*;
Schneider (2014) on multi-plane lensing; McCully et al. (2014) on multi-plane algorithms;
Petkova, Metcalf & Giocoli (2014) (GLAMER). Cross-reading `lenstronomy`'s multi-plane
implementation is also worthwhile as a second independent codebase.

Record which convention each source uses. The likely source of confusion — and worth
settling explicitly early — is **deflection normalisation**: our
`deflections_between_planes_from` returns `traced_grids[i] - traced_grids[j]`, i.e.
scaled against the final plane, so it is NOT the physical deflection at plane j in the
convention some papers use. Concretely, during #480 the obvious cross-check of truncating
the tracer to planes <= j gave 1.86 where the correct answer was 27.9. That is not a bug,
it is a convention mismatch — and it is exactly the kind of thing this task must
document rather than trip over.

## Deliverable: a workspace guide

This ends as a @autolens_workspace guide, not only a test module. Multi-plane
ray-tracing conventions are exactly the thing users get wrong and we have nothing
explaining them. Route the authorship through `/workspace` for placement, audience
register and the sibling guide to mirror.

The guide should carry: the multi-plane lens equation as the papers state it, how our
scaling factors map onto it, the convention traps above (with the 1.86-vs-27.9 worked
example), and the cross-validation itself as runnable, inspectable code — a reader
should be able to check the library themselves.

Split at start_dev time: the library test module and the workspace guide are one prompt
here but likely two PRs, library first.

## Suggested scope

1. Read the papers, fix the notation, write down the multi-plane lens equation and the
   magnification/Jacobian at an arbitrary plane in the paper's convention.
2. Map our implementation onto it and document every convention difference explicitly.
3. Implement the independent arms as reusable fixtures.
4. Add the cross-validation tests, covering the degenerate reductions first (cheap, sharp)
   and the general multi-plane case second.
5. Report any disagreement as a finding, not as a test to loosen. #480 and the Richardson
   step bug both say the implementation is the more likely party to be wrong.
6. Author the workspace guide via `/workspace`.

<!-- Sizing: large. The tests are tractable; establishing the formalism from the
     literature and settling the conventions is the real work, and it is research-grade. -->

<!-- formalised by the Intake (Conception) Agent on 2026-08-27 from file:/tmp/claude-0/-home-user/73120990-acb3-5546-bddd-2d75b5a0c771/scratchpad/intake4.md -->
