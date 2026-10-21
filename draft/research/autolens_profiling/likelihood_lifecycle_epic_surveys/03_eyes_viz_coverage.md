# Survey 03 — PyAutoEyes and autolens_visualization coverage per dataset type (2026-10-21, Explore worker, read-only)

## Headline

The work the "Eyes on all dataset types" phase describes has already shipped. Issue PyAutoLabs/autolens_visualization#4 ("feat: visualize every PyAutoLens dataset type (dataset + fit) and group on Eyes") is CLOSED, and PR #5 `feature/viz-all-dataset-types` was merged on 2026-10-21 (merge 1f65e89). The Mind completion record is `organs/PyAutoMind/complete/2026/10/viz-all-dataset-types.md`. It says: "autolens_visualization and PyAutoEyes now cover every PyAutoLens dataset type… each writing only `dataset.png` + `fit.png`". Its stated follow-up is "Bespoke point-source, cluster and weak visualizations, driven by the human through the Eyes dashboard."

All 10 dataset types have a producer and at least one `fit.png` in the manifest. That manifest is `lens/autolens_visualization/gallery/viz_manifest.yaml`: schema 1, generated 2026-10-21, autolens 2026.8.17.1, figure_count 72. All 72 PNGs are on disk, and the checkout is clean at `main` = origin/main, HEAD 33e23a1.

## Table: dataset type → producer → fit figure → dataset

All paths are under `lens/autolens_visualization/`. "Manifest line" is the line in `gallery/viz_manifest.yaml`.

| Dataset type | Producer (domain) | fit*.png present (manifest line) | Other figures | Dataset used |
|---|---|---|---|---|
| imaging | `scripts/imaging/visualization.py` | YES: `parametric/fit.png` (:139), `delaunay/fit.png` (:73), plus `fit_log10`, `fit_of_plane_0/1` | Full VisualizerImaging set: dataset, adapt_images, image_with_positions, tracer, galaxies, inversion, mappings | `dataset/imaging/hst`: 0.05"/pix, 141x141, 21x21 Gaussian PSF, mask 3.5". Copied byte-for-byte from autolens_profiling |
| interferometer | `scripts/interferometer/visualization.py` | YES: `parametric/fit.png` (:259), `delaunay/fit.png` (:205), plus `fit_dirty_images`, `fit_real_space` | Full VisualizerInterferometer set | `dataset/interferometer/sma`: SMA preset, 190 visibilities, 256x256 at 0.1"/pix, DFT |
| point source, image-plane chi² | `scripts/point_source_image_chi_squared/visualization.py` | YES: `fit.png` (:379), `fit_image_with_points.png` | dataset, image_with_points, point_solver, `teaching/point_solver.png` | `dataset/point_source/simple`: 4 positions, 5 mas noise (shared) |
| point source, source-plane chi² | `scripts/point_source_source_chi_squared/visualization.py` | YES: `fit.png` (:415), `fit_image_with_points.png` | dataset, image_with_points | `dataset/point_source/simple` (shared) |
| multi_galaxy | `scripts/multi_galaxy/visualization.py` | YES: `fit.png` (:367), dataset + fit only | — | `dataset/multi_galaxy/simple`: 0.05"/pix, 140x140, two lenses + shear + light-only extra galaxy |
| group | `scripts/group/visualization.py` | YES: `fit.png` (:55), dataset + fit only, galaxy-scale imaging plots | — | `dataset/group/simple`: 0.1"/pix, 160x160, main lens + 2 dPIE extras. Extended imaging only, no point source |
| cluster | `scripts/cluster/visualization.py` | YES: `point_0/fit.png` (:19), `point_1/fit.png` (:37) | per-source dataset, point_solver | `dataset/cluster/simple`: 2 point sources at z=1, 2 (5 and 2 images), source-plane chi² only. Generic point plots, called via PlotterPoint |
| multi dataset (multi-band) | `scripts/multi_dataset/visualization.py` | YES: `g/fit.png` (:343), `r/fit.png` (:355) | per-band dataset | `dataset/multi_dataset/lens_sersic`: g 0.08"/pix, r 0.12"/pix, 80x80 |
| datacube | `scripts/interferometer_datacube/visualization.py` | YES: `channel_{0,1,2}/fit.png` (:307, :319, :331) | per-channel dataset | `dataset/interferometer/datacube`: 3 channels, SMA uv-coverage. Interferometer only, no IFU/imaging cube |
| weak lensing | `scripts/weak/visualization.py` | YES: `fit.png` (:439), renamed from `subplot_fit_weak.png` | dataset | `dataset/weak/simple`: 1500 shears in a 50"–200" annulus, shape noise 0.25 |

Gaps left within "all types", for the epic to consider:
- **Imaging and interferometer only** have the full figure set and parametric plus Delaunay variants. The other eight types have only dataset and fit.
- **Cluster** has no image-plane chi² variant and no extended-source variant.
- **Group** has no point-source variant.
- **Point, cluster and weak** have no bespoke figures. The producer docstrings and the completion record list these as follow-ups.
- **Profiling datasets differ.** Only imaging/hst is shared with autolens_profiling. The other viz datasets are separate seeded simulations (`scripts/misc/simulators/*.py`, `true_models/`).

### Tree (depth 2)
- `gallery/`: `gallery_build.py`, `gallery_run.sh`, `viz_manifest.yaml`
- `scripts/`: `cluster/`, `group/`, `imaging/`, `interferometer/`, `interferometer_datacube/`, `multi_dataset/`, `multi_galaxy/`, `point_source_image_chi_squared/`, `point_source_source_chi_squared/`, `weak/`. Each holds `visualization.py` and `images/`.
- `scripts/misc/`: `simulators/` (cluster, datacube, group, imaging, interferometer, multi_dataset, multi_galaxy, point_source, weak) and `test/` (test_eyes_scratch, test_gallery_build).
- `dataset/`: cluster/simple, group/simple, imaging/hst, interferometer/{sma,datacube}, multi_dataset/lens_sersic, multi_galaxy/simple, point_source/simple, weak/simple.
- `config/visualize/plots.yaml`, `instruments/{imaging,interferometer}.py`, `_viz_cli.py`, `GALLERY.md` (415 lines, one `##` section per domain).
- The harness also mirrors renders to an opt-in Eyes scratch folder via `PYAUTO_EYES_SCRATCH` (`README.md:55-56`, `_viz_cli.py:217-262`).

## 1. PyAutoEyes contract and registry

All paths are under `organs/PyAutoEyes/`.

**Manifest contract, "Figure manifest: schema 1"** (`REFERENCE.md:20-72`):
- **Where it lives:** the project repo commits it at the registry's `manifest:` path. It is generated by `gallery/gallery_build.py` and never hand-edited (`:22-25`).
- **Top-level keys** (`:28-36`): `schema` (int), `generated` (date), `rendered_with` (package→version map), `figure_count` (== len(figures)), `figures`.
- **Per-figure keys** (`:37-42`): `file` (repo-relative .png), `producer`, `domain`, `source` (sub-variant), `bytes`, `sha256` (64 hex).
- **Required** (`:45-48`): every key. `rendered_with` must be non-empty and should include `import_name`. Each `file` is unique.
- **What the organ reads** (`:50-56`): `file` → `<images_base_url><file>` link; `domain`/`source` → grouping; `rendered_with[import_name]` + `generated` → freshness; `bytes`/`sha256` → `check`. `producer` goes to the conductor and is not displayed.
- **Domain order** (`:58-60`): one browser per domain, alphabetical, mirroring `scripts/<domain>/`.
- **Versioning** (`:62-72`): additive changes stay on schema 1; breaking changes bump it, and the organ learns the new version first. Today `eyes/manifest.py:23` has `SUPPORTED_SCHEMAS = (1,)`.

**Registry** (`registry.yaml`, schema 1; fields at `REFERENCE.md:74-98`). Rows pin no commits or versions. Each row carries `name, repo, path, github, library, import_name, manifest, images_base_url (…/main/), gallery, dispatch_event`, and freshness comes from the manifest's `rendered_with`.

| name | repo / path | library | dispatch_event |
|---|---|---|---|
| lens | autolens_visualization / lens/autolens_visualization | PyAutoLens (autolens) | pyautolens-release |
| galaxy | autogalaxy_visualization / galaxy/… | PyAutoGalaxy | pyautogalaxy-release |
| fit | autofit_visualization / fit/… | PyAutoFit | pyautofit-release |
| cti | autocti_visualization / cti/… | PyAutoCTI | pyautocti-release |

All four use `manifest: gallery/viz_manifest.yaml` and `gallery: GALLERY.md`.

## 3. Mind drafts (both stale or largely superseded)

Both drafts are still in `draft/` and still shown on the Mind dashboard (`dashboard.md:796-807`).

**`draft/feature/pyautoeyes/multi_galaxy_gallery.md`** (Epic pyautoeyes-birth, Phase 6, medium, supervised, draft, filed 2026-09-25)
1. Scope: add a multi_galaxy domain, with an HST-scale dataset (lens + companion/LOS galaxy) and its simulator.
2. Producer to follow the full imaging pattern: all-true plots.yaml, parametric and Delaunay sources.
3. Harness, manifest, GALLERY.md and lint/render workflows to cover it.
4. Witness: `gallery_build.py --check` passes, and the Eyes survey shows 0 gaps and 0 orphans.
5. Status vs reality: the domain, dataset, simulator and producer already exist from PR #5. Only the full figure set and the parametric/Delaunay variants remain undone.

**`draft/feature/pyautoeyes/group_cluster_gallery.md`** (Epic pyautoeyes-birth, Phase 7, large, supervised, draft, filed 2026-09-25)
1. Scope: group and cluster galleries, each with both point-source and extended-source modelling.
2. Tracked datasets (positions/fluxes plus extended imaging), each with a simulator.
3. Flat producers for every visualizer output: FitPositions/flux figures and extended imaging figures.
4. References `autolens_workspace_test/scripts/cluster/visualization.py` and `scripts/point_source/visualization/`. Witness is `--check` plus 0 gaps and 0 orphans.
5. Status vs reality: group (extended only) and cluster (point, source-plane only) exist as dataset + fit. Still missing: group point-source, cluster extended imaging, cluster image-plane chi², and the full or bespoke figure sets.

## 4. Open issues

- `PyAutoLabs/autolens_visualization`: **0 open**. Closed issues: #4 (all dataset types) and #8 (Eyes scratch mirror). There are no open PRs.
- `PyAutoLabs/PyAutoEyes`: **0 open**. Recent closed issues: #32 (alphabetical domains), #29, #25 (one figure at a time), #16, #8, #6.

## 5. autolens_profiling: which figure is inspected

The files named never say which figure the human must inspect during a campaign. Grepping `fit.png|subplot_fit|fit_dataset` over `AGENTS.md`, `README.md`, `skills/` (only `skills/profile_likelihood/{SKILL.md,reference.md}`) and `_profile_cli.py` returns **zero matches**. The only figures they mention are timing plots:
- `skills/profile_likelihood/SKILL.md:34-36`: "`local_cpu_{fp64,mp}`, `local_gpu_{fp64,mp}`, `hpc_a100_{fp64,mp}`, and `comparison` — each a `.json` + `.png` pair."
- `_profile_cli.py:790`: `return results_dir / f"{basename}.json", results_dir / f"{basename}.png"`, the timing PNG.
- `AGENTS.md:66`: "trends stay inspectable across releases." This is about timing trends, not a fit figure.

Elsewhere in the repo, fit subplots are only rendered for timing:
- `scripts/{imaging/mge,interferometer/mge,interferometer/delaunay}/quick_update.py` and `scripts/point_source_image/image_plane/quick_update.py` call `subplot_fit_quick`. For example, `scripts/imaging/mge/quick_update.py:261`: `print("\n=== Phase 3: subplot_fit_quick rendering (6-panel) ===")`.
- They write into `tempfile.mkdtemp` (`scripts/imaging/mge/quick_update.py:206`; `scripts/point_source_image/image_plane/quick_update.py:129`), so nothing is kept for inspection.
- The Brain profiling conductor (`organs/PyAutoBrain/agents/conductors/profiling/AGENTS.md`) has no fit.png reference either.

So today no fit-figure inspection step is written into profiling. Its script types are cluster image/source-plane, datacube/delaunay, imaging (several), interferometer (several), lens, multi_dataset/delaunay and point_source_image/source. It has no group, multi_galaxy or weak scripts, even though `dataset/group` and `dataset/abell_1201` exist.

**What this leaves for the epic:** the Eyes coverage you would set up already exists. The real gaps are:
- (a) a fit-figure inspection step in profiling campaigns, for example keeping the `subplot_fit_quick` output or linking to the matching viz domain;
- (b) the follow-up variants left open in the two drafts;
- (c) bespoke point, cluster and weak figures.

The two drafts should be updated or re-scoped to those remaining items rather than duplicated.
