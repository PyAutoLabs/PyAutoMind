## coolest-powerlaw-herculens
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/616
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/503, https://github.com/PyAutoLabs/PyAutoLens/pull/617
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/175
- summary: Follow-up to #612. Added `ag.mp.PowerLawIntermediate` — elliptical power-law whose einstein_radius is the COOLEST intermediate-axis θ_E (θ_int = √q·(2/(1+q))^(1/(γ−1))·θ_PL) — via a behavior-preserving `einstein_radius_major_from(xp)` hook in PowerLawCore/PowerLaw (existing profiles numerically unchanged; full suites 988+387 green; explicit numeric pin test). COOLEST PEMD mapping for it is an identity; `mass_profile_from(..., intermediate=True)` and `al from_coolest(intermediate=True)` rebuild PEMDs in that parameterisation. Priors-config block added (af.Model verified). awst `scripts/coolest_herculens_parity.py` PROVES the direct link: herculens 0.3.0 EPL theta_E IS the COOLEST intermediate-axis convention exactly (probe ratio 1.0 — the SPEMD √((1+q²)/(2q)) factor does not apply to EPL); same COOLEST template gives matching convergence (rtol 1e-8) and deflections (rtol 1e-6) in both codes, incl. spherical limit. herculens installs alongside pinned jax 0.10.2 cleanly (objax/utax/parameterized only), env-only, never a library dep. Shipped through Heart RED (5 pre-existing unrelated reasons) on user ack; awst leg was an additive parallel PR (repo claimed by viz-render-gallery, zero overlap).

## Original prompt

# PowerLawIntermediate profile + herculens power-law parity via COOLEST

Type: feature
Target: autolens
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## Context

Follow-up to feature/autolens/coolest_standard_support.md (do not start until
that task's COOLEST conversion layer is shipped or its API is stable).

From the Slack thread: autolens's power-law Einstein radius and axis-ratio
conventions differ from COOLEST (and lenstronomy/herculens) by factors of
sqrt(q), because autolens does not use the intermediate-axis convention. James:
"I may make PyAutoLens fully intermediate axis-ratio internally (I've had a few
people suggest this is the 'best' way to do it) but thats separate from Coolest
work."

Original request (verbatim, the follow-up clause):

> as a follow up try and make it so for the power-law, which you will add a
> PowerLawIntermediate profile as described, you get a direct link typing
> herculens's power-law to this one via Coolest

## Scope

- @PyAutoGalaxy: add a `PowerLawIntermediate` mass profile using the
  intermediate-axis-ratio (COOLEST) convention for Einstein radius and
  axis-ratio — convergence/deflections numerically consistent with the
  existing `PowerLaw` under the sqrt(q) parameter rescaling (regression-tested
  against it).
- COOLEST layer: `PowerLawIntermediate` maps to COOLEST's power-law (PEMD/EPL)
  with an identity parameter mapping (no sqrt(q) factors).
- @PyAutoLens: parity validation against herculens — same input parameters via
  a COOLEST model file, herculens's power-law (EPL) and `PowerLawIntermediate`
  produce numerically matching convergence and deflection angles on a common
  (y,x) grid (workspace_test parity script; herculens as an optional dev
  dependency, never a library dependency).
- Documentation: when to use `PowerLawIntermediate` vs `PowerLaw`, and the
  exact convention difference.
