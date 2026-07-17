## coolest-standard-support
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/612
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/501, https://github.com/PyAutoLabs/PyAutoLens/pull/613, https://github.com/PyAutoLabs/PyAutoLens/pull/615 (corrective: relative paths)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/283, https://github.com/PyAutoLabs/autolens_workspace_test/pull/173
- summary: COOLEST standard interop for Euclid DR1 prep — conversion layer at the model I/O boundary, internals unchanged (Slack-thread consensus with Sonnenfeld/Galan; user-confirmed scope). `autogalaxy/interop/coolest/` gives dict-in/dict-out converters for Sersic(+Sph), Isothermal(+Sph)→SIE, PowerLaw(+Sph)→PEMD, NFW(+Sph), ExternalShear, MassSheet→ConvergenceSheet with derived + numerically certified factors (θ_cool = √q·(2/(1+q))^(1/(γ−1))·θ_ag; Sersic r_eff already intermediate-axis; φ_cool = angle−90° East-of-North). `autolens/interop/coolest.py` adds to_coolest/from_coolest COOLEST JSON template I/O (`coolest` optional extra + test/dev/optional extras; shear/sheets as MassField entities; NFW Σ_crit from cosmology; Einstein-radius definition documented vs the DR1 tangential-critical-curve definition). Workspace guide `guides/coolest_interop.py` + workspace_test `coolest_round_trip.py` validate end-to-end (round trip to 8.9e-16). Gotchas: a guides/coolest.py shadows the coolest package (hence coolest_interop.py); coolest JSONSerializer rejects relative paths (fixed #615); PyAutoBuild generate.py stages the notebooks it writes (git restore --source=HEAD needed); notebooks/weak/*.ipynb stale on autolens_workspace main (excluded, needs its own sweep). Shipped through Heart RED (6 pre-existing unrelated reasons) on user ack. Follow-up drafted: draft/feature/autolens/coolest_powerlaw_herculens_parity.md (PowerLawIntermediate profile + herculens EPL parity via shared COOLEST file).

## Original prompt

# COOLEST standard support throughout PyAutoGalaxy and PyAutoLens

Type: feature
Target: autolens
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

## Context

Preparation for modeling the ~18,000 Euclid DR1 lenses: PyAutoLens results must
be exchangeable with other lens-modeling codes (lenstronomy, herculens, Glee)
via the COOLEST standard (https://github.com/aymgal/COOLEST).

Original request (verbatim):

> read this SLACK chat about the COOLEST standards, implement them throughout
> PyAutoGalaxy and PyAutoLens, and then as a follow up try and make it so for
> the power-law, which you will add a PowerLawIntermediate profile as
> described, you get a direct link typing herculens's power-law to this one
> via Coolest

Key points from the Slack thread (James Nightingale, Alessandro Sonnenfeld,
Aymeric Galan):

- James's original plan: define every light/mass profile so that for input
  ndarrays of (y,x) coordinates it outputs deflections, convergence and the
  other COOLEST quantities; align PyAutoLens angle conventions with COOLEST;
  verify parity with lenstronomy/herculens on a Power Law + Shear (+ Sersic
  lens light and source) on one Euclid lens, including image orientation on
  load (no vertical flips).
- Sonnenfeld + Galan both advised: do NOT change PyAutoLens internals; keep
  sampling on (e1, e2) with a (q, PA) wrapper, and write a conversion step
  (PyAutoLens ↔ COOLEST wrapper) instead. lenstronomy/herculens also let users
  define coordinates freely, so they too need a conversion step — internal
  changes would not by themselves buy parity.
- The intermediate-axis-ratio question: autolens's Einstein radius and
  axis-ratio come out different from COOLEST (factors of sqrt(q)); James is
  considering making the mass profiles intermediate-axis internally, which is
  separable from the COOLEST wrapper work (handled in the follow-up prompt).
- Einstein-radius definition must be unambiguous: Sonnenfeld assumes
  (A/pi)^(1/2) with A the area enclosing mean kappa=1; the Euclid DR1
  catalogue uses the area within the tangential critical curve (includes
  shear's shaping). The export must state its definition explicitly.
- Export scope: analytic profile parameters only; deflection/convergence maps
  stay in the distributed .fits catalogue (optionally exportable later).
- Sonnenfeld's COOLEST .json lens models for validation:
  https://gitlab.euclid-sgs.uk/asonnenf/goldenlenses/-/tree/e0ff0fbab2aa4c8bc19b4c18d7bcfe24bc367795/paper1/lens_models
- James's descope in-thread: "focus on getting a wrapper from PyAutoLens to
  Coolest". The instruction above ("implement them throughout") supersedes but
  the plan must surface the wrapper-vs-internal-change scope decision for
  approval.

## Scope

- @PyAutoGalaxy: COOLEST conversion layer for light and mass profiles —
  bidirectional mapping of profile parameterisations (ellipticity (e1,e2) ↔
  (q, PA) with COOLEST position-angle convention, sqrt(q) intermediate-axis
  factors, angle/orientation conventions), covering the profiles COOLEST
  defines (Sersic, shear, SIE/PowerLaw, NFW, ...).
- @PyAutoLens: COOLEST .json import/export of full lens models (lens light +
  mass + source), reading/writing the COOLEST template system; explicit,
  documented Einstein-radius definition on export.
- Round-trip tests: import Sonnenfeld's golden-lens .json models, re-export,
  verify parameter fidelity; unit tests for every profile mapping including
  the sqrt(q) Einstein-radius rescaling.
- Keep sampling and all internal model composition on (e1, e2) — the COOLEST
  layer is a conversion step at the model I/O boundary, not an internal
  convention change (per Sonnenfeld/Galan consensus; deviation from this needs
  explicit approval in the plan).

Follow-up prompt (separate task): feature/autolens/coolest_powerlaw_herculens_parity.md
