# Quick-update plotting cost — minutes per update, and it is not JAX compile

Type: research
Target: autolens
Repos:
- PyAutoLens
- PyAutoGalaxy
Themes:
- visualization
- profiling
Difficulty: medium
Autonomy: safe
Priority: medium
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-07-31 (backfilled from git)

## Why

While removing `fit_quick.png` (PyAutoLens#680, merged 2026-07-31), a control
probe on the wst `modeling_visualization_jit.py` MGE-linear imaging setup
measured `perform_quick_update`:

- old 6-panel `fit_quick`: cold 199 s / warm 184 s
- new normal `fit.png` subplot: ~296 s first call

Cold ≈ warm, so the cost is **recurring** per-update fit-quantity computation
plus rendering — NOT one-off JAX compile (the `fit_for_visualization` jit
compile is ~27 s, shared, and its warm call is ~2.6 s). Numbers are from a
heavily loaded WSL box (load ~5), so absolute values are inflated, but a
~3-minute recurring cost per quick update dwarfs the seconds-scale search
iterations it interleaves with. The user expected the fit/search side to be
seconds — it is; the plotting path is the sink.

## What

Profile where the time goes in `PlotterImaging.fit_imaging` /
`VisualizerImaging.visualize` when called from the quick-update hook with a
jit-cached fit: fit `cached_property` evaluation (inversion / per-plane model
images / source-plane quantities), JAX→NumPy device transfers, critical-curve
computation (`_compute_critical_curves_from_fit`), and matplotlib rendering/
savefig. Produce a breakdown, then propose and (if warranted) implement the
cheap wins — e.g. reusing already-computed quantities, computing critical
curves less often, or skipping expensive panels during quick updates without
reintroducing a second fit-plot layout (the whole point of #680 was one
layout). Re-measure on a quiet box and record before/after per-update cost.

Probe script from the #680 session (rebuildable): scratchpad
`quick_update_timing_probe.py` — builds the wst MGE-linear analysis, times
`perform_quick_update` cold/warm.

## Triage 2026-09-09 — why this needs a local box, and what a static pass already found

Considered for the `visualization` bundle and **dropped**: the deliverable is a
*measured* breakdown plus a before/after re-measure, and the prompt itself
discounts its original numbers because the box was loaded (load ~5). A remote
Claude container is a worse measuring instrument than the one those numbers came
from — shared 4-core, no lensing stack, no JAX, and no wst MGE-linear dataset —
so any timing it produced would be exactly the untrustworthy kind this task
exists to replace. **The measurement leg is human/local (or RAL) work.**

A static read of the quick-update path on `main` (2026-09-09) did narrow the
suspects, and these are worth checking first when the profiling is actually run:

- `autolens/imaging/model/visualizer.py:108` calls
  `_compute_critical_curves_from_fit(fit)` on **every** quick update. That
  resolves (`autolens/imaging/plot/fit_imaging_plots.py:25`) to
  `_compute_critical_curve_lines(tracer, fit.mask.derive_grid.all_false)` — the
  **fully unmasked, full-resolution** image-plane grid, deliberately, so the
  curves cover the whole image extent. Critical-curve extraction over that grid
  is a per-update cost that scales with the *unmasked* image size rather than
  the fitted region, and it is recurring, not compiled once. This is the single
  strongest candidate for the "cheap win" the prompt asks for — e.g. computing
  the curves on a coarser grid, or less often than every quick update.
- The curves are already hoisted correctly: the visualizer computes them once
  and passes them into `plotter.fit_imaging`, which reuses them
  (`autolens/imaging/model/plotter.py:69-79`). So the *duplication* win is
  already taken; what remains is the cost of the single computation.
- `_get_source_vmax` (`fit_imaging_plots.py:38`) walks
  `fit.model_images_of_planes_list`, a `cached_property` chain that triggers the
  inversion — cheap if the fit is already warm, not if the quick-update hook
  hands over a fresh fit.

Suggested re-scope if this is picked up unattended: split the *analysis + an
instrumented probe committed to the repo* (deliverable: a breakdown document and
a runnable timing harness, no numbers claimed) from the *measurement + tuning*
(deliverable: before/after per-update cost on a quiet box). Only the first half
is container-safe.
