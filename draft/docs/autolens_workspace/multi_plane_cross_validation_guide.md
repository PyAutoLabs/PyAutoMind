# Publish the multi-plane cross-validation as a workspace guide

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- notebooks
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-29
Depends-on: PyAutoLens#714 (phase 1)

Phase 1 (PyAutoLens#714) settled the multi-plane conventions and built the independent
oracles as a library test module,
`PyAutoLens/test_autolens/lens/test_multi_plane_cross_validation.py`. Phase 2 publishes
them where users will actually meet them: multi-plane ray-tracing conventions are exactly
the thing people get wrong, and the workspace has nothing that shows a reader how to check
their own answer.

## Where it goes

**Extend the existing `scripts/guides/advanced/multi_plane.py`. Do not create a sibling
guide.** That script already opens by citing Schneider, Ehlers & Falco 1992 §9.1 equations
(9.6)/(9.7b), walks the recursion with simplified copies of the source code, and closes
with `__Lensing Units vs Physical Units__`, `__The PyAutoLens Convention__`,
`__Profiles With Physical Units__` and `__Science Corollaries__`. The cross-validation is
the natural next question for that same reader — "how do I know any of this is right?" —
and splitting it into its own guide would duplicate the setup and the formalism.

Add a `__Cross Validation__` section **after `__Science Corollaries__`** and before
`__Attribution__`, and add its bullet to the `__Contents__` list at the top of the module
docstring. Keep the existing `__Env__` block last and untouched.

## What the section must carry

### 1. The settled formalism and the two convention traps

Paste the formalism and convention text **verbatim** from the phase-1 module docstring
(`test_autolens/lens/test_multi_plane_cross_validation.py`) — it was written from the
papers rather than transcribed from the source, and phase 1 exists so it does not have to
be re-derived. It covers:

- SEF 1992 §9.1 eqs (9.6)/(9.7b): `theta_j = theta_1 - sum_{i<j} beta_ij alpha_i(theta_i)`
  with `beta_ij = (D_ij D_s) / (D_j D_is)`, `D_s` the **final** plane — hence `beta_ij = 1`
  when `z_j = z_final` and `beta_ij = 0` when `z_i = z_j`.
- Narayan & Bartelmann 1996 (https://inspirehep.net/literature/419263) eqs 55 and 60:
  `A = I - H`, `kappa = 1 - tr(A)/2`, `gamma_1 = (H_xx - H_yy)/2`, `gamma_2 = H_xy`,
  `mu = 1/det(A)`.
- McCully, Keeton, Wong & Zabludoff 2014 (arXiv:1401.0197): `A_1 = I`,
  `A_j = I - sum_{i<j} beta_ij U_i A_i` with `U_i = d alpha_i / d theta` at `theta_i`.
- **Trap (a):** `Tracer.deflections_between_planes_from(plane_i=i, plane_j=j)` returns
  `traced_grids[i] - traced_grids[j]` — the final-plane-scaled *difference* of positions,
  NOT the physical deflection at plane `j`.
- **Trap (b):** truncating a tracer to planes `<= j` changes `redshift_final` and therefore
  every `beta_ij`, so it is not an oracle for plane `j`.

Prose register: the guide's existing voice (second half is discursive and worked-example
led), not test-module terseness. This is tutorial prose — write it in-session per the
`WORKFLOW.md` prose split rather than delegating it.

### 2. The 1.86-vs-27.9 worked example

The sharpest thing in the whole task, and the reason trap (b) is worth a section. During
PyAutoLens#480 the obvious cross-check — truncate the tracer to the planes up to `j` and
ask for the magnification there — returned **1.86** where the correct value is **27.9**, a
factor of 15, from a convention mismatch rather than a bug. Show it as runnable code: build
the truncated tracer, print the wrong number, build the full tracer with `plane_j=j`, print
the right one, and explain that the betas silently changed because `D_s` moved. A reader who
has hit this will recognise it immediately; one who has not is about to.

### 3. The cross-validation arms, as runnable, inspectable code

Port the oracles from the phase-1 module (they are deliberately self-contained functions):

- **astropy arm** — `beta_ij` from `astropy.cosmology.Planck15.angular_diameter_distance`,
  against `ag.cosmo.Planck15().scaling_factor_between_redshifts_from`. State the measured
  agreement: **~2e-7 relative**, set by the two cosmologies' differing quadrature (the
  project integrates `1/E(z)` by a hand-rolled Simpson rule), with all six Planck15
  parameters matching astropy exactly. That 2e-7 is why phase 1 runs the paper recursion
  twice — with astropy betas at 1e-6 and with the project's own betas at 1e-10 — and the
  guide should explain that split, because it is the difference between testing the
  cosmology and testing the ray-tracing algebra.
- **paper-recursion arm** — the SEF recursion written out, using each galaxy's single-plane
  `deflections_yx_2d_from`, matching `traced_grid_2d_list_from` to 1e-10.
- **numerical-Jacobian arm** — central differences of `theta -> beta_j` with
  `mu = 1/det(J)`; show the h-stability sweep across `h` in 1e-4…1e-7, since an oracle that
  is not step-stable is not an oracle.
- **McCully recursion arm** — the Jacobian propagated plane by plane, giving `mu`, `kappa`
  and `gamma` without ray-tracing a single perturbed position.
- Optionally the **double Einstein ring** closed form (two aligned isothermal spheres,
  ring radii `theta_E1 + theta_E2` and `theta_E1 - theta_E2` when
  `theta_E2 > (1 - beta_01) theta_E1`) — the only arm with an exact analytic multi-plane
  observable, and it makes a good figure.

### 4. The JAX `jacfwd` arm, under `ENV: jax`

Phase 1 is numpy-only by the unit-test contract, so the exact-autodiff arm lands here.
Force float64 with `from autolens import jax_wrapper` before anything else — float32 gave
1.6e-02 residuals where float64 gave 1.8e-09 on this exact comparison. Put it in its own
subsection whose ENV declaration is `ENV: jax`, so the smoke runner skips it on the nojax
leg.

### 5. Mention the known defect

`LensCalc._hessian_via_richardson`'s hardcoded `buffer=0.01` arcsec step is pinned as a
strict xfail in phase 1
(`PyAutoMind/draft/bug/autogalaxy/lenscalc_numpy_hessian_step_is_too_coarse.md`). It is
reproducible from the guide's own machinery: where a ray passes ~4e-4 arcsec from a compact
deflector's centre the NumPy Hessian returns
`[-0.00694, -0.00221, 0.00139, 0.00246]` where exact autodiff and the ray-traced Jacobian
both give `[0.04508, 0.01099, -0.08602, -0.01118]` — wrong by ~100-120% with a flipped
sign on all four points. A one-paragraph warning with the numbers, pointing at the JAX path
for compact multi-plane configurations, is worth more to a user than silence. Do not
present it as fixed; it is not.

## Housekeeping

- Regenerate the notebook per the workspace convention (`autolens_workspace/AGENTS.md`,
  *Generating notebooks*), from the workspace root:
  `PYTHONPATH=../PyAutoHands/autohands python3 ../PyAutoHands/autohands/generate.py autolens`,
  and commit `notebooks/guides/advanced/multi_plane.ipynb` alongside the script. Never edit
  the `.ipynb` directly.
- The guide already declares `ENV: full_datasets` in its `__Env__` block; the new JAX
  subsection needs its own `ENV: jax` declaration, and the `__Env__` block stays last.
- Run the script before shipping. Note it is NOT in `smoke_tests.txt` (that list is a
  curated subset), but it is also not in `config/build/no_run.yaml`, so the full workspace
  CI run does execute it — keep the new section cheap and free of long fits.
