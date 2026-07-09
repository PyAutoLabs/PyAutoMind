# PYAUTO_SMALL_DATASETS support for cluster lensing (fast workspace test runs)

Type: feature
Target: cluster
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Add PYAUTO_SMALL_DATASETS support for cluster lensing, so workspace test runs of the cluster
scripts run fast the way other datasets do.

Original request (verbatim): "Can you add a PyAutoMind prompt to add PYAUTO_SMALL_DATASET support
for cluster lensing, which makes it so workspace test runs run fast and is used for other
datasets. This may already be there due to point source models but is worth a task."

Grounding (2026-07-09 session):

- PYAUTO_SMALL_DATASETS already exists and covers parts of the path: PointSolver has a documented
  smoke-test short-circuit (autolens/point/solver/point_solver.py:87-111), and PyAutoArray
  downsizes masks/grids/over-sampling (mask_2d.py, uniform_2d.py, dataset_util.py,
  over_sample_util.py). So the point-source *solve* is already fast-mode aware.
- Despite that, cluster/start_here.py and cluster/modeling.py exceed 500 s under
  PYAUTO_TEST_MODE=2 even on clean main (control-verified 2026-07-08) and are parked in
  PyAutoBuild no_run.yaml:32-33 ("test mode breaks it"). PyAutoBuild env_vars.yaml has NO cluster
  entries, so the flag is never even applied to them in CI. The un-parking of these two scripts is
  the concrete success criterion for this task.
- Suspected remaining hot spots to profile and fix under the flag: (a) the cluster simulator
  auto-regeneration (JAX PointSolver JIT compile + full-resolution imaging sim at 0.1"/px over an
  arcminute field) — small-mode should shrink the imaging grid and/or skip the imaging leg;
  (b) the 149-profile lenstool example scripts (scripts/cluster/lenstool/): data.py downloads a
  96 MB mosaic (small-mode should skip the cutout leg) and modeling.py's tracer operations scale
  with profile count; (c) tracer/critical-curve visualization on multi-plane cluster tracers
  (known ~10 min/plane in numpy — the same cost that forced tracer.png regeneration to be dropped
  in autolens_workspace#238 and MAKE_FIGURES gating in #240).
- Beware the known env-flag footguns: PYAUTO_SMALL_DATASETS mutates Grid2D.uniform inside
  decorators, so trace the full call path when extending it (memory: smoke-env grid mutations);
  and fixes belong in config/build/env_vars.yaml overrides, never os.environ mutation in scripts.
- Deliverables: (1) extend/verify small-dataset behaviour across the cluster path (simulator,
  modeling, start_here, lenstool example, csv_api/likelihood_function as needed); (2) add cluster
  entries to PyAutoBuild env_vars.yaml; (3) un-park cluster/start_here + cluster/modeling from
  no_run.yaml with a timed CI-green run as evidence; (4) consider promoting the new lenstool
  example scripts into the smoke set (small curated subset rule — only if genuinely fast).

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/fa55f70e-2cea-4887-bf12-61f81cff042f/scratchpad/intake_small_datasets.md -->

__Addendum (user direction, 2026-07-09): standardize the auto-simulation guard__

Data-consuming workspace scripts should use the canonical auto-simulation pattern, as the imaging
scripts do:

    if al.util.dataset.should_simulate(str(dataset_path)):
        import subprocess, sys
        subprocess.run([sys.executable, "scripts/cluster/simulator.py"], check=True)

The cluster scripts currently use hand-rolled existence checks (`modeling.py` / `start_here.py`
test data.fits + scaling_galaxies.csv manually) and `lenstool/data.py` uses its own download
caching. As part of this task, migrate the cluster scripts to `al.util.dataset.should_simulate`
— which also carries the PYAUTO_SMALL_DATASETS delete-and-regenerate semantic that makes the
small-mode dataset actually get built small (see autoarray/util/dataset_util.py). The weak-lensing
twin of this migration is already in flight (weak-viz-profiles, PyAutoLens#581, plus
feature/weak/9_small_datasets.md) — mirror its conventions so imaging, weak and cluster all tell
the same auto-sim story. For lenstool/data.py, downloads are not simulations: keep the download
caching, but gate the expensive legs (96 MB mosaic/cutout) off under PYAUTO_SMALL_DATASETS.
