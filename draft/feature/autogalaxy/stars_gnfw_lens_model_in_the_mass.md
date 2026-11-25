# Stars + gNFW lens model in the mass-sheet-normalised frame (from stars_dm_slope)

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: A unit test shows the new stars + gNFW mass-sheet-frame profile gives deflections equal to `(stars + gNFW deflections) / lambda_0 + (1 - 1/lambda_0) * (grid - centre)` to 1e-10 on NumPy and JAX, and a workspace example fits a simulated lens with it and recovers the input dark-matter fraction.
Review-minutes: 3
Unattended: needs-slicing
Lane: any

The science project `stars_dm_slope` (Cortex key `stars_dm_slope`, folder
`~/Science/Science/complete/stars_dm_slope`, closed 2026-11-25) searched for the best way
to parameterise a stellar (Sérsic, mass follows light) + dark matter (gNFW) lens model. Its
recommendation, confirmed by the maintainer on 2026-11-25, is to fit the model in a
**mass-sheet-normalised frame**. The prototype lives in the project and is to move into the
library, because a follow-up science project on HST data is waiting for it.

Read first, in the project folder:

- `wiki/project/recommendation.md` — definitions, default priors, evidence.
- `scripts/parameterisations.py` — the prototype (JAX-traceable, used in over 300 Nautilus
  fits on RAL): `StarsGNFWMSTFrame`, `lambda0_terms`, `kappa_ring_from`, `SersicLinearML`,
  `SersicApertureMass`, `gNFWApertureMassSph`, `gnfw_unit_aperture_mass`, `hyp2f1_pfaff`,
  `with_stable_prior_order`, `model_from`.
- `scripts/pilot_fit.py` (`FramePositionsLH`) and `scripts/scratch/test_inv_frame.py` (the
  frame's own tests and Hessian check).
- `wiki/project/2026-11-16-parameterisation-and-systematics.md` — the research note.

## Why

Along the likelihood valley of a stars + halo model the solutions differ by an approximate
mass-sheet transformation. The source plane is rescaled by λ ∝ 1 − kappa_ring(theta_ap), so
the posterior widths of the source centre, the shear and the aperture mass scale with λ and
their volume goes as (1 − kappa_ring)⁵. Sampled in ordinary units, that volume tilts the
inner-slope posterior steep (by 0.2–0.3 in the median on Euclid-like mocks; 24 of 27
recovery fits pass). In the normalised frame 27 of 27 pass and the tilt goes.

## What to build

1. **The frame profile.** A mass profile for Sérsic stars + spherical gNFW halo on the same
   centre, fitted as the mass-sheet transform of the pair by 1 / λ₀:

       kappa'(theta) = kappa(theta) / λ₀ + 1 − 1 / λ₀
       alpha'(theta) = alpha(theta) / λ₀ + (1 − 1 / λ₀) (theta − centre)

   λ₀ = 1 − kappa_ring(theta_ap) of the stars + halo at the nominal aperture mass
   m_ap = π theta_ap², so it depends on the shape only (slope, dark fraction, scale radius,
   light), not on the sampled mass; floored at 0.02. Three library components: the stars
   with M/L / λ₀, a `gNFWSph` with kappa_s / λ₀, a `MassSheet` of convergence 1 − 1 / λ₀.
   Sampled: `eps` (fractional offset of the transformed aperture mass, U(−1, 1)), `f_dm`
   (dark fraction of the projected mass inside `theta_f`, U(0, 1)), `inner_slope`
   (U(0, 2.5)), `scale_radius` (fixed by default). `theta_ap` is a fixed aperture near the
   Einstein radius; `theta_f = theta_ap` gives the angular form, `theta_f` = 5 kpc in arcsec
   the physical form. The profile must expose the physical quantities
   (`mass_to_light_ratio_physical`, `kappa_s_physical`, `m_ap_physical`, `lambda0`).
   In this frame the external shear and the source plane are the physical ones divided by
   λ₀: default priors used were shear U(−0.6, 0.6) and source centre U(−3″, 3″). The
   positions penalty must follow: the project divides its source-plane threshold by λ₀
   (`FramePositionsLH`).
2. **The pieces it is made of**, where the library lacks them: the ring convergence from
   deflections (`kappa_ring_from`, 64 azimuthal points, JAX-traceable), a Sérsic and a gNFW
   normalised by projected mass inside an aperture (`SersicApertureMass`,
   `gNFWApertureMassSph`; with PyAutoFit compound priors `(1 − f_dm) * m_ap` and
   `f_dm * m_ap` they give the ordinary-units form P1, kept as the comparison).
3. **A JAX-safe 2F1 for the gNFW enclosed mass.** `jax.scipy.special.hyp2f1` returns inf or
   ~1e167 for z < −1 (jax 0.12). The project uses the Pfaff transformation
   (`hyp2f1_pfaff`), which agrees with SciPy to 1e-15 for 0 ≤ slope ≤ 2.4. The library
   already works around this in its own gNFW code (PyAutoGalaxy #722–#730); check whether
   one shared helper should serve both.
4. **A workspace example** in `autolens_workspace`: simulate a stars + gNFW lens, fit it in
   the frame, convert the result back to physical units, and say when to use it.

## Slices

1. **Building blocks.** A shared JAX-safe 2F1 helper for the gNFW enclosed mass, the ring
   convergence from deflections, and the Sérsic and gNFW profiles normalised by projected
   mass inside an aperture. *Repos:* PyAutoGalaxy
   *Witness:* unit tests show the 2F1 helper matches `scipy.special.hyp2f1` to 1e-12 for slopes 0 to 2.4 on NumPy and JAX, and each aperture-normalised profile encloses its `mass_ap` inside `theta_ap` to 1e-8.
2. **The mass-sheet-frame profile.** The stars + gNFW profile in the normalised frame, its
   λ₀ helper, the physical-unit attributes, and the positions penalty scaled by 1 / λ₀.
   *Repos:* PyAutoGalaxy, PyAutoLens
   *Witness:* a unit test shows its deflections equal `(stars + gNFW deflections) / lambda_0 + (1 - 1/lambda_0) * (grid - centre)` to 1e-10 on NumPy and JAX, and the ring convergence of the transformed lens at `theta_ap` is zero to 1e-6 at `eps = 0`. *Depends:* 1
3. **Workspace example.** Simulate a stars + gNFW lens, fit it in the frame, convert the
   result back to physical units. *Repos:* autolens_workspace
   *Witness:* the example runs in smoke and recovers the input dark-matter fraction inside its 95% interval. *Depends:* 2

## Design questions for the plan

- The prototype is one composite profile holding stars + halo + sheet with the light shape
  passed in as fixed numbers. Decide the library form: a composite mass profile as
  prototyped, or a general "mass-sheet frame" wrapper around any list of mass profiles with
  λ₀ from their ring convergence. The second is more general but must keep λ₀ independent
  of the sampled mass.
- Free lens light: every project fit fixed the light to the truth. With free light, λ₀
  depends on the light parameters; the prototype handles this on the JAX path
  (`lambda0_terms`) but it was never fitted.
- Elliptical halo and an M/L gradient are out of scope here (untested in the project).

## Already known and related

- Reloading a model with compound or replaced priors reorders them
  (`draft/bug/autofit/a_compound_prior_model_reloaded_from_model.md`). The prototype works
  around it with `with_stable_prior_order`; the library version should not need to.
- `jax.scipy.special.hyp2f1` itself stays wrong for z < −1; never call it directly.
- The gNFW MGE deflection error grows above slope 2 (6% at 2.4): the slope prior stops at
  2.5 and the project's conclusions use slopes ≤ 2.

## What the project verified (carry these as tests)

- Image-plane invariance: at the truth, the optimised log likelihood of the frame model is
  within 0.10–0.24 of the ordinary-units model on three mocks (the difference is the
  optimiser's polish, not an exact identity test; the library version should test the
  deflection identity directly).
- The maps between the frame parameters and (slope, f_dm, r_s, m_ap) use the same λ₀ floor
  in both directions (`scripts/scratch/test_inv_frame.py tests` passes).
- On a Euclid-like mock the spread of the nuisance log-determinant along the likelihood
  ridge fell from 18.97 (ordinary units) to 0.63 (frame).
- 27 of 27 Nautilus recovery fits pass (9 mocks × 3 seeds, n_live 400, 11 min a fit on
  4 CPUs with the JAX likelihood).

## Not in this task

The follow-up science project on HST data (a new Cortex project, to start once item 1 has
shipped); an M/L gradient; any change to how many-lens results are combined.

<!-- formalised by the Intake (Conception) Agent on 2026-11-25 from file:/mnt/c/Users/Jammy/Workspace/Science/development/stars_dm_slope/wiki/project/upstream_prompt.md -->
