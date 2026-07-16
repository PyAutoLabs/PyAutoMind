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
