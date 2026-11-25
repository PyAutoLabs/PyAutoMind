## likelihood-lifecycle-p5c-galaxy-lens
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/881
- completed: 2026-11-24
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/752
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/882
- epic: likelihood-lifecycle (phase 5C; next 5B-3 lazy factory operator, then 5C-3 aggregator reapply, then 5D PyAutoFit)

Phase 5C of the likelihood-lifecycle epic shipped as two PRs under one issue. It wires the 5B `aa.Setup` into the analyses: `setup=` is opt-in per R6, and without it nothing changes beyond an "auto would choose …" log line.

- **5C-1, PyAutoGalaxy** (#752, merged 2026-11-24 as 5bcb54a9):
  - `setup=None | "auto" | aa.Setup | setup_id` on `AnalysisDataset` / `AnalysisImaging` / `AnalysisInterferometer`.
  - `resolve_setup(model)` runs first in `modify_before_fit`. It sets `_use_jax` from the setup's backend, calls `dataset.apply_setup`, runs the factory consistency check (via PyAutoArray's private `_check_*` helpers), calls `apply_threads` and logs the banner.
  - `files/setup.json`.
  - Rule key from the model's mesh: DelaunayNN → delaunay_nn, Delaunay* → delaunay, rectangular → rectangular, no mesh → mge. A missing row falls back, with a note in the banner.
  - New module `autogalaxy.analysis.setup_util`.
- **5C-2, PyAutoLens** (#882):
  - Lens imaging and interferometer pass `setup=` to the Galaxy base; `_xp` follows `_use_jax`.
  - `AnalysisPoint` / `AnalysisWeak` resolve through the `AnalysisSetupNoOperator` mixin. Point: a `FitPositionsSource` subclass → point_source_source/source_plane, else point_source_image/image_plane. Weak → weak/isothermal.
  - `al.exc.SetupException` is raised at the top of `log_likelihood_function`, outside `raise_fit_exception`, when a setup was given but never resolved (factor graphs). `fit_from` is unguarded.
- **Design calls (human-approved 2026-11-24):**
  1. Resolve at `modify_before_fit`; the banner is the authoritative report.
  2. No lens-scale hint arguments.
  3. Factor-graph setup agreement → 5D.
  4. SLaM one-setup → 5F.
- **Gate:**
  - 5C-1: 1641 tests; Heart dev GREEN; smoke 5/5.
  - 5C-2: 1086 passed + 1 xfailed; Heart dev GREEN; smoke 4/4. Both smoke runs were against the branch.
- **Scope added mid-phase (human-approved):** resolving only at `modify_before_fit` leaves calculations outside modeling on the slow dense route. Two follow-ups were filed:
  - `draft/feature/autoarray/likelihood_lifecycle_p5b3_array_lazy_factory_operator.md`: a lazy, size-gated operator in the inversion factory.
  - `draft/feature/autolens/likelihood_lifecycle_p5c3_aggregator_setup_reapply.md`: aggregator reloads reapply `setup.json`, and one shared resolution helper absorbs the duplicated `setup_environment`.
- **Traps:**
  - With no setup, `Environment.detect()` still runs every fit (about 1.4 s on the first call when `nvidia-smi` is present).
  - `log_fit_start`'s JAX line can be stale under a setup.
  - No cluster analysis class exists, so the `cluster/*` rules are unused.
  - The canonical PyAutoArray and PyAutoLens checkouts had to be fast-forwarded so the task worktree's symlinks saw the setup code.

## Original prompt

# Likelihood lifecycle phase 5C: PyAutoGalaxy + PyAutoLens `setup="auto"` (opt-in), `setup.json`, the setup banner, one setup through multi-dataset sums and SLaM, lens-scale keys resolved

Type: feature
Target: PyAutoLens
Repos:
- PyAutoGalaxy
- PyAutoLens
Themes:
- hpc-gpu
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/881
Consequence: judge
Witness: with PyAutoGalaxy and PyAutoLens main, `al.AnalysisImaging(dataset, setup="auto")` (and the interferometer, point, weak and multi-dataset analyses, plus their PyAutoGalaxy counterparts) resolves the setup through `aa.Setup.auto` with the lens-scale keys mapped by the caller (imaging/interferometer variant from the model's pixelization / linear light profiles; group, multi_galaxy, cluster and point-source keys from the analysis type), applies it once at construction (`dataset.apply_setup` plus the factory consistency check, so a mismatch raises at construction rather than becoming rejected samples mid-search), writes `setup.json` beside the search output, and prints the setup banner line at fit start. An explicit `al.Setup(...)`, a setup_id string or `PYAUTO_SETUP=<setup_id>` always wins, and `use_jax=` stays as an explicit override that maps onto a Setup. Without `setup=` the behaviour is unchanged apart from a one-line "auto would choose …" banner (R6: opt-in release first, default flipped in a later release). Unit tests cover every analysis type, with a monkeypatched `Environment`; full PyAutoGalaxy and PyAutoLens suites are green, and `pyauto-heart smoke --affected-by PyAutoLens` passes.
Review-minutes: 30
Unattended: no
Lane: any
Gate: 5B MERGED (PyAutoArray#709 e70af85d, PyAutoArray#710: `aa.Setup`, `Setup.auto`, `setup_rules.yaml`, `Imaging/Interferometer.apply_setup`, the inversion-factory mismatch check, `Setup.apply_threads`). Heart lib-tests install Array from source main, so no release is needed for CI. R6 = opt-in first (approved 2026-11-16).
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-24

## Context

- Phase 5 order: 5A Nerves (done) → 5B Array (done) → **5C Galaxy+Lens (this prompt)** → 5D Fit (`number_of_cores="auto"`, banner hook, search metadata) → 5E estimator (the banner's second, "Estimate:" line) → 5F–5H workspace/assistant/science.
- Design: report §3.5, PyAutoGalaxy/PyAutoLens row (`draft/research/autolens_profiling/likelihood_lifecycle_epic_report.md`):
  - `Analysis*(dataset, setup="auto")`; `use_jax=` is kept as an explicit override that maps onto a Setup.
  - Weak and point analyses are aligned with the rest.
  - A multi-dataset sum resolves one setup.
  - SLaM helpers accept a setup once.
  - `setup.json` is written beside the search output.
  - The banner reads `Setup: jax/gpu/dense/fp64 (A100-SXM4-80GB) · rule imaging-pixelized-gpu · optimal (Pulse day zero …)`. The "Estimate:" line is 5E's.
- Boundary (report §3.4): auto decides the backend, device, operator, precision, transformer/route and threads. It never decides the model (mesh, over-sampling, regularisation), the sampler or the HPC request. An explicit override always wins.
- 5B design call 3: Array knows dataset classes only. 5C maps the lens-scale likelihood keys (group, multi_galaxy, cluster, point source, and `imaging/<mesh>` vs `imaging/mge` from the model) to `Setup.auto(dataset_type, variant)`.
- 5B-2 lesson: the PyAutoLens numpy-path analyses wrap every exception as `af.exc.FitException`, which the search treats as a rejected sample, and the PyAutoGalaxy visualizers catch `InversionException`. So the setup must be applied and checked when the analysis is constructed, or a mismatch shows up as silently rejected samples.
- Threads: `Setup.apply_threads()` at fit start (5B-2) is safe inside multiprocessing workers. `number_of_cores="auto"` belongs to 5D.
- Existing code:
  - PyAutoGalaxy: `autogalaxy/analysis/analysis/{analysis,dataset}.py` (`use_jax`).
  - PyAutoLens: `autolens/analysis/analysis/{dataset,lens}.py`, `autolens/{imaging,interferometer,point,weak}/model/analysis.py`, `autolens/analysis/model_util.py` and `autolens/analysis/result.py`. These hold the SLaM-facing helpers; the SLaM pipelines themselves are workspace scripts and move in 5F.
- The planning question to settle: do the SLaM helpers live in the library (thread a `setup` through `model_util` / result chaining), or is "accept a setup once" only a workspace change for 5F?

## Out of scope

- `number_of_cores="auto"` and search metadata (5D).
- The runtime estimate and the banner's second line (5E).
- Workspace and HowTo prose, and the SLaM workspace scripts (5F).
- Assistant skills (5G).
- Science projects (5H).
- Flipping the default to `setup="auto"`, which happens in the release after this one (R6).
- Mixed precision is never chosen by auto (R4).
- No compute.
