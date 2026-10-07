## eyes-fit-cti-instances
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/455
- completed: 2026-09-29
- epic: pyautoeyes-birth (phase 4)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/431
- library-pr: https://github.com/PyAutoLabs/autofit_visualization/pull/1
- library-pr: https://github.com/PyAutoLabs/autocti_visualization/pull/1
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/456
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/244
- library-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/5
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/180
- library-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/16
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/49

### What shipped
- **autofit_visualization#1** (merge b2063ad) — the fit project repo: 4 flat producers (`samples`, `model`, `ep`, `visualizer`) rendering 49 tracked PNGs on `gaussian_x1` with real cheap searches (both corner plots for DynestyStatic/Nautilus/Emcee/Zeus, six LBFGS MLE variants, MultiStartAdam figure-of-merit; `ModelPlotter` variants; the EP graph/state/factor figures and `EPPlotter`; `VisualizerExample`); tracked JSON datasets; all-true config with `model_figure` and `force_visualize_overwrite`; `lint.yml` + `render.yml` (`pyautofit-release`, fires `eyes-refresh`). No `instruments/` (1D toy data). Full render 2–5 min (EP is the slow domain).
- **autocti_visualization#1** (merge b8575e9) — the cti project repo: 2 flat producers (`dataset_1d`, `imaging_ci`) rendering 135 tracked PNGs (7 MB, 45 s) via the `VisualizerDataset1D` / `VisualizerImagingCI` lifecycles on tiny simulated charge-injection data (parallel+serial 30×30 with non-uniform injection and cosmic rays, a parallel-only source, three-normalisation 1D) plus direct `aplt` calls for the fit quantities the visualizers never write; fits from the true model without a search; `lint.yml`/`render.yml` use the central Heart `install-arcticpy` action (`pyautocti-release`). Trimmed from a 731-PNG cross product to one call per figure kind.
- **PyAutoEyes#5** (merge 6b12101) — registry rows `fit` and `cti`, tests, four-instance prose, dashboard regenerated (265 figures: lens 40 / galaxy 41 / fit 49 / cti 135).
- **PyAutoMind#456** (merge 49f79da) — body-map rows, PyAutoEyes role names all four `<lib>_visualization` repos, ROUTING and epics.
- **PyAutoHeart#244** (merge 518ce45) — drift exclusions for both repos.
- **PyAutoBrain#431** (merge 711257a) — Eyes conductor / skill / docs prose; no conductor code (flat layout keeps `_eyes.py` repo-name-free).
- **PyAutoNerves#180, PyAutoGut#16, PyAutoCortex#49** (merges 1ec1c82, d854afc, 438a7fc) — `repos_sync` map blocks.
- **Org-level `PAT_PYAUTOLABS`** (human, same day): the token moved from three repo-level secrets (Mind/Brain/Hands, since deleted) to ONE organization secret visible to all public repos; verified by autogalaxy_visualization render run 36606190174 dispatching `eyes-refresh` → PyAutoEyes' first `repository_dispatch` Dashboard Refresh (green). No per-repo PAT step remains for future project repos.

### Witness evidence
- Delivered: `pyauto-brain eyes survey` on both repos (no gaps/orphans/stale); `gallery_build.py --check` green with tracked manifests in both; `pyauto-eyes check` green over all four registry rows; dashboard shows fit and cti sections.
- **Not delivered:** `repos_sync.py --check` "clean" — after the map-block merges it still reports the pre-existing 25 hook-copy drifts, the undeclared `COWLS_COSMOS_Web_Lens_Survey` root checkout and the `.github` profile organ table (human patch on #455).

### Traps / notes
- PyAutoFit and PyAutoCTI have NO plotter classes any more: sampler plots are functions in `autofit.plot` (`figure_of_merit_vs_iteration` is only in `autofit.non_linear.plot`); autocti's are `aplt.*` functions. Only `ModelPlotter`, `EPPlotter`, `Visualizer` remain as classes.
- A parallel session's `worktree_create` rewrote the shared root `activate.sh` mid-task; a sourced bundle activate then pointed `repos_sync --write` at the other bundle and spilled into canonical checkouts (reverted). Give subagents a private env copy and assert `PYAUTO_ROOT` before `--write`.
- Mind#456's firewall and Eyes#5's lint were red by construction until Brain / the project repos merged, and a `pull_request` re-run reuses its merge commit — the branches had to move (merge main in) to go green.
- Unseeded dynesty/emcee/zeus in the fit repo mean re-renders change PNG bytes; the `rendered_with` stamp is the source-checkout version (2026.8.17.1).
- Heart YELLOW acknowledged by the human at ship (four unrelated reasons, recorded on #455).

### Review candidates (for a later `/eyes review`)
- fit: `corner_anesthetic` sets the global matplotlib `font.size` and never restores it — every figure rendered after it carries larger text.
- cti: masked cosmic-ray panel renders all zeros; colourbars labelled `e- s^-1`; signal-to-noise panels clip negatives; `VisualizerDataset1D.visualize` writes a `dataset_full` fit into `fit_dataset/` with no `_full` suffix (unlike ImagingCI).

### Not verified / human follow-ups
- Apply the `.github` profile README patch pasted on #455.
- Nothing sends `pyautofit-release` / `pyautocti-release` yet (`draft/feature/pyautohands/release_fires_visualization_dispatch.md`); `render.yml` runs by `workflow_dispatch` until it ships.

## Original prompt

# PyAutoEyes phase 4 — birth autofit_visualization + autocti_visualization

Type: feature
Target: autofit_visualization
Repos:
- autofit_visualization
- autocti_visualization
- PyAutoEyes
- PyAutoMind
- PyAutoBrain
- PyAutoHeart
Themes:
- visualization
- infrastructure
Difficulty: large
Autonomy: supervised
Priority: normal
Lane: local-dev
Status: active
Consequence: judge
Witness: the fit and cti project-repo surveys report no gaps/orphans; each repo's `gallery_build.py --check` green with a tracked manifest; `pyauto-eyes check` green over all four registry rows; the PyAutoEyes dashboard shows fit and cti sections; `repos_sync.py --check` clean
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 4
Filed: 2026-09-25
Issued: 2026-09-29

Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/455 — both repos created 2026-09-29.

## Task

Two project repos, same steps as phase 3:

- `fit/autofit_visualization` — ModelPlotter, EPPlotter, VisualizerExample on
  `gaussian_x1`.
- `cti/autocti_visualization` — Dataset1D + ImagingCI visualizers, simulated
  from `autocti_workspace/scripts/*/simulators`.

Each: flat producers, all-true `plots.yaml`, simulated datasets, render
harness, tracked PNGs + `GALLERY.md` + tracked manifest, `lint.yml` +
`render.yml` on its library's release dispatch (`pyautofit-release`,
`pyautocti-release`) firing `eyes-refresh`; Mind/Brain/Heart registration as
phase 1a; PyAutoEyes `registry.yaml` rows.
