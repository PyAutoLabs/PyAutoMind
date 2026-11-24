## likelihood-lifecycle-p5b-array
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/708
- completed: 2026-11-24
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/709
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/710
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/709
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/710
- epic: likelihood-lifecycle (phase 5B; next 5C PyAutoGalaxy + PyAutoLens)

Phase 5B of the likelihood-lifecycle epic shipped in PyAutoArray as two PRs under one issue.

- **5B-1, choosing a setup** (#709, merged 2026-11-24 as e70af85d):
  - `aa.Setup`, with `from_setup_id` / `.setup_id`.
  - `Setup.auto(dataset_type, variant, regime, environment)`.
  - `autoarray/config/setup_rules.yaml`: 39 rows from Pulse 94a101f4, written by the `python -m autoarray.setup.generate_rules --pulse … [--check]` generator.
  - Hardware with no designation uses the nearest class, with `extrapolated=True`.
- **5B-2, applying a setup** (#710):
  - `Imaging.apply_setup`: sparse → `apply_sparse_operator` (jax) / `apply_sparse_operator_cpu` (numba); dense → no operator. With a `.setup`, `apply_mask` / `apply_noise_scaling` re-apply it, so the operator is rebuilt for the new mask or noise-map. `apply_over_sampling` carries it.
  - `Interferometer.apply_setup`: `_nufft` → `TransformerNUFFT`; `_wtilde` → `apply_sparse_operator`. One finufft-built operator serves both backends, and `xp` picks the route. A constructor `setup` skips the >10,000-visibility DFT guard.
  - Both `apply_setup` methods are idempotent.
  - The inversion factory raises `InversionException` on an operator/backend mismatch. One case is new even without a setup: a numba imaging operator under JAX `xp`.
  - `Setup.apply_threads()`: numba plus threadpoolctl. It never raises, and it leaves numba alone inside multiprocessing workers.
- **Gate:**
  - 5B-1: 85 + 2562 tests; smoke 7/7.
  - 5B-2: 2594 tests; Heart dev GREEN; smoke 7/7 against the branch.
  - #710's first CI run failed `unittest-nojax`: five new tests built the JAX operator without `pytest.importorskip("jax")`. Fixed in 3aebdb19.
- **Traps:**
  - Local venvs always have JAX, so a new test that builds `ImagingSparseOperator` needs an importorskip or it only fails on the no-JAX CI leg.
  - Heart smoke grades the worktree only when `activate.sh` exports `PYAUTO_ROOT`. It did here.
- **For 5C:**
  - A factory mismatch raised inside a search is caught as a rejected sample (`FitException`) or a skipped plot, so 5C should check, or `apply_setup`, once when the analysis is constructed.
  - The lens-scale keys (group, multi_galaxy, cluster, point source) are resolved by the caller.
  - R6: `setup="auto"` is opt-in first, with a "would choose" banner.

## Original prompt

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
Status: active
Issued: 2026-11-23
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/708
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
