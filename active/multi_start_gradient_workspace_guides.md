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
