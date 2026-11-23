# Likelihood lifecycle phase 5B: PyAutoArray `aa.Setup`, `Setup.auto`, rule table from the Pulse designations, `dataset.apply_setup`, operator/backend consistency check

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Themes:
- hpc-gpu
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: PyAutoArray main carries `aa.Setup` (the report §3.1 setup tuple plus `rule_id`, `regime`, `hardware_class`, `decision_id`, `extrapolated`) with `Setup.from_setup_id()` round-tripping every setup_id in the rule table; `autoarray/config/setup_rules.yaml` generated from PyAutoPulse `decisions.yaml` (39 designations) with a provenance header, and a parity test that regenerates it from a Pulse checkout when one is available (skipped otherwise); `aa.Setup.auto(dataset_type, variant, environment=None)` returns the designated optimal setup for every (likelihood, hardware class) row, unit-tested with a monkeypatched `Environment`; `PYAUTO_SETUP=<setup_id>` and an explicit `aa.Setup(...)` always win; `Imaging.apply_setup` / `Interferometer.apply_setup` attach the matching operator/transformer, are idempotent and survive `apply_mask` / `apply_over_sampling` / `apply_noise_scaling`; the inversion factory raises a clear error on an operator/backend mismatch instead of silently taking another path; full test suite green
Review-minutes: 30
Unattended: no
Lane: any
Gate: 5A MERGED 2026-11-23 (PyAutoNerves#223; `autonerves.environment.Environment.detect()` and `parse_setup_intent()` on Nerves main; Heart lib-tests install Nerves from source main, so no release is needed for Array CI). Boundary table (report §3.4) and R6 = opt-in first approved 2026-11-16.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-23

## Context

- Phase 5 order: 5A Nerves (done) → **5B Array (this prompt)** → 5C Galaxy+Lens (`setup="auto"` on analyses, `setup.json`, banner, SLaM threading) → 5D Fit (`number_of_cores="auto"`) → 5E estimator → 5F–5H workspace/assistant/science. One issue in PyAutoArray.
- Design: report §3.5, PyAutoArray row (`draft/research/autolens_profiling/likelihood_lifecycle_epic_report.md`): `aa.Setup` dataclass; `Setup.auto(...)` with rule table `config/setup_rules.yaml` generated from the Pulse designation decisions; regimes computed from the dataset; `dataset.apply_setup(setup)` idempotent and carried by `apply_over_sampling` / `apply_mask` / `apply_noise_scaling`; inversion factory raises when operator and backend disagree; threads at runtime via `numba.set_num_threads` (+ threadpoolctl if available).
- Boundary (report §3.4): auto decides backend, device, operator, precision, transformer/route, threads; never the model (mesh, over-sampling, regularisation), the sampler or the HPC request; an explicit override always wins.
- Rule source: `@PyAutoPulse/decisions.yaml`, 39 `kind: designation` rows, keyed (likelihood = `<dataset_type>/<variant>`, regime = `standard`, hardware_class ∈ {cpu_many_core, gpu_a100}) → `optimal: <setup_id>`, `secondary: [...]`, `rule` (one sentence in dataset terms). Examples: imaging/{rectangular,delaunay,delaunay_nn} cpu → `numba_cpu_sparse_fp64`, gpu → `jax_gpu_dense_fp64`; imaging/mge cpu → `jax_cpu_dense_fp64`; interferometer pixelized cpu → `numba_cpu_sparse_fp64_wtilde`, gpu → `jax_gpu_sparse_fp64_wtilde`; interferometer/mge → `jax_{cpu,gpu}_dense_fp64_nufft`; point-source/cluster → `jax_{cpu,gpu}_na_fp64`.
- Array knows dataset classes, not lens-scale concepts: group / multi_galaxy / cluster / point-source likelihood keys are resolved by the caller (5C passes `dataset_type`/`variant`); 5B ships the full table and the lookup, and the Array-level helpers for imaging and interferometer.
- Existing code: `@PyAutoArray/autoarray/dataset/imaging/dataset.py` (`apply_sparse_operator`, `apply_sparse_operator_cpu`, `apply_mask`, `apply_over_sampling`, `apply_noise_scaling`), `@PyAutoArray/autoarray/dataset/interferometer/dataset.py` (the >10,000-visibility DFT guard, `apply_sparse_operator`), `@PyAutoArray/autoarray/inversion/inversion/factory.py` (operator dispatch), `@PyAutoArray/autoarray/settings.py` (`interferometer_route`).

## Out of scope

`setup="auto"` on analyses, `setup.json`, banner, SLaM threading (5C); `number_of_cores="auto"` (5D); the estimator (5E); workspace prose (5F). Mixed precision is never chosen by auto (R4). No compute.
