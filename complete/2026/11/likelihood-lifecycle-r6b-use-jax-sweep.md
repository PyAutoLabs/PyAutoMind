## likelihood-lifecycle-r6b-use-jax-sweep
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/691
- completed: 2026-11-26
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/692
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/140
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/285
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/109
- epic: likelihood-lifecycle (R6 phase B)

`use_jax=True` swept out of analysis constructors so workspace examples pick up `setup="auto"`; merged before the release by human ruling (on 2026.11.25.1 the default is `use_jax=True`, so behaviour is unchanged until the R6 release).

- Removed: autolens_workspace 131, HowToLens 3, autogalaxy_workspace 40, HowToGalaxy 16 (AST helpers in Science/scratch/likelihood_lifecycle_r6bc_2026-11-26/). Kept: `use_jax=` on FactorGraphModel, PositionsLH, apply_sparse_operator, PointSolver, simulators, operators, AnalysisEllipse, and every `use_jax=False`.
- Pins added until PyAutoLens#895: mixed-type factor graphs (imaging + interferometer, imaging + point, autogalaxy pixelization multi-dataset) keep `use_jax=True`; weak scripts pin `use_jax=False` (PyAutoLens#614).
- autolens_workspace_test / autogalaxy_workspace_test: no change — every analysis `use_jax=True` there is a deliberate JAX-path test.
- Prose worded true on both releases; notebooks regenerated for changed scripts only; `markdown/` pages wait for the next render.
- Smoke against library main: autolens 45/45, howtolens 41/41, autogalaxy 14/14 + 2/2 notebooks, HowToGalaxy run_smoke 30/30, autolens_test 40/40.

Follow-up: once PyAutoLens#895 releases, the factor-graph and weak pins can be removed (a later docs pass).

## Original prompt

# Likelihood lifecycle R6 phase B: sweep `use_jax=` out of the workspaces

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
- autogalaxy_workspace
- HowToLens
- HowToGalaxy
- autolens_workspace_test
- autogalaxy_workspace_test
Themes:
- hpc-gpu
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: autolens_workspace and autogalaxy_workspace start_here scripts construct their analyses with no `use_jax=` and log "Automatic compute setup" at fit start under the released stack.
Epic: likelihood-lifecycle
Phase: 6 (R6 rollout, phase B)
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Gate: lifted 2026-11-26 by the human — merges before the release (wording true on both releases; no R6-only arguments).
Filed: 2026-11-26
Issued: 2026-11-26

## Context

R6 phase A made `setup="auto"` the analysis default; an explicit `use_jax=True/False` with no `setup` now OPTS OUT of auto (human ruling 2026-11-25). So every workspace script that still passes `use_jax=True` silently keeps the manual path. ~355 scripts pass `use_jax=` (autolens_workspace 170, autogalaxy_workspace 52, HowToLens 4, HowToGalaxy 13, autolens_workspace_test 74, autogalaxy_workspace_test 42; counts from 2026-11-25).

## Ask

- Remove `use_jax=True` where the script means "the default".
- Keep a deliberate `use_jax=False` (now the documented opt-out) or replace it with an explicit `setup=` where a test pins a NumPy route.
- Update prose that explains `use_jax` (start_here, guides, HowTo chapters) to say `setup="auto"` is the default and how to opt out.
- One PR per repo; smoke each repo against the released stack; merge after the release (workspace main must not run ahead of PyPI).
- Notebooks regenerate from inside each workspace repo, never from a task root.
