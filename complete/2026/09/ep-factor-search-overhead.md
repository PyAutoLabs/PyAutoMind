## ep-factor-search-overhead

- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1642
- completed: 2026-09-24
- epic: graphical-ep
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1643
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1644
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1645
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1643
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1644
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1645
- assets: `complete/2026/09/ep-factor-search-overhead-assets/` (the filing-time cProfile report + pstats dumps)

## Shipped

All three PRs were merged into PyAutoFit `main` on 2026-09-24 by the human's `/prm`. CI was green on every leg of each head and no Heart freeze was active. Each merge was made under the human's Heart RED override (see below). At close-out, every feature head was proven to be an ancestor of `origin/main` (0 commits ahead).

- **PR 1, [PyAutoFit#1643](https://github.com/PyAutoLabs/PyAutoFit/pull/1643)** (merge `71c096d46`, branch `feature/ep-factor-search-overhead`):
  - **Dynesty single pass** (`0e2c09748`). A converged Dynesty search now finishes in one `run_nested` pass. `AbstractDynesty.run_search_internal` treats "dynesty stopped itself inside its call budget" as converged, so there is no intermediate `perform_update(during_analysis=True)`, no checkpoint restore and no second, empty `run_nested`.
  - **EP maths** (`16789050a`). `TruncatedNormalMessage.log_partition` / `kl` / `_normal_gradient_hessian_from` call `scipy.special.ndtr` directly (bit-identical). `Fitness.manage_quick_update` returns early when quick updates are disabled. `ITERATIONS_NEVER` moved to `autofit.non_linear.fitness` and is re-exported from its old location.
  - Result: `run_nested` calls 30 → **15**; per-search wall −18 % (1.93 → 1.57 s); moments bit-for-bit identical. Tests: 2881 passed / 2 skipped.
- **PR 2, [PyAutoFit#1644](https://github.com/PyAutoLabs/PyAutoFit/pull/1644)** (merge `aff2f3686`, branch `feature/ep-factor-search-overhead-p2`):
  - EP factor searches skip per-search visuals by default. New config key `general.yaml → output.visualize_ep_factor_searches: false`, read with `.get(..., False)`.
  - New switches `NonLinearSearch._visualize_fit` / `_visualize_before_fit`, which `optimise` resets in a `finally`. New `SearchUpdater(visualization_enabled=...)`.
  - The EP optimiser's own graph/history outputs are unchanged.
  - Result: per-search wall 26–37 % lower in load-matched pairs; moments bit-identical to PR 1. Tests: 2885 passed / 2 skipped.
- **PR 3, [PyAutoFit#1645](https://github.com/PyAutoLabs/PyAutoFit/pull/1645)** (merge `dd9fbe0aa`, branch `feature/ep-factor-search-overhead-p3`):
  - Frozen-model fast path for `instance_from_vector`: `AbstractPriorModel._vector_priors()` and `Model._instance_plan()` are `@frozen_cache`d, and replay goes through `_instance_for_arguments_frozen`. The unfrozen path is unchanged.
  - Result: mapper **5.8x** (single Gaussian, 21.27 → 3.68 µs/call) and **4.6x** (3-Gaussian collection, 58.83 → 12.81 µs/call) per call. The EP wall gain on the toy is within noise (about 7 % of search time). Tests: 2895 passed / 2 skipped. Workspace smoke on the stacked PR 2 + PR 3 head: 8/8 scripts + 2/2 notebooks.
- **Net on the toy:** per-factor search 2.45 s → **~0.9–1.0 s** (witness target ≤ 1.5 s).

## Witness

The witness passed:
- `run_nested` is called once per Dynesty factor search (15 calls for 15 searches).
- Per-search wall is ≤ 1.5 s.
- Parent moments are identical.
- The full serial `test_autofit` is green at each PR.

**Correction to the witness.** As filed, the witness compared moments "within 1e-6 of a control run with the same seeds". That comparison is only meaningful on a fully seeded harness. The InitializerPrior draws from stdlib `random`, so `random.seed` has to be set alongside numpy/dynesty. With that seeding, the moments were bit-identical (max abs diff 0.0, ep_history flags identical) across baseline → PR 1 → PR 2 → PR 3, well inside the 1e-6 bar.

## Heart RED override

Heart was RED throughout for reasons unrelated to this work: readiness score 45, ts 2026-09-24T15:11:12Z.
- The red reasons were release validation FAILED (stage integrate); workspace validation 4 failed (autolens cluster/weak notebooks and scripts); and manifest drift (hub organism blurb).
- A live human authorized a development-only override for PR 1 on 2026-09-24 ("Yes, override and open PR 1"). The same human extended it to the stacked PR 2 and PR 3 ("Yes, same override for PR 2 and PR 3").
- The override is recorded on each PR, on the issue, on the active.md row and in autonomy_log.
- It covered commit/push/pending-release PRs only. It did not cover a release, and Heart remains RED for release purposes.

## Follow-up

- `draft/bug/autofit/nautilus_converged_run_double_pass.md`: the same converged-run double pass, suspected in Nautilus. It stays a draft.

## Traps

- **activate.sh symlink.** The task worktree's `activate.sh` symlink was rewritten by other sessions mid-task and pointed `PYTHONPATH` at another library worktree. Assert `autofit.__file__` before every timing or harness run.
- **Seeding.** Seeding numpy and dynesty is not enough for a reproducible EP harness. `InitializerPrior` uses stdlib `random`, so seed it too, or moment comparisons are noise.
- **Assets under active/.** `lifecycle check` rejects non-md files under `active/`, so a prompt's assets directory cannot follow it there. It stayed at `draft/refactor/autofit/…_assets/` while the task was active and moved beside this record at close-out.
- **Stacked PRs.** Retarget each PR to `main` after its base merges (#1644 after #1643, #1645 after #1644).

## Original prompt

# EP: cut the per-factor-search wrapper overhead (redundant second run_nested pass, per-search plots, instance_from_vector fast path)

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: on the ep_toy_gaussian N=5, max_steps=3 toy, `run_nested` is called once per Dynesty factor search (15 calls for 15 searches, not 30) and per-search wall drops from ~2.45 s to <= 1.5 s at identical parent moments (mean and sigma within 1e-6 of a control run with the same seeds), with the full `test_autofit` suite green run serially.
Review-minutes: 5
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-24
Issued: 2026-09-24
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1642

## Why

Every EP factor update is a full autofit non-linear search. On the
`ep_toy_gaussian` #1405 collapse toy (PyAutoCortex
`projects/ep_toy_gaussian.md`) a 1-parameter Dynesty factor search spends
about as much time in the autofit wrapper as in the sampler. A 1000-search
N=50 repeat carries ~15-20 min of pure overhead; best case on the toy is ~2x.

Profile (2026-09-24, laptop, PyAutoFit at the RAL mirror a73684012, N=5,
max_steps=3, 15 factor searches, cProfile total 109 s; files in
`complete/2026/09/ep-factor-search-overhead-assets/`):

- **Per search 2.45 s = ~1.47 s dynesty `run_nested` + ~0.98 s autofit wrapper**
  (plots, a redundant second `run_nested` pass, samples writes).
- **Redundant second `run_nested` pass (~5.5 s / 13 %).** 30 `run_nested`
  calls for 15 searches. `run_search_internal`
  (`autofit/non_linear/search/nest/dynesty/search/abstract.py:413-455`)
  returns `finished = total_iterations == iterations_after_run`, which is
  never true on a first pass that converges, so every search does a full
  `perform_update(during_analysis=True)` + checkpoint restore + a no-op second
  `run_nested`.
- **Per-search visuals.** `corner_anesthetic` + `model_fit.png` 7.7 s / 18 %;
  `data.png` redrawn every search 2.3 s / 5 % although the data never changes.
- **`instance_from_vector`** (`autofit/mapper/prior_model/abstract.py:990`)
  is 57 % of `fitness.call`, i.e. ~25-30 % of `run_nested` for a 1-parameter
  model: `autofit/mapper/model.py:30` `cache` 486k calls,
  `autofit/mapper/prior_model/attribute_pair.py` wrapper 481k calls,
  `prior_model.py:483 _instance_for_arguments` 2.7 s tottime.
- **`truncated_normal.log_partition` / `kl`** call `scipy.stats.norm.cdf`
  18.6k times / 3.45 s — use `scipy.special.ndtr` / `log_ndtr`.
- **`manage_quick_update`** 1.8 s while quick-update is disabled (61k calls).
- **`gc.collect` per search** 75 ms (1.78 s over 15).

## What (phases)

1. **Dynesty finished-detection fix** so a converged first pass is recognised
   and the second `perform_update` + checkpoint restore + `run_nested` is
   skipped; unit test that counts `run_nested` calls (mock the sampler) and
   asserts one per converged search.
2. **EP factor searches skip per-search visuals** — a config switch, default
   off under EP (corner/model_fit per search), and `data.png` drawn once per
   analysis rather than per search.
3. **Mapper fast path for fixed-structure models** in `instance_from_vector`
   (precompute the prior-to-attribute map once per model; bypass the
   `cache` / `attribute_pair` wrappers on the hot path).
4. **`ndtr` swap** in `autofit/messages/truncated_normal.py` (and
   `mapper/prior/_erf_helpers.py` if it pays) — `scipy.special.ndtr` /
   `log_ndtr` in place of `scipy.stats.norm.cdf`. Also look at the disabled
   `manage_quick_update` early-out and the per-search `gc.collect`.

Each phase should be measured on the same toy (per-search wall, `run_nested`
call count, parent moments against a same-seed control).

## Side observation (reproducibility)

Three runs of `ep_repeat.py --repeat 0` gave parent means 51.86 / 51.33 /
51.61: the repeat seed does not make EP reproducible at a73684012. Known cause
— the Laplace refine draws from global `np.random` and depends on variable-id
ordering (PyAutoFit#1352). The witness's "same seeds" control therefore needs
the global RNG seeded (or the #1352 fix) before the 1e-6 moment comparison is
meaningful; if it cannot be made deterministic, compare moments across
matched repeats within their spread and say so.

## Links

- Campaign ledger: `draft/research/graphical_ep/ep_campaign.md` (row 1b; phase 6 epic 2, EP profiling)
- Sibling: `draft/refactor/autofit/ep_analysis_level_compile_cache.md` (the JAX recompile per factor search)
- EMFILE fix that preceded this profile: PyAutoFit#1632 (dynesty single-core no pool), #1634 (release factor search internals)
- Evidence: `complete/2026/09/ep-factor-search-overhead-assets/ep_profile_report.txt`, `ep_pstats_cumulative.txt`, `ep_pstats_tottime.txt` (paths shortened: `SP/` = site-packages, `PyAutoFit/`, `STDLIB/`, `SCRATCH/` = the profiling scratch dir)
