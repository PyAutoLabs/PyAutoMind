## analytic-gaussian-benchmark
- issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/91 (closed completed 2026-09-02)
- completed: 2026-09-02
- workspace-pr: autofit_workspace_test https://github.com/PyAutoLabs/autofit_workspace_test/pull/92 (head `764af83e`, merge `54af208398ae7fd336d3d9bca363776ad50da037`)
- classification: research (graphical_ep) — epic `graphical-ep`, phase 1 (the keystone; ledger
  `draft/research/graphical_ep/ep_campaign.md`). No library PR: PyAutoFit was read-only for this
  task (claimed by two other tasks), so every defect filed as a Mind bug prompt.
- ci: `Smoke Tests [pull_request]` run 33662780163 — `changes`, `smoke (3.12)`, `smoke (3.13)` all
  green; mergeStateStatus CLEAN. (Repo workflow fires `push` on `main` only, so the PR run is the
  whole signal.)
- heart-ack (carried from the `active.md` entry): PyAutoArray open PR 10d old; release validation
  incomplete (no rehearsal for current source). Neither touches this workspace-only change.

- summary: Closed-form conjugate hierarchical Gaussian benchmark under
  `autofit_workspace_test/scripts/graphical/analytic_*.py` (six scripts, plus `no_run.yaml` and
  `smoke_tests.txt`): the known-scatter leg is analytic, the unknown-scatter leg exact by
  quadrature; compared against a minimal hand-rolled EP, autofit EP (Laplace) and the graphical
  joint fit, over a prior-family sweep and the phase-2 collapse configuration.
- verdict: closed form, minimal EP and the graphical joint fit agree everywhere; **every failing
  cell is autofit's EP column, including the exactly Gaussian leg A** (`mu` stays at its start:
  50.00 ± 20.6 vs 50.86 ± 4.11).
- mechanisms (root-caused read-only, recorded on PyAutoFit#1405, filed as four bug prompts under
  `draft/bug/autofit/`):
  - D1 — first prior of a process (id 0) compares equal to the `FactorValue` sentinel, corrupting
    every multi-variable factor gradient → `ep_prior_id_zero_collides_with_factor_value.md`
    (small, safe — do first).
  - D2+D3 — Laplace "covariance" is mean-field precision plus one non-accumulating random diagonal
    secant (no factor curvature; depends on prior ids through sampling order); a failed line search
    still projects the start point and overwrites the message →
    `ep_laplace_covariance_and_failed_update_projection.md` (the phase-2 mechanism).
  - D4+D5 — truncation limits dropped by `from_natural_parameters`/`__pow__` (leg B σ message
    returns (−inf, inf)); `TransformedMessage.from_mode` skips the Jacobian for scalar variables
    (log-σ leg never moves) → `ep_message_support_and_transform_lost_in_projection.md`.
  - D6 — `errors_at_sigma(as_instance=True)` crashes on a prior-valued global model →
    `samples_errors_at_sigma_instance_prior_valued_model.md` (small, safe).
- smoke gate: the closed-form reference (`analytic_gaussian.py`) and the minimal EP are curated into
  the smoke gate; the three autofit-parity scripts are parked `NEEDS_FIX` in `no_run.yaml`.
  **Un-park them** once D1–D6 land — re-run the parity sweep as the first check on each fix.
- banked: analytic upper limit `sigma_q95 = 12.18` (seed 0, truncated(10,5,0,100), N=5) — the
  phase-2 scatter-collapse referee. Calibration ceiling: EP with a Gaussian site on σ is biased on
  this model by construction (seeds 0–4 minimal-EP scatter row a ≤ 0.077, b ≤ 0.145) — judge any
  autofit fix against that, not zero.
- follow-ups: phase 2 (`ep_scale_collapse_basin_cure_or_caveat.md`) now has its mechanism and the
  analytic referee to run; phase 5 diagnostics gains "zero SUCCESS updates on a factor is a STALE
  result that no library warning reports"; `autofit_profiling_bootstrap.md` can port the benchmark
  into the profiling repo once that repo exists.
- worktree: `~/Code/PyAutoLabs-wt/analytic-gaussian-benchmark` removed at close-out; its 53 MB of
  gitignored `output/` (EP run products, test_mode/database scratch) deleted — re-derivable in
  minutes on CPU, evidence tables banked on #91.

## Original prompt

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
