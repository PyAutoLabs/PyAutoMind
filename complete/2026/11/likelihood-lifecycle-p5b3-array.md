## likelihood-lifecycle-p5b3-array
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/711
- completed: 2026-11-24
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/712
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/712
- epic: likelihood-lifecycle (phase 5B-3; next 5C-3 Galaxy/Lens call sites + aggregator reapply + shared helper, then 5D)

Phase 5B-3 shipped as PyAutoArray#712 (merged 2026-11-24 as faa80349): a lazy, size-gated sparse operator on the real dataset, so calculations outside modeling can get the optimal operator once 5C-3 adds the call sites.

- **API:** `Imaging.sparse_operator_for(xp, needs_operator, settings)` / `Interferometer.sparse_operator_for(...)` return the attached operator; otherwise, with the policy on, they build once and cache privately on the dataset; otherwise None.
- **Builds:** they reuse `apply_sparse_operator_cpu()` / `apply_sparse_operator()`, with exact / 1e-14 equality. Above 1e6 visibilities the interferometer uses `apply_sparse_operator_from_chunks` (2**18 per chunk, matching to 1e-12). One log line gives the build time.
- **Policy:** an explicit `Settings(lazy_sparse_operator=...)` wins; otherwise `general.yaml` `inversion: lazy_sparse_operator: "auto"` (quoted, because YAML reads a bare `off` as False) or `PYAUTO_SETUP=auto` turns it on. An unset or empty `PYAUTO_SETUP` stays off. Default off (R6). An extra config key, `inversion: lazy_sparse_operator_visibility_budget`, overrides the 1e6 budget.
- **Gates (never build):**
  - `xp` isn't numpy, or a JAX tracer is detected (jax is checked only if already imported);
  - inside a multiprocessing worker (`numba_util.parallel_kernel_allowed()`), where it returns an inherited cache but never builds;
  - an explicit setup whose operator isn't sparse;
  - `needs_operator=False`;
  - real ≠ imaginary noise, which gives a one-time warning and never pools.
- **Cache:** carried by `apply_over_sampling`; cleared by every rebuilding `apply_*`, by `apply_setup`'s copy shortcut and by `trimmed_after_convolution_from`.
- **Design (human-approved after a read-only survey):** the hook is on the real dataset, not the inversion factory, because every fit wraps its data in a fresh `aa.DatasetInterface` with no back-reference. The fit call sites moved to 5C-3, and the 5B-3/5C-3 drafts were amended to match.
- **Gate:** 2614 tests (20 new); Heart dev GREEN; smoke 7/7 against the branch; PR CI GREEN, including the no-JAX leg.
- **Traps:**
  - A Mind push in this phase was rejected by a concurrent push, and the temp worktree was removed by an `&&` chain before the retry. The dangling commit was recovered with `git fsck --lost-found` and cherry-picked. Remove temp Mind worktrees only after a successful push.
  - The commit message's "Closes #711" auto-closed the issue on merge.

## Original prompt

# Likelihood lifecycle phase 5B-3: PyAutoArray lazy, size-gated sparse operator on the dataset (`dataset.sparse_operator_for`), so non-modeling calculations get the optimal setup

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
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/711
Consequence: judge
Witness: `Imaging.sparse_operator_for(xp, needs_operator)` and `Interferometer.sparse_operator_for(xp, needs_operator)` return the attached operator when there is one. Otherwise, with the policy on (`general.yaml` `inversion: lazy_sparse_operator: auto`, exposed as a `Settings` property, or `PYAUTO_SETUP=auto`), they build the designated operator once and cache it privately on the real dataset: imaging gets the numba operator, interferometer gets w-tilde via the NUFFT builder, switching to the chunked builder above a visibility budget (default 1e6). The build logs one line with its time. Nothing is built when `xp` isn't numpy, a JAX tracer is detected, the call is inside a multiprocessing worker, the dataset has an explicit dense setup, `needs_operator` is False, or (interferometer) the real and imaginary noise differ; that last case gives a one-time warning and the noise map is never pooled. `apply_over_sampling` carries the cache; `apply_mask` / `apply_noise_scaling` drop it. With the policy off (the default this release, R6), behaviour is unchanged. Full test suite green.
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
- **The choke point (superseded 2026-11-24 by survey):** every inversion goes through `galaxy/to_inversion.py` / `lens/to_inversion.py` → `aa.Inversion` → `inversion_imaging_from` / `inversion_interferometer_from` (`autoarray/inversion/inversion/factory.py`). The factory knows the dataset type, the mapper's mesh (the variant) and `xp`, so it can resolve the rule key itself.
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

- **Design calls (human-approved 2026-11-24, after the survey):**
  1. The hook is on the real dataset, not the factory. Every fit wraps its data in a fresh `aa.DatasetInterface` (autogalaxy `imaging/fit_imaging.py:143`, autolens `lens/to_inversion.py:209`, …) with no `setup` and no back-reference, so a factory-side cache would be lost after every fit. The fit call sites move to 5C-3.
  2. The interferometer size gate is on n_vis: the unchunked NUFFT spreader buffer is about 3 GB at 1e6 visibilities and 15 GB at 5e6, while the stored operator is extent-sized. Above the budget use `apply_sparse_operator_from_chunks`; don't refuse.
  3. Never change the data silently: real ≠ imaginary noise → skip with a one-time warning; never pool.
  4. Workers never build (`numba_util.parallel_kernel_allowed()`); they inherit the parent's cache, because PyAutoFit evaluates one likelihood before forking.

## Out of scope

- The Galaxy/Lens fit call sites and aggregator reapplication of `setup.json` (5C-3).
- The JAX path, which stays modeling-applied or explicit.
- Flipping the policy on by default, which goes with the R6 default flip.
- Workspace script cleanup (5F).
