## multi-start-gradient-guides
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/277 (closed) + https://github.com/PyAutoLabs/autogalaxy_workspace/issues/132 (closed)
- completed: 2026-07-14
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/278 (merged aac9321c) + https://github.com/PyAutoLabs/autogalaxy_workspace/pull/133 (merged 4d91e878)
- repos: autolens_workspace, autogalaxy_workspace
- summary: Phase 3 of the multi-start gradient search promotion (Fit#1369). Added a MultiStartAdam config section to scripts/guides/modeling/searches.py in both user workspaces, after LBFGS, framed as the optimizer that works on complex lens/galaxy parameter spaces (wide multi-start) where single-start LBFGS fails. Config-only guides (construct search objects, no fits — per human, intent is API discovery not a data run). Contents updated; notebooks regenerated. --auto safe; Heart YELLOW human-acked (set unchanged from Phase-2 ack). Scope was user-workspaces-only (test workspaces skipped per human). See project_multi_start_gradient_search_promotion.

## Original prompt

# Multi-start gradient searches — autolens/autogalaxy searches guides (Phase 3)

Type: docs
Target: autolens_workspace, autogalaxy_workspace
Repos:
- @autolens_workspace
- @autogalaxy_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: issued

Propagate the multi-start gradient MAP searches (PyAutoFit#1369, shipped) to the
user-facing `scripts/guides/modeling/searches.py` configuration guides in
autolens_workspace and autogalaxy_workspace, alongside the existing LBFGS section.

These guides are configuration references (they construct `search = af.X(...)`
objects to document the API/settings; they do not run fits). So the addition is a
`af.MultiStartAdam(...)` config block plus prose in each guide, mirroring the LBFGS
section, framed against the caveat those guides already state ("parameter spaces
fitted by lens/galaxy models are often too complex for optimizers"): multi-start
Adam is the optimizer that *does* work on these complex spaces, because its wide
population of parallel starts escapes the local maxima that trap single-start
LBFGS (the Phase-3 GPU benchmark proved multi-start Adam recovers the truth basin
on the HST MGE lens likelihood). Note it needs a JAX-traceable analysis
(`use_jax=True`), that `MultiStartADABelief`/`MultiStartLion` are drop-in
alternatives, and that (like all optimizers) it returns a MAP point estimate not a
posterior, so Nautilus stays the default when errors are needed.

Update each guide's `__Contents__` list and regenerate the paired notebook. One
issue + PR per repo.

<!-- Phase 3 of promote_the_multi_start_gradient_map_optimizer (user workspaces only, per human 2026-07-14) -->
