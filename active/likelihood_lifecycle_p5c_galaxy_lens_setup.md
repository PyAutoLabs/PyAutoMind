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
