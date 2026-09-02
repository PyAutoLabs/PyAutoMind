# Analytic Gaussian benchmark: closed-form validation of graphical + EP

Type: research
Target: graphical_ep
Repos:
- autofit_workspace_test
Themes:
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued — autofit_workspace_test#91, worktree analytic-gaussian-benchmark
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: graphical-ep
Phase: 1
Campaign: research/graphical_ep/ep_campaign.md (Phase 1 — the keystone; start here)
Filed: 2026-08-19 (backfilled from git)
Issued: 2026-09-02
Issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/91

## Why

We have three test cases (1D Gaussian toy, slope_hierarchy cosmology, IC50
cancer) but none has a *known closed-form posterior*. Every EP validation so
far compares EP against a graphical joint fit — two sampled answers compared
to each other, neither compared to truth-with-pen-and-paper. A fourth test
case where every likelihood is a simple Gaussian (fully conjugate hierarchical
model) gives exact analytic posterior means **and errors**, including an
explicit analytic upper bound on the parent scatter. That turns "EP looks
about right" into a statistical statement about the source code: priors,
messages, cavity distributions and projections are either reproducing the
closed form or they are not.

This cannot replace the real use cases (their likelihoods need full sampling)
— it is the referee, not the match.

## The model

A conjugate hierarchical Gaussian: parent (mean μ, scatter σ) → per-dataset
draws x_i → Gaussian data likelihoods with known noise. Small N (3–10) so the
closed form stays hand-checkable. Derive and commit the closed-form posterior
(document the derivation in the script docstring — it is the ground truth and
must be auditable).

## Run it three ways

1. **Closed form** — the analytic posterior, evaluated directly (numpy).
2. **Minimal hand-rolled EP loop** — an as-simple-as-possible EP
   implementation *outside* autofit (one file, explicit messages and cavity
   maths). This isolates "EP the algorithm" from "EP the autofit
   implementation": if (2) matches (1) but (3) does not, the defect is in the
   source code, not the method.
3. **autofit APIs** — the same model through `FactorGraphModel` as (a) a
   graphical joint fit and (b) the EP loop (`factor_graph.optimise`).

Assert means AND standard deviations of every parameter match (1) within
statistical tolerance, for both (3a) and (3b).

## Prior-family stress tests

The historical constraint was GaussianPrior-only EP; the extension to all
priors was never thoroughly validated. On this benchmark, sweep:

- everything initialised with `GaussianPrior` (the safe baseline);
- `TruncatedGaussianPrior` near a physical edge (parent scatter bounded at
  zero — deliberately the slope_hierarchy configuration, to expose any
  boundary artefact against the known analytic answer);
- at least one non-Gaussian family end-to-end (e.g. LogGaussian / Gamma where
  conjugacy still gives a checkable moment).

The 2026-07/08 priors-and-messages fixes (census retired 2026-08-18; property
sweep PR#1499) validated each density in isolation; this validates them
*through the EP machinery*.

## Feeds

- `bug/autofit/ep_scale_collapse_basin_cure_or_caveat.md` — an analogous run
  with a known scatter upper limit answers "does the collapse basin exist even
  when the truth is fully conjugate?", and cleanly separates prior-boundary
  effects from EP-intrinsic shrinkage.
- The EP-profiling epic — a fast, deterministic model is the right harness
  for wrapper-overhead measurement.

## Home + acceptance

Code lives in `autofit_workspace_test/scripts/graphical/` beside `ep_parity.py`,
`ep_exact.py` and `ep_deterministic.py` (re-homed 2026-09-02 from the
`autofit_workspace_developer/analytic/` proposal: this is EP CI infrastructure,
so the core parity script is curated into the smoke gate). Acceptance: a single
script (or small package) that runs in minutes on CPU, prints a
closed-form-vs-EP-vs-graphical parity table, and exits non-zero on tolerance
breach so it can serve as a regression check.
