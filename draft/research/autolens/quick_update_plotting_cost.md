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
