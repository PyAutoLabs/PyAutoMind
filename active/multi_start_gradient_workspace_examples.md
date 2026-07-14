# Multi-start gradient searches — autofit_workspace example (Phase 2)

Type: docs
Target: autofit_workspace
Repos:
- @autofit_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Phase 2 (redefined) of the multi-start gradient MAP search promotion (PyAutoFit#1369,
library + JAX validation shipped in Fit#1370 + awt#43). The original "config +
packaged defaults" phase was found to have no content — PyAutoFit searches have no
per-search parameter config and the new searches add zero config keys (they reuse
the existing MLE `visualize`/`general`/`output` surface). The real remaining work is
the user-facing workspace example.

## What to build

Document the new `af.MultiStartAdam` / `af.MultiStartADABelief` / `af.MultiStartLion`
searches in the user-facing `autofit_workspace`, mirroring the existing Drawer / LBFGS
examples in `scripts/searches/mle.py`:

- Add a **Search: MultiStartAdam** section to `scripts/searches/mle.py` after LBFGS,
  running the search on the shared 1D Gaussian model and plotting the max-log-likelihood
  fit (same plotting idiom as the Drawer/LBFGS sections).
- Because the multi-start gradient searches are JAX-native (they raise if the analysis
  is not `use_jax=True`), this section needs its own JAX-traceable analysis:
  `enable_pytrees()` + `register_model(model)` (from `autofit.jax.pytrees`, as in
  autofit_workspace_test `Nautilus_jax.py`) and `af.ex.Analysis(..., use_jax=True)`.
  Keep the existing `use_jax=False` shared analysis for Drawer/LBFGS unchanged.
- Briefly note that `MultiStartADABelief` and `MultiStartLion` are drop-in alternatives
  (different optax update rule; Lion wants a ~10x smaller learning rate), and what the
  N broad starts + best-basin selection buy you (escaping wrong basins that trap
  single-start optimizers).
- Update the script header (module docstring bullet list + `__Contents__`) and the
  "Relevant links" block to include the new searches.
- Regenerate the paired notebook `notebooks/searches/mle.ipynb` so the committed mirror
  matches the script (workspace convention; keep them in sync).

Opus authors the tutorial prose (workspace example narrative). Keep the run cheap
(modest `n_starts`/`n_steps`) — the example demonstrates the API and truth-basin
recovery, not a profiling run.

<!-- Phase 2 (redefined config→examples) of promote_the_multi_start_gradient_map_optimizer -->
