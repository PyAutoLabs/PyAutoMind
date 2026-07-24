# autolens_workspace_developer rectangular experiments — Gut stash + rename

Type: maintenance
Target: autolens_workspace_developer
Repos:
- autolens_workspace_developer
- PyAutoGut
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

## Context (split from rectangular-mesh-consolidation, PyAutoArray#402, closed 2026-07-24)

The consolidation deleted the spline/rotated/kernel-named rectangular classes
from PyAutoArray (#403). `autolens_workspace_developer` still holds the
experiment scripts that used them; the repo was claimed by
`blackjax-smc-gradient-kernel` at wrap-up time (23 dirty files), so this
cleanup was deferred. File issued when that claim releases and the repo is
clean.

## Task

1. **Stash to PyAutoGut** (condemned-material lifecycle — durable recoverable
   refs) the spline/rotated experiments now that their library classes are
   gone:
   - `rect_adapt_duo/` (rotated-vs-spline demo `compare_meshes.py` +
     `simulator.py` + bundled `dataset/` — `RectangularRotatedAdaptImage` /
     `RectangularSplineAdaptImage`, live nowhere else);
   - `searches_minimal/probe_grad_pix_adapt_image.py` (tests the deleted
     `RectangularSplineAdapt*`);
   - `jax_profiling/misc/pixelization_spline_vs_linear.py` +
     `pixelization_spline_fit_comparison.py` + their `results/jit/imaging/spline_vs_linear*`.
2. **Rename kernel-named survivors to the plain names** (the classes still
   exist, just renamed): `searches_minimal/probe_grad_pix.py`,
   `pix_multi_start.py`, `plotting_alignment/kernel_cdf_alignment.py`
   (`RectangularKernelAdapt{Density,Image}` → `RectangularAdapt{Density,Image}`,
   drop any now-redundant `bandwidth=`/default handling).
3. **Update** `jax_profiling/gradient/README.md` rows to the consolidated
   naming (the linear-mesh staircase rows stay as history; the kernel rows are
   now just "the adaptive rectangular mesh"). See the completion record's
   bandwidth note (optimal h is config-dependent) for the README caveat.

## Constraints

- Wait for the `blackjax-smc-gradient-kernel` claim to release; verify the repo
  is clean before starting (it had 23 dirty files at wrap-up).
- Developer repo (doc-light, not CI-gated like the workspaces); still verify
  renamed scripts import cleanly against merged main.
- Copy any gitignored products out before any worktree teardown.
