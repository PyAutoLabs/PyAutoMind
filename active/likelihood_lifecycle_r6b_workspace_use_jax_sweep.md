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
