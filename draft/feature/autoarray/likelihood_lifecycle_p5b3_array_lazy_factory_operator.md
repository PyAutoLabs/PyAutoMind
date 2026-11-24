# Likelihood lifecycle phase 5B-3: PyAutoArray lazy, size-gated operator in the inversion factory, so non-modeling calculations get the optimal setup

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
Witness: With the policy on (per dataset via `dataset.setup = "auto"`, or globally via `PYAUTO_SETUP=auto` or a config key), a numpy-path pixelized inversion on a dataset with no sparse operator builds the designated operator once inside the inversion factory and caches it on the dataset. That is the numba sparse operator for imaging and the w-tilde operator for interferometer. The build logs one line naming the operator and its build time; repeated fits reuse the cache; and the cache is carried through `apply_mask` / `apply_noise_scaling` the way `.setup` is. Nothing is ever built under JAX tracing. An interferometer build above the size budget (n_vis × n_pix, from the Pulse regimes) refuses with a clear message instead of a silent multi-minute, multi-GB precompute. An explicit operator or an explicit dense setup always wins. With the policy off (the default this release, R6), behaviour is unchanged. Full test suite green; `pyauto-heart smoke --affected-by PyAutoArray` passes.
Review-minutes: 30
Unattended: no
Lane: any
Gate: 5C-2 MERGED (PyAutoLens setup wiring), so modeling's eager `modify_before_fit` apply is in place and this layer only complements it. Phasing approved by the human 2026-11-24.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-24

## Context

- **Why:** 5C resolves the setup in `modify_before_fit`, so only modeling gets the optimal operator. These do not:
  - direct fits: `al.FitImaging(dataset, tracer)` and similar, in 117 workspace scripts, of which 37 attach `apply_sparse_operator` by hand;
  - aggregator reloads (5C-3);
  - `analysis.fit_from(...)` before a search.

  On CPU a pixelized fit without an operator takes the dense mapping-matrix route: slow, with memory that grows as n_image × n_source.
- **The choke point:** every inversion goes through `galaxy/to_inversion.py` / `lens/to_inversion.py` → `aa.Inversion` → `inversion_imaging_from` / `inversion_interferometer_from` (`autoarray/inversion/inversion/factory.py`). The factory knows the dataset type, the mapper's mesh (the variant) and `xp`, so it can resolve the rule key itself.
- **The numpy path barely depends on the variant:** every pixelized imaging CPU row is numba sparse, and inversions with only light profiles (MGE) take the mapping route regardless of any operator.
- **Risks to design against:**
  1. The interferometer w-tilde precompute takes minutes and GBs at ALMA/JVLA scale, hence the size gate and a loud refusal.
  2. Multiprocessing: a lazy build in Nautilus workers is one operator per worker. Modeling must keep applying eagerly before the fork (5C does), and the lazy path must not be what modeling relies on.
  3. Cache lifetime across `apply_*` copies.
  4. The sparse and mapping routes differ by about 1e-4 relative, so hard-coded likelihoods may shift when the default flips.
  5. How far it reaches: every numpy pixelized test switches route when the policy is on, hence default off.
- **Existing code:**
  - `autoarray/inversion/inversion/factory.py` (the operator/backend consistency check from 5B-2);
  - `autoarray/dataset/imaging/dataset.py` and `autoarray/dataset/interferometer/dataset.py` (`apply_setup`, `apply_sparse_operator*`);
  - `autoarray/setup/setup.py` (`Setup.auto`, `setup_rules.yaml`);
  - the interferometer route cost model in `factory.py` (`_use_interferometer_numba`).

## Out of scope

- Aggregator reapplication of `setup.json` (5C-3).
- The JAX path, which stays modeling-applied or explicit.
- Flipping the policy on by default, which goes with the R6 default flip.
- Workspace script cleanup (5F).
