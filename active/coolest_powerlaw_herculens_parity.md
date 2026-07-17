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
