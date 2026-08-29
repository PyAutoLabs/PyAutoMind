# plot coverage — follow-ups deferred from plot-coverage-gaps

Filed: 2026-07-30 (backfilled from git)
Themes:
- visualization

Four items deliberately scoped out of **plot-coverage-gaps**
(PyAutoLens#667 / #668, autolens_workspace#404, autogalaxy_workspace#191).
Each is independent; do **not** bulk-issue them as a series.

Recorded 2026-07-30, at that task's PR-open.

## 1. Demo `subplot_fit_interferometer_combined`

PyAutoLens#668 **exported** `aplt.subplot_fit_interferometer_combined` for API
symmetry — imaging's `subplot_fit_combined` was exported, the interferometer
equivalent was not — but nothing demonstrates it.

It takes a `fit_list`, so its home is a multi-dataset interferometer example,
not the single-fit `scripts/interferometer/plot.py`. Passing `[fit, fit]` there
would teach a wrong idiom (the same reasoning that kept the `*_x1_plane` pair
out of that task).

Candidate home: `autolens_workspace/scripts/multi/` — `multi/plot.py` already
demonstrates the imaging combined subplots (`subplot_fit_combined`,
`subplot_fit_combined_log10`), and `multi/features/imaging_and_interferometer/`
provides a real multi-interferometer fit context.

- @autolens_workspace

## 2. Demo `subplot_ellipse_errors`

`ag.plot.subplot_ellipse_errors` is demonstrated nowhere in autogalaxy_workspace.

It takes `fit_pdf_list: List[List[FitEllipse]]` — outer list one entry per
posterior sample, inner list one `FitEllipse` per ellipse. A standalone
`plot.py` runs no search, so this needs a real ellipse model-fit to produce
genuine samples. Do **not** fake it by perturbing parameters: the figure's whole
point is the inference-derived error region.

Likely home: an ellipse results/`fit.py`-adjacent script that already has a
`Result`, rather than `scripts/ellipse/plot.py`.

- @autogalaxy_workspace

## 3. `docs/api/plot.rst` omits already-exported symbols

PyAutoLens#668 added its two new exports to `docs/api/plot.rst`, but the file
was already missing several symbols that `autolens.plot` exports:

- `subplot_imaging_dataset`
- `subplot_imaging_dataset_list`
- `fits_imaging`
- `fits_interferometer`
- `subplot_fit_interferometer_tracer`
- `subplot_interferometer_dirty_images`

There is no "Dataset Subplots" heading in the rst at all — the dataset-level
functions have no home in it. Check the autogalaxy equivalent for the same class
of drift, and consider whether `/audit_docs` should cover `plot.rst`
autosummary blocks against the live `aplt` namespace.

- @PyAutoLens (and probably @PyAutoGalaxy)

## 4. `autolens.plot` shadows two of its own interferometer functions — RESOLVED

**SHIPPED 2026-07-30 as PyAutoLens#670 (`339867e2c`).** Resolved additively:
`subplot_fit_interferometer_dirty_images` now exports autolens's own function,
matching the existing `subplot_fit_real_space` /
`subplot_fit_interferometer_real_space` convention. `subplot_fit_dirty_images`
was deliberately **left bound to autogalaxy's** version — the signatures diverge
(`residuals_symmetric_cmap` vs `image_plane_lines`), so rebinding would be a
behaviour change rather than an additive export.

Confirmed the autolens version is materially better for lensing, not a
duplicate: with `image_plane_lines=None` it auto-derives the tracer's critical
curves from the fit (`_compute_critical_curve_lines`) and overlays them on the
dirty model image. Verified functionally on a real `FitInterferometer` — 1 curve
derived — not just signature-checked.

**Remaining sub-item:** `autolens_workspace` still calls the autogalaxy-bound
`aplt.subplot_fit_dirty_images` at 11 sites —
`scripts/interferometer/{fit,modeling,plot}.py`, four
`scripts/interferometer/features/*/fit.py`, and
`scripts/multi/features/imaging_and_interferometer/modeling.py`. All pass
`fit=fit` only (none pass `residuals_symmetric_cmap`), so all 11 can be switched
to the new name and would gain critical-curve overlays for free. Deferred
because it is a **visual change across 11 lens examples** and deserves its own
review pass.

<details>
<summary>Original finding</summary>


`aplt.subplot_fit_dirty_images` and `aplt.subplot_fit_real_space` resolve to the
**autogalaxy** implementations inside `autolens.plot`:

```python
>>> aplt.subplot_fit_dirty_images.__module__
'autogalaxy.interferometer.plot.fit_interferometer_plots'
```

autolens has its own versions in
`autolens/interferometer/plot/fit_interferometer_plots.py` which accept
lensing-specific `image_plane_lines` / `image_plane_line_colors` /
`source_plane_lines` arguments the autogalaxy versions do not. Lens users
calling `aplt.subplot_fit_dirty_images` therefore silently get the galaxy
version and cannot pass critical-curve/caustic overlays.

Note `subplot_fit_interferometer_real_space` **is** separately exported as
autolens's own, so `subplot_fit_real_space` (AG) and
`subplot_fit_interferometer_real_space` (AL) currently coexist under different
names — confusing but not lossy. `subplot_fit_dirty_images` is the lossy one:
autolens's version is reachable under **no** exported name.

This was kept out of #668 deliberately: rebinding an existing exported name is a
**behaviour change**, not an additive export. Decide whether to rebind (and
accept the behaviour change), add a distinct `subplot_fit_interferometer_dirty_images`
name, or leave it — then sweep the workspace calls accordingly.

- @PyAutoLens
- @autolens_workspace (calls `aplt.subplot_fit_dirty_images` in
  `scripts/interferometer/plot.py`, `scripts/interferometer/modeling.py` and
  `scripts/multi/features/imaging_and_interferometer/modeling.py`)

</details>
