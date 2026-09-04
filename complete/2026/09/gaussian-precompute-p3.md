- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/528 (closed, completed)
- completed: 2026-09-04
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/530 (MERGED 7bbffe800)
- epic: gaussian-deflections-precompute — **epic COMPLETE, all 3 phases shipped 2026-09-03/04**
  (p1 complete/2026/09/gaussian-precompute-p1.md, p2 complete/2026/09/gaussian-precompute-p2.md,
  p3 here). Ledger retired to complete/archive/epics/precompute_fixed_geometry_gaussian_deflections.md
  and the epics.md entry dropped. PyAutoArray#520 / PyAutoGalaxy#602 / #605 remain **pending-release**;
  that obligation is carried by the phase 1 and phase 2 records, not re-declared here (this phase is a
  docs-only workspace change).
- shipped: **no mechanism** — phase 3 is a verification sweep plus one paragraph of prose. The paragraph
  goes in the `__MASS LIGHT DARK PIPELINE__` docstring of
  `scripts/imaging/features/advanced/mass_stellar_dark/slam.py` (and its regenerated notebook, markdown
  cell 12): the light-tied mass profiles' deflections depend only on the **fixed light geometry**, so on
  the numpy path they are memoised across likelihood evaluations — for an MGE lens light (a `Basis` of
  Gaussians) each fixed Gaussian's field is computed once and rescaled by the free
  `mass_to_light_ratio`, and on JAX the field is folded out of the traced graph as a constant.
  `AUTOGALAXY_DEFLECTIONS_MEMO=0` is the kill switch, named in the prose so a user who suspects the memo
  can turn it off.
- measured: on the merged library `main`s (PyAutoGalaxy `65af1122`, PyAutoArray `e36a5af4`),
  `OMP_NUM_THREADS=1`, all output to scratch —
  **`test_autolens` 610 passed, 1 xfailed**.
  SLaM `mass_stellar_dark/slam.py` in test mode (smoke defaults, `PYAUTO_TEST_MODE=2`,
  `PYAUTO_SMALL_DATASETS=1`), 3 repeats per leg: **every stage's max-log-likelihood bit-identical**
  memo on vs `AUTOGALAXY_DEFLECTIONS_MEMO=0`; `mass_light_dark[1]` median **0.370 s on vs 0.515 s off
  (0.72x)**, every stage at or below memo-off; `memo_stats` **119 hits / 20 misses / 0 evictions /
  119 kB / 20 entries**; the kill-switch leg reports all zeros.
  Numba likelihood pins held: `pixelization_numba` hst **27661.910206968903** vs pin
  27661.910133665442 (rel **2.65e-9**, inside 1e-6); `pixelization_numba_mge_mass`
  **−56107.564075886374 bit-identical**, memo **2.61x per call** at production hst resolution — that
  cell, not the test-mode ratios, is the production-scale number for this shape.
- honest-negative: the store-churn worry was **wrong**. `mass_light_dark[1]` has a linear-Sersic light
  with a free `mass_to_light_ratio`, i.e. an **L1** profile whose memo key changes on every call, so the
  memo was expected to pay eviction/insert cost for nothing. It still ran **0.72x** wall with the memo on
  and evicted **nothing** (0 evictions, 119 kB store). No library change proposed; recorded as measured.
- controls: kill switch = `AUTOGALAXY_DEFLECTIONS_MEMO=0`, run as the second leg of every comparison
  (all `memo_stats` counters zero, likelihoods unchanged). `autolens_workspace_test` regressions on the
  same mains: `imaging/jax_likelihood/mge.py` PASS (vmap −86283.10390232 vs pin −86283.10392994,
  **3.2e-10**; `jit(fit_from)` matches numpy to 1e-15), `imaging/jax_grad/mge.py` PASS (FD max rel
  2.6e-6), `imaging/visualization/modeling_visualization_jit.py` PASS (35 min, all asserts). **No pin
  edited anywhere** — this phase reports pins, it does not move them.
- honest-negative: `interferometer/visualization/modeling_visualization_jit.py` Part 1 passes and its
  live-Nautilus Part 2 is **OOM-killed locally at 10.7 GB RSS**. That is its existing `no_run.yaml`
  SLOW/OOM entry, pre-existing and unrelated to the memo — named here so the gap in the sweep is on the
  record rather than implied green.
- finding/trap: `no_run.yaml` lists `mass_stellar_dark/slam` as needing JAX/CSE, yet the script runs
  clean on the **numpy test-mode path** — the exclusion is broader than the reason behind it. Not fixed
  here (it would be a `no_run.yaml` edit outside this phase's scope); worth a prompt if the entry ever
  blocks a sweep again.
- finding: the `multi_galaxy` and `group` SLaM variants share only the pipeline **header**, not the
  `__MASS LIGHT DARK PIPELINE__` docstring block, so the paragraph could not be mirrored into them and
  they were deliberately left untouched. A future "document the memo everywhere" pass has to write prose,
  not copy a block.
- session: local CLI; PR opened 2026-09-03 under a human-acknowledged Heart RED (PR-open only), merged
  and closed out via /prm 2026-09-04. All 7 CI legs across the 3 `pull_request` runs green,
  `mergeStateStatus` CLEAN; the Heart freeze window does not apply to a workspace repo.
- affected-repos:
  - autolens_workspace

## Original prompt

# Gaussian precompute phase 3: downstream sweep — SLaM, test_autolens, workspace regressions, doc line

Type: feature
Epic: gaussian-deflections-precompute
Phase: 3
Target: autolens
Repos:
- @PyAutoLens
- @autolens_workspace
- @autolens_workspace_test
Themes:
- numba-cpu
- mass-profiles
- profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Status: active
Filed: 2026-09-03
Issued: 2026-09-03
Parent: draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md

> Phase 3 of the `gaussian-deflections-precompute` epic — ledger
> `draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md`. Successor work to the
> completed `numpy-deflections-cpu` epic (`complete/archive/epics/numpy_deflections_cpu_speedup.md`).
> Phases 1 and 2 are hard predecessors — this phase adds no library mechanism, it **verifies** the memo
> on the driver it was built for and documents it where a user meets it.

## Goal

The memo exists for the SLaM `mass_light_dark` shape: a fixed MGE lens light chained into the mass with one
free `mass_to_light_ratio`. Prove nothing downstream moved, and tell the user the switch exists.

## Steps

1. **`test_autolens`** green in full (numpy; and under JAX where the suite runs it).
2. **SLaM smoke** on `autolens_workspace/scripts/imaging/features/advanced/mass_stellar_dark/slam.py` —
   the driver the memo is for. Run it in test mode per the workspace's smoke contract and confirm it
   completes with the memo on and with `AUTOGALAXY_DEFLECTIONS_MEMO=0`.
3. **`autolens_workspace_test` regression scripts** for fixed-MGE lens models: run and compare, report any
   drift rather than re-pinning.
4. **Numba likelihood pins** unchanged (hst rect 27661.910133665442 and siblings).
5. **Doc line** in the SLaM `mass_light_dark` script explaining that fixed-geometry deflections are memoised
   across likelihood evaluations and rescaled by the free ratio, and naming the
   `AUTOGALAXY_DEFLECTIONS_MEMO=0` kill switch.
6. **No PyAutoLens library edit is assumed.** This is a verification phase; if a PyAutoLens change turns out
   to be needed, file it then — do not scope it now.

## Verification

- `test_autolens` green; `ruff check` + `ruff format --check` clean on anything touched.
- SLaM smoke completes both with the memo on and with the kill switch set; runtimes for both recorded.
- `autolens_workspace_test` regression scripts pass with pins unchanged; any shift reported as a finding.
- Numba likelihood pins unchanged at rtol 1e-6.
- The doc line renders correctly in the generated notebook for the SLaM script.

## Ship

Workspace-only expected: `autolens_workspace` PR (doc line) and, if any regression script needed a fix,
an `autolens_workspace_test` PR. Behind the library-first gate — phases 1 and 2 must be merged first.

## Out of scope

Any library mechanism change (phases 1 and 2); re-pinning likelihood or deflection values; new SLaM
features; PyAutoLens source edits not proven necessary by this phase's own runs.
