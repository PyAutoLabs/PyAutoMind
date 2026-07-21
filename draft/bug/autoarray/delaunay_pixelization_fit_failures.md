# Delaunay pixelization fit failures (FitException + interferometer broadcast) (parked NEEDS_FIX)

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace
- HowToLens
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Parked-since-2026-04-10 Delaunay-specific cluster from the 2026-07-20 sweep. Two symptoms, likely
a shared Delaunay-mesh/mapper root cause in PyAutoArray:
- `autofit.exc.FitException in Delaunay pixelization fit` — imaging.
- `broadcast shape mismatch (2,2) vs (1032,1032) in Delaunay interferometer` — interferometer.

Affected (remove NEEDS_FIX from each repo's config/build/no_run.yaml once green):
- autolens_workspace: `imaging/features/pixelization/delaunay`, `interferometer/features/pixelization/delaunay`
- HowToLens: `imaging/features/pixelization/delaunay`, `interferometer/features/pixelization/delaunay`

First step: reproduce autolens_workspace/interferometer/features/pixelization/delaunay on clean main
(real data) — the (2,2) vs (1032,1032) broadcast points at a Delaunay source-plane grid vs visibility
count mismatch. Then the imaging FitException. Related parked clusters: pixelization-inversion-not-PD,
jax-grad-gradient-custom-jvp (Delaunay gradients).
