# Set galaxy-scale PointSolver grid extents per workspace package (evidence-backed, after the library sanity check)

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
- autolens_workspace_test
- HowToLens
Themes:
- point-source
- profiling
- ci-smoke
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-decision
Epic: point-source-cpu-speed
Filed: 2026-09-26
Parent: active/pointsolver_cpu_speed_phase_4.md (issue autolens_profiling#314)
Depends-on: draft/feature/autolens/pointsolver_extent_sanity_check.md (library first)

## Human decision (2026-09-26, live)

> "I think +-3" is a bit small for galaxy scale lenses and I think we would need to update it in
> workspace accordingly for each package. but +-10" still wont do clusters well so I think a
> workspace level task is right. We probabbly need some sort of a sanity check that prints or alerts
> the user? and warning based on the extent of the masked data (or the Point dataset)?"

This is a **workspace-level** task. There is no library default change for the extent.

## Goal

Set the **galaxy-scale** point-source solver grids in each workspace package to an extent justified by
the phase-4a evidence, and explain the choice in the scripts' prose (why this extent, and what to do
for a larger lens). Leave **cluster** (and group-scale) scripts alone: they belong to epic
`cluster-pointsolver-speed`.

**Proposal, to be decided at start_dev (not yet decided):** ±4″ to ±6″ extent, with a **0.4″
initial scale** where it stays precision-equivalent.
- Scale 0.4 keeps the default's 0.0016″ last-step triangle side, because it adds one refinement step.
- At full extent, 0.4 is 1.43× and gives log L identical to the default on 200/200 prior draws.

The candidate settings (±9.9″/0.2 control 1.824 ms) are:

| extent | scale 0.2 | scale 0.4 | step-0 rows at 0.2 → 0.4 |
|---|---:|---:|---:|
| ±6″ | 1.52× | (not run) | 4 428 → — |
| ±4″ | 1.78× | 2.15× | 2 075 → 559 |
| ±3″ (rejected by the human as too small for galaxy scale) | 2.05× | 2.23× | 1 197 → 330 |

- Scale 0.5 is **not** precision-equivalent (0.0020″) and drops 2/200 stress images.
- Scale 0.8 is inadmissible.
- ±6″/0.4 was not measured. Run it with the sweep cell before choosing ±6″, or accept ±6″/0.2.
- The prompt-3 warning validates each chosen extent against that package's own data.

## Evidence

- Source: `lens/autolens_profiling/results/breakdown/point_source_image/solver_config_sweep_hpc_ral_cpu_fp64.json`,
  RAL job 356367, Xeon 8490H, fp64.
- Harness: `lens/autolens_profiling/scripts/point_source_image/likelihood_breakdown/solver_config_sweep.py`.
- Ledger: `lens/autolens_profiling/results/notes/point_source_cpu_campaign.md`, "Phase 4a".
- The images on the workspace prior reach max radius 1.81″; the broad stress set reaches 2.52″.
- Step 0 is ≈ 66 % of the likelihood (1.21 ms of it containment at ±9.9″/0.2).
- Phase 4b (`draft/feature/autoarray/pointsolver_step0_gather_containment.md`) may shrink the gain from
  a smaller extent. **Re-measure after 4b lands** if it lands first, and keep the extent choice
  primarily a correctness/prose decision.

## Inventory (grep of `PointSolver.for_grid` on 2026-09-26, `.py` scripts; notebooks regenerate)

68 files mention `PointSolver`: 46 autolens_workspace, 17 autolens_workspace_test, 5 HowToLens,
0 autolens_assistant, 0 autogalaxy_workspace. The extent is the half-width of the
`Grid2D.uniform(shape_native, pixel_scales)` passed to `for_grid`. Precision is `1e-3` unless noted.

**In scope: galaxy-scale modeling / fit / likelihood solvers (all ±10″ @ 0.2 today)**
- autolens_workspace `scripts/point_source/`: `start_here.py` L186, `modeling.py` L167, `fit.py` L162,
  `plot.py` L110, `features/time_delays.py` L124, `features/fluxes.py` L123,
  `features/extra_galaxies/modeling.py` L146, `features/scaling_relation/modeling.py` L123.
- autolens_workspace: `scripts/multi_dataset/features/imaging_and_point_source/modeling.py` L270, and
  `scripts/guides/modeling/advanced/graphical.py` L110.
- autolens_workspace_test `scripts/point_source/`:
  - `jax_likelihood/{image_plane.py L101, source_plane.py L114, point.py L141, fluxes_time_delays.py L110}`;
  - `jax_grad/gradient.py` L119, and L334 at precision 1e-5;
  - `visualization/{visualization.py L62, visualization_jax.py L65, modeling_visualization_jit.py L86}`;
  - `simulators/simple.py` L55.
  - **Their rtol log-L pins must not move.** Extent-only and the 0.4 scale reproduced the control's
    log L exactly on the sweep draws, but re-run every pin.
- HowToLens: `scripts/chapter_1_introduction/tutorial_4_point_sources.py` L228.

**Simulators and guides (judge at start_dev; these are one-off solves, not per-likelihood cost)**
- ±5″ @ 0.05, used to simulate the data positions: autolens_workspace `point_source/simulator.py`
  L138, `point_source/simulator_sample.py` L77, `features/{deblending,extra_galaxies,multiple_sources,scaling_relation}/simulator.py`,
  `features/scaling_relation/{likelihood_function.py L179, fit.py L153}`, and
  `features/multiple_sources/modeling.py` L120. Also autolens_workspace_test
  `point_source/simulators/point_source.py` L86.
- Positions for imaging/interferometer simulators: `imaging/simulator.py` (±5″ @ 0.1),
  `interferometer/simulator.py` (±12.8″ @ 0.1 and ±4″ @ 0.01), `multi_galaxy/*/simulator.py`
  (±12.5″ @ 0.05), and HowToLens `simulator/no_lens_light.py` (±5″ @ 0.1).
- Guides: `guides/plot/visuals.py` ±2.5″ @ 0.05, `guides/misc/witt_wynne.py` ±5″ / ±3″ @ 0.05,
  `guides/mappings.py` ±5″ @ 0.1, and `point_source/simulator.py` L507 (±50″ @ 1.0, a JAX demo).

**Out of scope: cluster and group**
- autolens_workspace `scripts/cluster/*` (±50–70″ @ 0.7–1.4) and `weak/features/strong_lensing/a2744.py`.
- `group/*/simulator.py` (±25″ @ 0.1).
- autolens_workspace_test `cluster/*`.
- HowToLens `simulator/{cluster,group}.py` and `chapter_4_scaling_up_lensing/tutorial_5_cluster_scale.py`.

## Method

1. Library first: prompt 3's warning must be released, or on a same-named branch, so each new extent
   is validated against that script's own dataset. It must stay silent on the edge check.
2. Decide the extent and scale with the human (the proposal above). Measure ±6″/0.4 if it is a
   candidate.
3. Edit the in-scope scripts. Add prose that explains the extent: images of a galaxy-scale lens lie
   within ~θ_E/√q + |β| of the centre, so the grid must cover them with margin, and a larger lens or
   an offset centre needs a larger grid. Point cluster users to the cluster package.
4. Regenerate notebooks per workspace convention. Run the workspace_test point_source pins and the
   smoke tests.
