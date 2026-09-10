# Switch 11 workspace call sites to `subplot_fit_interferometer_dirty_images`

Type: docs
Target: workspaces
Repos:
- autolens_workspace
Themes:
- visualization
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: notify
Witness: After the sweep a grep for `subplot_fit_dirty_images` under `autolens_workspace/scripts/` returns nothing, all 11 named sites call `subplot_fit_interferometer_dirty_images`, and each regenerated figure carries the auto-derived critical-curve overlay the autogalaxy-bound version did not draw. The call-site count and the `fit=fit`-only claim are re-verified against current main first.
Review-minutes: 0
Unattended: ready
Filed: 2026-09-09

Split from `plot_coverage_followups.md` on 2026-09-09 (the remaining sub-item of
item 4 of 4). That file was a container of four independent follow-ups and said
so — "do **not** bulk-issue them as a series" — so it has been split into one
prompt per item and archived. **Item 4's own finding already shipped**
(2026-07-30, PyAutoLens#670, `339867e2c`); this prompt carries only the
workspace sweep it deferred.

## Why

PyAutoLens#670 added `subplot_fit_interferometer_dirty_images` — autolens's own
version, which with `image_plane_lines=None` auto-derives the tracer's critical
curves from the fit (`_compute_critical_curve_lines`) and overlays them on the
dirty model image. `subplot_fit_dirty_images` was deliberately **left bound to
autogalaxy's** version, because the signatures diverge
(`residuals_symmetric_cmap` vs `image_plane_lines`) and rebinding would be a
behaviour change rather than an additive export.

## What

`autolens_workspace` still calls the autogalaxy-bound `aplt.subplot_fit_dirty_images`
at 11 sites:

- `scripts/interferometer/{fit,modeling,plot}.py`
- four `scripts/interferometer/features/*/fit.py`
- `scripts/multi/features/imaging_and_interferometer/modeling.py`

All pass `fit=fit` only (none pass `residuals_symmetric_cmap`), so all 11 can be
switched to the new name and would gain critical-curve overlays for free.

Deferred from the originating task because it is a **visual change across 11
lens examples** and deserves its own review pass — which is why this is
`supervised`: the figures change, and a human should look at them.

Re-verify the call-site count and the "all pass `fit=fit` only" claim against
current `main` before editing; the finding was recorded 2026-07-30.

- @autolens_workspace
