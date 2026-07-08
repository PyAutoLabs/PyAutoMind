# Point-source solver over/under-prediction handling + workspace guide

Type: feature
Target: cluster
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Careful treatment of multiple-image over- and under-prediction in the point-source solver/likelihood, plus a workspace guide documenting the choices.

The cluster/point-source image-plane likelihood must handle the case where the model tracer predicts
*more* images than observed (extra images — often demagnified centrals or artefacts of a wrong mass
model) and *fewer* images than observed (under-prediction — the model cannot reproduce an observed
image). The library currently offers three pairing schemes (Pair / PairAll / PairRepeat, Hungarian
assignment — see scripts/cluster/likelihood_function.py which documents the too-many/too-few image
pathology) but the behaviour under mismatched image counts needs deliberate design rather than
incidental behaviour:

- Audit what each pairing scheme actually does today when n_model != n_observed, including the
  likelihood penalty (or silent absence of one) in each direction. Compare against how LensTool
  handles it (chi^2 penalty terms for missing images; treatment of predicted-but-unobserved images,
  which observers often justify as "below detection limit").
- Decide and implement the default: e.g. explicit penalty terms for unmatched observed images
  (under-prediction should always be penalized hard) and a configurable policy for extra model
  images (penalize / ignore-with-warning / magnification-threshold filter for demagnified centrals).
  No silent guards — a model that cannot produce an observed image should be loudly bad, not
  quietly fine.
- Verify solver robustness feeding this: PointSolver grid resolution vs missed images (a real
  image missed by a too-coarse solver grid must not masquerade as model under-prediction).
- Write a guide at `autolens_workspace/scripts/guides/` (matching the existing guides' style)
  documenting: the pairing schemes, the over/under-prediction policies and how to choose, solver
  settings that matter at cluster scale, and source-plane vs image-plane chi^2 trade-offs — the
  reference the flagship LensTool example links to for likelihood choices.

Relevant prior finding: cluster source-plane chi^2 has a PointSolver precision-floor issue
(magnification-amplified, ~8e7 at truth — see cluster-test-workspace notes / likelihood_sanity.py);
this prompt's audit should keep that in mind since penalty-term magnitudes interact with the floor.

Scope: PyAutoLens (point-source fit/solver) + autolens_workspace (guide + cluster scripts prose).
Should land before or alongside the flagship LensTool example, whose real-data fit will hit these
cases immediately.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/fa55f70e-2cea-4887-bf12-61f81cff042f/scratchpad/p5_solver_over_under_prediction.md -->
