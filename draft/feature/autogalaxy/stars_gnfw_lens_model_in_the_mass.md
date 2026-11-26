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
Witness: Unit tests show, on NumPy and JAX, that the general mass-sheet frame around stars + gNFW and around a power law traces a grid to `centre + (source-plane grid of the physical lens - centre) / lambda_0` to 1e-10, and a workspace example fits a simulated stars + gNFW lens with it and recovers the input dark-matter fraction.
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

1. **The frame.** One general mass profile (working name `MassSheetFrame`) that wraps a
   list of ordinary mass profiles and is fitted as their mass-sheet transform by 1 / λ₀:

       kappa'(theta) = kappa(theta) / λ₀ + 1 − 1 / λ₀
       alpha'(theta) = alpha(theta) / λ₀ + (1 − 1 / λ₀) (theta − centre)

   λ₀ = 1 − kappa_ring(theta_ap) of the wrapped profiles at the nominal aperture mass
   m_ap = π theta_ap², so it depends on their shape only, not on the sampled mass; floored
   at 0.02. Sampled on the frame: `eps` (fractional offset of the transformed aperture
   mass, U(−1, 1)). `theta_ap` is a fixed aperture near the Einstein radius.
   For the stars + gNFW model the wrapped profiles are item 2's aperture-normalised Sérsic
   and gNFW, sampled by `f_dm` (dark fraction of the projected mass inside `theta_f`,
   U(0, 1)), `inner_slope` (U(0, 2.5)) and `scale_radius` (fixed by default);
   `theta_f = theta_ap` gives the angular form, `theta_f` = 5 kpc in arcsec the physical
   form. A power law is wrapped the same way.
   In this frame the external shear and the source plane are the physical ones divided by
   λ₀: default priors used were shear U(−0.6, 0.6) and source centre U(−3″, 3″). The
   positions penalty must follow: the project divides its source-plane threshold by λ₀
   (`FramePositionsLH`). The design, the evidence for it and the physical quantities the
   frame must give are in "Assessment" below. The prototype is one composite profile,
   `StarsGNFWMSTFrame`; the composite is not built.
2. **The pieces it is made of**, where the library lacks them: the ring convergence from
   deflections (`kappa_ring_from`, 64 azimuthal points, JAX-traceable; the frame also needs
   the projected mass inside the ring from the same call, see "Assessment"), a Sérsic and
   a gNFW normalised by projected mass inside an aperture (`SersicApertureMass`,
   `gNFWApertureMassSph`; with PyAutoFit compound priors `(1 − f_dm) * m_ap` and
   `f_dm * m_ap` they give the ordinary-units form P1, kept as the comparison; with
   `1 − f_dm` and `f_dm` they are what the frame wraps). The Sérsic must be usable as a
   mass-only profile, because the frame holds the stars' mass and the galaxy holds their
   light.
3. **A JAX-safe 2F1 for the gNFW enclosed mass.** `jax.scipy.special.hyp2f1` returns inf or
   ~1e167 for z < −1 (jax 0.12). The project uses the Pfaff transformation
   (`hyp2f1_pfaff`), which agrees with SciPy to 1e-15 for 0 ≤ slope ≤ 2.4. The library
   already works around this in its own gNFW code (PyAutoGalaxy #722–#730); check whether
   one shared helper should serve both.
4. **A workspace example** in `autolens_workspace`: simulate a stars + gNFW lens, fit it in
   the frame, convert the result back to physical units, and say when to use it.
5. **Physical-units profiles** (M200 for the halo, a physical stellar mass or M/L for the
   stars): see "Physical-units parameterisation" below.

## Assessment: the mass-sheet rescaling is its own profile (done 2026-11-26)

Maintainer's steer (2026-11-25): the rescaling is general enough that we would want to
apply it to a power law too, and keeping it out of the Sérsic and dark-matter profiles
keeps the source cleaner. The assessment this section used to ask for was done on
2026-11-26 (a Fable session with the maintainer), against the prototype and the library.
**Result: the separation comes out clean. Build the general frame; do not build the
composite.** The numbers below come from
`~/Science/Science/scratch/mass_sheet_frame_assessment/general_frame_check.py`, which holds
a sketch of the object (not library code) and runs against the project's prototype.

### The object

`MassSheetFrame(profile_list, eps, theta_ap)` is a `MassProfile` in
`autogalaxy/profiles/mass/sheets/` that holds a list of ordinary mass profiles, as `Basis`
(`autogalaxy/profiles/basis.py`) does. It uses only their summed deflections `alpha`:

    m_1, k_1   = projected mass inside theta_ap and ring convergence at theta_ap of the profiles as given
    nominal    = π theta_ap² / m_1
    λ₀         = max(1 − nominal k_1, 0.02)
    mass_scale = nominal (1 + λ₀ eps)
    alpha'     = (mass_scale / λ₀) alpha + (1 − 1 / λ₀) (theta − centre)

with the same rescaling for the convergence and the potential. Both ring numbers come from
one deflection call on 3 × 64 points: the prototype's `kappa_ring_from` with a third ring
at `theta_ap` itself, where m = π theta ⟨alpha_r⟩. `centre` is the first profile's, as in
`Basis`. The physical lens is `mass_scale` × the wrapped profiles; its aperture mass is
m_ap = π theta_ap² (1 + λ₀ eps); the physical shear and source plane are the fitted ones
× λ₀. This is the prototype's algebra with the stars + halo sum replaced by any sum. It
relies only on deflections being linear in an overall amplitude.

### Which parameter is "the mass"

None of the wrapped profiles'. The frame normalises the summed field itself, so the
overall amplitude of the wrapped profiles has no effect on the lens (a power law with
`einstein_radius` 1.0 or 1.9 gives the same deflections to 1e-14) and `eps` is the only
mass parameter. So λ₀ depends on shape only for any profile, and:

- One amplitude is fixed per frame, or the likelihood is flat along it. For a power law
  fix `einstein_radius` (at 1). For stars + halo the two aperture masses are 1 − f_dm and
  f_dm.
- Every other wrapped parameter is shape and may be free, including one that changes mass
  and shape together (an NFW mass under a mass–concentration relation).
- `theta_ap` is fixed, near the Einstein radius (from an earlier fit or the arcs). `eps`
  is to first order (theta_E / theta_ap)² − 1, theta_E the Einstein radius: at
  eps = ±0.3 that expression is +0.33 and −0.28.

Considered, not adopted: sample the Einstein radius and take the ring there, with no fixed
aperture. It is simpler to explain, but it is not the form the project's 27 fits tested.
The two are close: at eps = ±0.3 the transformed ring convergence at the Einstein radius
is ±0.007 for stars + gNFW and zero for a power law.

### Stars + gNFW in the general frame

The dark-fraction split belongs to the model, not the frame. The wrapped pair is slice 1's
aperture-normalised Sérsic and gNFW with `mass_ap` = 1 − f_dm and f_dm inside `theta_f`,
one `f_dm` prior shared through PyAutoFit compound priors (the comparison form P1 is built
the same way, with `(1 − f_dm) * m_ap` and `f_dm * m_ap`). Free parameters as in the
prototype: `eps`, `f_dm`, `inner_slope`.

- **Equivalence with the prototype.** On four configurations (slope 0.4 to 2.0, f_dm 0.3
  to 0.8, eps −0.2 to 0.3, elliptical light, `theta_f` ≠ `theta_ap`) λ₀ agrees to 3e-8 and
  the deflections to 2.3e-7″ over a 4″ grid, so the project's 27 of 27 recovery result
  carries over. It is not 1e-10, for two reasons, neither a fault of the frame: the stars'
  mass inside `theta_ap` comes from ring deflections in place of the light quadrature
  (7e-8), and library `gNFWSph` deflections are linear in `kappa_s` only to 3–5e-8
  (`NFWSph` 3e-16, `mp.Sersic` in M/L 4e-14), so scaling the summed field differs at that
  level from building the halo with `kappa_s / λ₀`.
- **Compound priors.** The prior-order defect on reload
  (`draft/bug/autofit/a_compound_prior_model_reloaded_from_model.md`) applies to this
  model, as to any model with a prior replaced after construction. The prototype escaped
  it by having no shared priors. Slice 4 should not ship a workaround: queue that bug
  ahead of slice 4.
- **Light.** An `lmp` profile inside the frame gives the galaxy no light: a `Galaxy` finds
  light profiles among its own attributes only (checked: empty light-profile list, zero
  image). So the wrapped stars are a mass-only profile and the galaxy's light is a
  separate light profile with the same parameters, passed as an instance when the light is
  fixed (every project fit) and through shared priors when it is free. Do not make the
  frame a `LightProfile` or a `Basis` subclass in this task.

### A power law in the general frame

`af.Model(MassSheetFrame, profile_list=[af.Model(PowerLaw)], eps=..., theta_ap=...)` with
`einstein_radius` fixed composes and makes instances: 6 free parameters (centre,
`ell_comps`, `slope`, `eps`). For a circular power law λ₀ = (slope − 1) / 2 whatever the
aperture, recovered to 1e-7; the floor is reached at slope 1.04, so keep the slope prior
above about 1.2. An elliptical power law (`ell_comps` up to (0.3, 0.1), centre off the
origin) gives mean convergence 1 + eps inside `theta_ap` and zero ring convergence at
eps = 0; the ring convergence from deflections agrees with the analytic convergence to
1e-7.

This is tested as software only. No recovery fit of a power law in the frame exists. The
volume argument predicts that a power-law fit in ordinary units favours steep slopes by
λ₀⁴ ∝ (slope − 1)⁴ (source centre and shear; the Einstein radius is unchanged by a
mass-sheet transformation), a shift of about 4 σ² / (slope − 1) in a slope measured to σ:
0.01 for σ = 0.05 at slope 2, 0.04 for σ = 0.1. That is the assessing agent's
extrapolation, to be tested in a science project; it is not for the documentation.

### Where it lives, and cost

- Rejected: a galaxy-level option (it would change `MassProfileAggregate`, the mass sums
  `Galaxy` and `MassField` share, for every model, and which profiles are rescaled would
  be implicit); and a model-composition helper alone (λ₀ depends on the sampled values
  through a ring integral, which priors cannot express).
- A `Galaxy` holding the frame and an `ExternalShear` sees those two mass profiles; the
  wrapped ones are not counted twice.
- Compute λ₀ inside the lensing methods, where `xp` is known (for example a
  `lambda0_from(xp)` method), not in the constructor: a PyAutoFit model cannot pass `xp`
  to a constructor, and the prototype's sniffing of its input types (`xp_for`) is not to
  be copied.
- JAX: `jax.jit` and forward gradients work with every power-law parameter traced, the
  centre included (the ring grid is then traced), and for stars + gNFW with `f_dm`,
  `inner_slope` and `eps` traced. Cost: one deflection call on 192 points per evaluation,
  against thousands on the image grid. Call the wrapped profiles through
  `deflections_memo.deflections_yx_2d_from`, as `Basis` and `Galaxy` do. The prototype's
  hand cache of the stars' ring term (`_sersic_unit_terms`) is not carried over.
- Also needed: a prior config in `autogalaxy/config/priors/mass/sheets/`, notation labels,
  JAX pytree registration (follow `Basis`, which also holds a `profile_list`), the
  `ag.mp` / `al.mp` export and the API docs.

### What goes with the frame

- **Everything outside the frame is in frame units.** The external shear, the source
  plane and any other mass in the lens plane are fitted as physical / λ₀. The shear does
  not go inside `profile_list` (it would be multiplied by `mass_scale`).
- **Positions penalty** (PyAutoLens `autolens/analysis/positions.py`): `PositionsLH`
  divides its threshold by the λ₀ of the frame it finds in the lens galaxies. With no
  frame nothing changes (pin this with a test); more than one frame in a tracer raises.
- **Priors.** The shear and source-centre priors of item 1 belong to other components, so
  a profile cannot own them: they go in the documentation and the workspace example.
- **Physical quantities.** An instance gives `lambda0`, `mass_scale`, `m_ap_physical` and
  a physical view of the lens (a mass profile whose fields are `mass_scale` × the wrapped
  sum), so that existing calculations (Einstein radius, mass in a circle, convergence) run
  on the physical lens. The physical M/L and kappa_s are `mass_scale` × the wrapped
  values. Whether λ₀ and m_ap can be declared through PyAutoFit's `latent_parameters`
  (they depend on the wrapped profiles through a ring integral) is for the slice's plan;
  if not, the workspace example does the conversion.
- **Untested; say so in the docs:** a pixelised source, point-source fits, more than one
  lens plane, free lens light. The magnification of the fitted tracer is that of the
  transformed lens, λ₀² times the physical one.

## Physical-units parameterisation

Maintainer's addition (2026-11-25). The recommended forms use a dark fraction, not physical
masses: P1-inv and P1′-f-inv sample `eps` and `f_dm`, and the ordinary-units physical form
P1′-f samples the total projected mass inside 5 kpc (M☉) and `f_dm_5`. The maintainer also
wants a parameterisation in the usual physical values: M200 for the dark matter and a
physical stellar mass, or mass-to-light ratio, for the stars.

- **Dark matter.** The library has `gNFWVirialMassConcSph` (`log10m_vir`, `c_2`,
  overdensity, redshifts) and the mass–concentration classes. Check they are JAX-traceable
  end to end (`gnfw_virial_mass_gnfw_conc.py` calls `scipy.integrate.quad`) and decide
  whether an "M200 + scale radius in arcsec" form is wanted. The project's `gNFWM200Sph`
  and `gNFWM200ConcSph` are closed-form, JAX-traceable prototypes (log10 M200c with r_s, or
  with c200 = r200 / r_s).
- **Stars.** The library has no stellar mass profile normalised by a physical mass:
  `mass_to_light_ratio` is in angular (convergence) units. Prototype: `SersicLogStellarMass`
  (log10 of the total stellar mass in M☉, with Σ_cr D_d² in M☉ / arcsec² passed in). Decide
  between total stellar mass and a physical M/L (M☉ / L☉ needs the photometric zero point
  and band), and take the critical density from redshifts and a cosmology, as
  `gNFWVirialMassConcSph` does, in place of a number passed in.
- **What the project found, for the documentation.** With log-uniform priors on M* and M200
  (its P2-log; also P1′-log, with log M* and log M_DM inside 5 kpc) 0 of 27 recovery fits
  pass: the measure piles the dark fraction onto 0 or 1, and M200 inside the sampling
  carries a hidden prior on the inner slope. No other prior on these parameters was
  fitted. So ship the profiles, document the caveat, and also give the conversions as
  derived quantities, so that a fit in the frame, or in any other form, reports M*, the
  physical M/L, M200 and the concentration.

## Slices

1. **Building blocks.** A shared JAX-safe 2F1 helper for the gNFW enclosed mass, the ring
   convergence and enclosed mass from deflections, and the Sérsic (usable mass-only) and
   gNFW profiles normalised by projected mass inside an aperture. *Repos:* PyAutoGalaxy
   *Witness:* unit tests show the 2F1 helper matches `scipy.special.hyp2f1` to 1e-12 for slopes 0 to 2.4 on NumPy and JAX, and each aperture-normalised profile encloses its `mass_ap` inside `theta_ap` to 1e-8.
2. **The mass-sheet frame.** The general `MassSheetFrame` of the epic prompt's "Assessment"
   section (settled 2026-11-26: a profile wrapping a list of mass profiles; the composite
   is not built), its λ₀ and `mass_scale`, the physical view and attributes, and the
   positions penalty scaled by 1 / λ₀. *Repos:* PyAutoGalaxy, PyAutoLens
   *Witness:* unit tests show, on NumPy and JAX, for the frame around stars + gNFW and around an elliptical power law: a grid traces to `centre + (source-plane grid of the physical lens - centre) / lambda_0` to 1e-10; the mean convergence inside `theta_ap` is `1 + eps` and the ring convergence at `theta_ap` is zero at `eps = 0`, both to 1e-6; a circular power law gives `lambda_0 = (slope - 1) / 2` to 1e-6; changing the power law's `einstein_radius` leaves the frame's deflections unchanged to 1e-10; and `PositionsLH` gives the same penalty for a frame lens as for its physical lens (the physical view, with the shear times `lambda_0`). *Depends:* 1
3. **Physical-units profiles.** A Sérsic normalised by physical stellar mass (or M/L) and a
   gNFW by M200, JAX-traceable, with the conversions also available as derived quantities (detail: the epic prompt's "Physical-units parameterisation" section).
   *Repos:* PyAutoGalaxy
   *Witness:* unit tests show a Sérsic built from a stellar mass returns that total mass to 1e-8 and a gNFW built from M200 encloses M200 inside r200 to 1e-6, on NumPy and JAX. *Depends:* 1
4. **Workspace example.** Simulate a stars + gNFW lens, fit it in the frame (the general
   frame around the aperture-normalised Sérsic and gNFW, `f_dm` shared by compound priors,
   the frame-unit shear and source priors), convert the result back to physical units
   (M*, M200). *Repos:* autolens_workspace
   *Witness:* the example runs in smoke and recovers the input dark-matter fraction inside its 95% interval. *Depends:* 2, and the fix of `draft/bug/autofit/a_compound_prior_model_reloaded_from_model.md`

## Design questions for the plan

- Free lens light: every project fit fixed the light to the truth. With free light, λ₀
  depends on the light parameters; the general frame handles this with no special path
  (the ring call traces whatever is free), but it was never fitted, and `jax.grad` through
  the Sérsic CSE decomposition is NaN in the light parameters (the prototype's
  `SersicLinearML` note).
- Names: `MassSheetFrame`, `eps` and `theta_ap` are working names from the prototype.
  Propose library names in the slice's plan.
- A reference test against the prototype: the prototype is not importable in library CI.
  If wanted, freeze a few deflection values from the assessment script as a fixture, with
  a tolerance of 1e-6″ (see "Assessment").
- Elliptical halo and an M/L gradient are out of scope here (untested in the project).

## Already known and related

- Reloading a model with compound or replaced priors reorders them
  (`draft/bug/autofit/a_compound_prior_model_reloaded_from_model.md`). The prototype works
  around it with `with_stable_prior_order`; the library version should not need to. The
  general frame shares `f_dm` by compound priors, so slice 4 waits for that fix.
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
