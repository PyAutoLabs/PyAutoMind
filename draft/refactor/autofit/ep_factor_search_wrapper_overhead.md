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

## Why

Every EP factor update is a full autofit non-linear search. On the
`ep_toy_gaussian` #1405 collapse toy (PyAutoCortex
`projects/ep_toy_gaussian.md`) a 1-parameter Dynesty factor search spends
about as much time in the autofit wrapper as in the sampler. A 1000-search
N=50 repeat carries ~15-20 min of pure overhead; best case on the toy is ~2x.

Profile (2026-09-24, laptop, PyAutoFit at the RAL mirror a73684012, N=5,
max_steps=3, 15 factor searches, cProfile total 109 s; files in
`ep_factor_search_wrapper_overhead_assets/`):

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
- Evidence: `ep_factor_search_wrapper_overhead_assets/ep_profile_report.txt`, `ep_pstats_cumulative.txt`, `ep_pstats_tottime.txt` (paths shortened: `SP/` = site-packages, `PyAutoFit/`, `STDLIB/`, `SCRATCH/` = the profiling scratch dir)
