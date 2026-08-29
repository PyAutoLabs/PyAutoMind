# Colormap control: audit the cmap lever end-to-end and default the Euclid configs to magma

Type: feature
Target: PyAutoLens
Repos:
- PyAutoArray
- PyAutoLens
- autolens_workspace
- euclid_strong_lens_modeling_pipeline
Themes:
- visualization
- euclid
Difficulty: small-medium
Autonomy: safe
Priority: high
Status: formalised
Epic: euclid-dr1-prep
Phase: 0
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28
Issued: 2026-08-28

Phase 0 of 10 in the Euclid DR1 preparation epic. Independent of every other phase —
it can start immediately and does not gate anything.

User request (verbatim):

"""
0) change default cmap to magma: lots of people compain about the cmap so make sure there is functionality to adjust 
cmap used throughout autolens and update euclid repo configs so that magma is used.
"""

## What already exists (surveyed 2026-08-28 — do not rebuild it)

The lever is already there. `PyAutoArray/autoarray/plot/utils.py::_default_colormap()`
reads `conf.instance["visualize"]["general"]["colormap"]` and falls back to the bundled
custom `"autoarray"` colormap (registered from
`PyAutoArray/autoarray/plot/segmentdata.py`, `COLORMAP_NAME = "autoarray"`). The key
`colormap: autoarray` is present in all three `config/visualize/general.yaml` files
(PyAutoArray, autolens_workspace, euclid_strong_lens_modeling_pipeline).

So the task is **audit + default change**, not lever construction.

## Deliverables

1. **Reach audit.** Confirm the config value actually reaches *every* 2D plotting
   surface, not just `plot/array.py` (which is the only confirmed consumer —
   `array.py:140-142` calls `_default_colormap()`). Check at minimum
   `PyAutoArray/autoarray/plot/inversion.py` (`_plot_rectangular`, `_plot_delaunay` both
   take a `colormap` argument — trace who supplies it), `plot/grid.py`, and any
   hardcoded colormap literal. `array.py:208` hardcodes `cmap="Greys"` for the
   `array_overlay`; decide whether that is deliberate (it probably is) and document it
   rather than silently leaving it undocumented.
2. **Per-figure override.** Verify a user can override the colormap for a single figure
   through the public plot API without editing config, and document how. If no such
   route exists, add the minimal one — prefer the lean existing lever over a new class.
3. **The silent fallback.** `_default_colormap()` (and its siblings
   `_conf_imshow_origin`, `_conf_output_format`) wrap the config read in a bare
   `except Exception`. A typo'd or missing key therefore fails silently to `autoarray`
   and the user never learns their setting was ignored. Tighten this so a genuinely
   absent config falls back quietly but a *malformed* value is loud. (Workspace
   convention: no silent guards.)
4. **Magma in the Euclid configs.** Set `colormap: magma` in
   `euclid_strong_lens_modeling_pipeline/config/visualize/general.yaml`. Leave the
   PyAutoArray/autolens_workspace defaults alone unless the user asks otherwise — the
   request scopes the magma change to "euclid repo configs".
5. **Documentation.** One short, discoverable place telling users how to change the
   colormap (config key + per-figure override). The `config/visualize/README.md` files
   are the natural home.

## Acceptance / gate

- A single config edit changes the colormap on every 2D figure the pipeline produces
  (imaging data, fits, residuals, inversion reconstructions), demonstrated on at least
  one imaging figure and one inversion figure.
- A malformed `colormap` value produces a clear error or warning, not a silent revert.
- The Euclid pipeline repo renders in magma out of the box.
- Nothing else in the epic gates on this; it can ship on its own.
