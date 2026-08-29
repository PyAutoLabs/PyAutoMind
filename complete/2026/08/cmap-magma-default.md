## cmap-magma-default
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/509 (closed 2026-08-28)
- completed: 2026-08-28
- library-pr: PyAutoArray#510 (merged 22191ec455ccf029033baf5834cbdbc124e4fffd -> main)
- workspace-pr: euclid_strong_lens_modeling_pipeline#42 (merged ac4b099a7bdd15a9f9f6e4ad5fb992f8d4fda63d -> main)
- epic: euclid-dr1-prep, phase 0 of 10 — independent, gated nothing and was gated by nothing.
- what shipped: the `visualize/general.yaml -> colormap` lever audited end-to-end, made loud on malformed values, documented on both routes, and defaulted to `magma` in the Euclid pipeline. All five deliverables of the prompt shipped; nothing deferred.
- deliverable 1 (reach audit): every 2D raster call in PyAutoArray resolves its colormap from the config, because all three drawing modules default `colormap=None` and then call `_default_colormap()` — `plot/array.py:140-142 -> 180, 187` (`imshow`), `plot/grid.py:105-107 -> 118-124` (`scatter`), `plot/inversion.py:79-81 -> 198, 214, 269` (`imshow`/`pcolormesh`/`tripcolor`). Everything above them (`dataset/plot/`, `fit/plot/`, `inversion/plot/`, PyAutoGalaxy's `_resolve_colormap("default")` at `autogalaxy/util/plot_utils.py:97-102`, PyAutoLens `tracer_plots.py` / `sensitivity_plots.py` / `imaging/plot/fit_imaging_plots.py`) either threads `colormap` through or leaves it `None`. **No surface silently ignores the key.** `plot_yx` is a 1D line plot and takes no colormap.
- deliverable 1, deliberate exceptions — now documented in `autoarray/config/visualize/README.md` instead of left silent, and all left unchanged because the map carries meaning: `plot/array.py:208` `cmap="Greys"` for `array_overlay` (must contrast with whatever the main array uses); `autolens/weak/plot/weak_dataset_plots.py` `viridis`/`twilight` (cyclic data needs a cyclic map)/`magma`; `autolens/weak/plot/fit_weak_plots.py:119` `RdBu_r` (diverging, centred on the median residual); `autolens/weak/plot/convergence_plots.py:202` `magma`; `autolens/cluster/plot/cluster_plots.py:49` `CLUSTER_CMAP = "gnuplot2"`; `autolens/potential_correction/*` and `autogalaxy/gui/clicker.py` `jet` (research + interactive-GUI paths).
- deliverable 2 (per-figure override): the route already existed — `colormap=` on any plot function — so no new code was written, only documentation and a test. The "use the config value" default is spelled `None` in PyAutoArray and PyAutoLens but `"default"` in PyAutoGalaxy; worth knowing before touching either.
- deliverable 3 (the silent fallback): `_default_colormap()` now separates *absent* from *malformed*. No `autonerves`, or no `colormap` key on the config path (a bare install with no workspace) -> quiet fallback to the bundled `autoarray` map, as before; a value matplotlib cannot resolve -> `ValueError` naming the key, the value and the fix. The bare `except Exception` is replaced by `ImportError` / `(KeyError, ConfigException)`. Siblings tightened the same way: `_conf_imshow_origin()` (additionally rejects anything but `upper`/`lower`) and `_conf_output_format()` (left to matplotlib's own `savefig` error, which already names the format and lists the supported ones). New private helper `autoarray.plot.utils._validate_colormap(name)`.
- deliverable 4 (magma): `euclid_strong_lens_modeling_pipeline/config/visualize/general.yaml` `colormap: autoarray` -> `colormap: magma`. PyAutoArray and `autolens_workspace` deliberately keep `autoarray` — the user request scoped magma to the Euclid repo, and the prompt said so explicitly.
- deliverable 5 (docs): `autoarray/config/visualize/README.md` gains a "Changing the colormap" section (config key, per-figure override, the figures that deliberately ignore both); the Euclid repo gains the same section in `config/visualize/README.md` plus a short **Visualization** section in its top-level `README.md`, so the lever is discoverable without opening the config folder.
- API changes: none — `_default_colormap`, `_conf_imshow_origin`, `_conf_output_format` are private, and the `colormap` config key and every public `colormap=` argument keep their names and defaults. One user-visible **behaviour** change: a `colormap` or `imshow_origin` value that was previously ignored now raises `ValueError` at plot time instead of silently reverting. Any config that was actually working is unaffected.
- validation: `test_autoarray` 1337 passed / 0 failed; 11 new tests in `test_autoarray/plot/test_utils.py` (config value returned, absent key -> quiet `autoarray` fallback + registration, unknown name -> `ValueError`, non-string -> `ValueError`, per-figure `colormap=` beats config, one config edit moves both `plot_array` and `plot_inversion_reconstruction`). **Control-tested**: the three cmap-spy assertions were flipped to a sentinel and confirmed to fail, so they really observe the cmap handed to `imshow`. Acceptance demo rendered an imaging `Array2D` figure and a rectangular-mapper inversion reconstruction under `colormap: magma` — both visually magma from the one config edit — and a malformed value raised the new error. The euclid PR is config + docs only: no scripts changed, so no notebook regeneration and no smoke run were needed.
- CI at merge: PyAutoArray `Tests [pull_request]` green on all three legs (3.12, 3.13, `unittest-nojax`) for `c8fe47f3`. Only a `pull_request` run exists and that is correct — `main.yml` is `on: push: branches: [main]` + `pull_request`, so a feature sha gets one run, not two.
- trap for later: **the euclid pipeline repo runs no CI of its own.** Its only workflow, `.github/workflows/url_check.yml`, was deleted in `7ff9405` ("URL hygiene centralised in PyAutoPulse"), so the repo now has zero workflow files on `main` while sibling workspaces (autolens_workspace, autogalaxy_workspace, HowToLens) still carry three. A PR there returns an **empty run list and an empty `statusCheckRollup` with `mergeStateStatus: CLEAN`** — which is `/prm` step 3's "no checks configured", not green CI, and not the CONFLICTING/path-filter causes the skill lists first. Diagnose it as such next time rather than reading `CLEAN` as a pass.
- heart-ack: PRs were opened and merged under the standing human authorisation recorded 2026-08-28 ("open prs under red and merge i acknowledge"). Heart was RED for an unrelated reason, verbatim: "release validation FAILED (stage integrate)"; YELLOW, also unrelated, verbatim: "workspace validation not passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py, autolens_test scripts/imaging/rectangular_mge_rtu.py)"; "manifest drift: session-start hooks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml". No interferometer, inversion-solve or hook code was touched by this branch.

## Original prompt

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
