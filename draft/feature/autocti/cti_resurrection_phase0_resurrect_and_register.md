# CTI resurrection — Phase 0: resurrect PyAutoCTI + register the CTI repos in the ecosystem

Type: feature
Target: PyAutoCTI
Repos:
- @PyAutoCTI
- @PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 0 of the **CTI resurrection epic**: bring PyAutoCTI, autocti_workspace
and autocti_workspace_test back into the PyAutoLabs ecosystem after ~2 years
unmaintained (PyAutoCTI/autocti_workspace last pushed 2024-11-13;
autocti_workspace_test 2023-02-21).

## Epic overview (6 phases — later phases get their own prompts as each predecessor nears shipping)

- **Phase 0 (this prompt)** — resurrect + register: repos into the workspace +
  org, `repos.yaml`, arcticpy spike, packaging modernisation, import-clean
  against the current stack, unit tests green.
- **Phase 1** — visualization migration: delete the Plotter/PlotterInterface
  object stack (5 Plotter + 3 PlotterInterface classes across
  `charge_injection` and `dataset_1d`) in favour of per-domain
  `plot/*_plots.py` matplotlib function modules + `model/visualizer.py`
  (`af.Visualizer`), mirroring PyAutoGalaxy. CTI-specific region overlays
  (`ParallelOverscanPlot`, `SerialOverscanPlot`, `SerialPrescanPlot`, FPR/EPER
  extracts) were autoarray `wrap` objects that no longer exist — they become
  CTI-local matplotlib helpers.
- **Phase 2** — autofit sync: Analysis/Visualizer contract, aggregator,
  searches (current Nautilus, drop stale `ultranest==3.6.2` pin or refresh),
  output-format drift.
- **Phase 3** — CI + ecosystem plumbing: replace 2-year-old GitHub Actions
  (`checkout@v2`, `set-output`), PyAutoBuild release path (navigator already
  lists autocti), Heart registration, docs hub + RTD revival.
- **Phase 4** — autocti_workspace update: 118 scripts / 79 notebooks
  (dataset_1d, imaging_ci, overview, plot) onto the new viz + autofit APIs;
  config schema sync; docs cleanup.
- **Phase 5** — autocti_workspace_test rebuild (on the autogalaxy_workspace_test
  template; preserve the Euclid `tvac/`, `temporal/`, `euclid/`, `validation/`
  heritage content) + first modern release of `autocti` to PyPI.

## Phase 0 scope

1. **Org + workspace registration.** The CTI repos are still under
   `Jammy2211/` — every other ecosystem repo migrated to the `PyAutoLabs` org.
   Transfer PyAutoCTI, autocti_workspace, autocti_workspace_test to
   `PyAutoLabs/`, clone them into `~/Code/PyAutoLabs/`, add them to
   `PyAutoMind/repos.yaml`, and run `repos_sync.py --write` to regenerate the
   routing tables.
2. **arcticpy install spike (THE risk).** `autocti/__init__.py` imports the
   clockers eagerly → `arcticpy` (pinned 2.6) is a hard import. PyPI has only
   a source tarball (Dec 2023, C++, no wheels, no declared deps). Verify it
   builds/imports on Python 3.11/3.12 with modern numpy; fallbacks in order:
   lazy clocker import (autocti imports without arctic), patched arcticpy
   re-release, vendoring.
3. **Packaging modernisation.** Old-style `setup.py` with exact
   `autoconf/autofit/autoarray=={VERSION}` pins → `pyproject.toml` with
   floor deps and dynamic version, matching PyAutoGalaxy (floors-not-pins
   redesign).
4. **Import-clean against the current stack.** ~60 broken imports vs installed
   autoconf/autofit/autoarray, of which ~45 are the removed Plotter/mat_plot/
   wrap/visuals layer (deferred to Phase 1). Phase 0 fixes the ~15 non-viz
   breaks (e.g. `autoarray Mask` → `Mask1D/Mask2D`, module renames,
   `mcmc_plotters`/`mle_plotters`/`nest_plotters` fallout) so `import autocti`
   succeeds with the plot subpackage temporarily quarantined/stubbed.
5. **Unit tests green.** The 96-file `test_autocti` suite collecting and
   passing minus the plot tests (skipped/quarantined until Phase 1);
   numpy-only, no JAX in unit tests.

Core structural autoarray API CTI needs (Array1D/2D, Mask1D/2D, Layout1D/2D,
Region1D/2D, `fit_util`, `geometry_util`) still exists — non-viz drift is
modest. Full survey facts: memory `project-cti-resurrection-epic-scoped`
(2026-07-16 session).

## Original request (verbatim)

> You'll see that I used gto work on CTI (PyAutoCTI, autocti_workspace,
> autocti_workspace_test), but its been around 2 years and these repos have
> become outdated, and un maintained. With fable, i now have the time and
> capacity to bring them back into the PyAuto ecosystem. Can you scope out an
> epic task which will bring them back into the ecosystem, update them to be
> in sync with the new autofit, update them to use the vsiualization API now
> used on autolens and other projects (e.g. epic removal of Plotter objects in
> favour of matplotlib) and whateevr else you think is required? I guess also
> docs clean up, etc. So, broadly speaking, look at the CTI repos and stage
> how we update them and then well do the work.
