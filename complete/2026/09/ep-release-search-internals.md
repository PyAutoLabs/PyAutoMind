## ep-release-search-internals
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1631
- completed: 2026-09-17
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1634 (merge fa2d540ac)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1634
- summary: |
    slope_hierarchy_scale job 342410 (25 AnalysisFactors, JAX likelihood, Nautilus number_of_cores=1,
    64 GB) died after ~3 EP steps / 76 factor searches with `LLVM ERROR: Unable to allocate section
    memory!`. The prompt's hypothesis was compile churn; the cause is a retention chain: EPHistory keeps
    every factor step's Status -> Status.result -> Result._search_internal (the nautilus/dynesty sampler)
    -> its likelihood callable, a Fitness -> the Fitness's per-instance `_vmap`/`_jit`/`_grad`
    cached_property caches holding every compiled XLA executable of that search. Nothing in
    `autofit/graphical` reads the sampler after `optimise` (latest_result consumers use .projected_model /
    .samples / .model). Fix: `Result.release_search_internal()` (new, `autofit/non_linear/result.py`) sets
    `_search_internal = None` and walks `child_results` because `AnalysisFactorCollection.make_result`
    hands the same sampler object to a CombinedResult and every child; `AbstractSearch.optimise` calls it
    (getattr-guarded, the regression suite's StaticSearch returns a bare object) before
    `status.result = result`. The `search_internal` property keeps its on-disk-dill fallback; plain
    `search.fit()` is untouched. Regression test `test_autofit/graphical/test_ep_release_search_internal.py`
    fails on main and passes with the fix. Full `test_autofit` serially 2858 passed / 2 skipped; CI legs
    unittest 3.12 / 3.13 / nojax + docs-build all green.
- witness: |
    5 AnalysisFactors, `af.ex.Analysis(use_jax=True)`, `af.Nautilus(n_live=50, n_batch=10,
    number_of_cores=1)` per factor, LaplaceOptimiser on the prior factors, 4 EP steps, JAX_PLATFORMS=cpu,
    ~3.5 min per run. Live Fitness (gc.get_objects) per step main vs fix: 5/0, 10/0, 11/0, 12/0; RSS MB
    529/463, 608/463, 617/463, 633/464. The prompt's own witness (25 factors x 12 steps inside a fixed
    memory budget on RAL) is a cluster run the human owns; the 5x4 laptop-scale witness is what shipped.
- notes: |
    Traps: (1) a weakref on `Fitness.__init__` is not a valid probe: a dynesty search that resumes from its
    checkpoint restores the sampler by unpickling, so the retained Fitness never passes `__init__` and every
    recorded weakref reads dead while the leak is live; count live Fitness objects via gc.get_objects as a
    delta against a pre-measured baseline instead. (2) `test_autofit/graphical` and `non_linear/search` are
    flaky under `pytest -n auto` on main (autouse `do_remove_output` wipes the shared `test_autofit/output`
    across xdist workers; 14-18 failures vary run to run, all FileNotFoundError search.summary); serial
    runs are clean; existing draft `ep_test_suite_is_not_xdist_safe.md` covers it. (3) autofit writes
    `./output` relative to cwd, and a completed output tree makes the next run resume instead of refit;
    run witnesses from a fresh scratch dir. Behaviour change to carry into the release note: after an EP
    factor step `status.result.search_internal` is served from disk, or None when `output.search_internal`
    is off; downstream EP callers (PyAutoGalaxy/PyAutoLens) not checked. Surface: Claude Code remote
    session, no worktree, PyAutoFit attached via add_repo and cloned shallow; branch
    `claude/vmapped-likelihood-jit-compiles-bhog4o` rather than `feature/ep-release-search-internals`;
    Heart not installed so the full serial suite was the readiness gate, freeze flag unreadable. Fable
    planned, Opus executed. Follow-ups filed: draft/refactor/autofit/ep_analysis_level_compile_cache.md
    (analysis-level compiled-callable cache across EP steps, one compile per factor per run),
    draft/bug/autofit/vmap_jit_recompiles_per_nautilus_batch_length.md (pad/bucket the leading batch dim),
    draft/bug/autofit/nautilus_ep_default_optimiser_reads_use_jax_unguarded.md (af.Nautilus as EP
    default_optimiser crashes on PriorFactors: `nautilus/search.py` reads `analysis._use_jax` unguarded).
    Shadow row: Consequence is `judge`, not `notify`; none appended.

## Original prompt

# EP re-jit-compiles the vmapped likelihood per factor search until LLVM section memory…

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
- jax
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-09-15
Consequence: judge
Witness: an EP run over 25 AnalysisFactors with a JAX likelihood completes 12 factor_steps (300 factor searches) inside a fixed memory budget; RSS / XLA compile-cache size is flat across steps, not growing by one compiled executable per factor search.
Review-minutes: 20
Unattended: ready

Gates:
- https://github.com/PyAutoLabs/slope_hierarchy_scale/issues/3
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1631

## Report (slope_hierarchy_scale job 342410, RAL `ral` partition, 2026-09-09/10)

The N=25 EP arm ran on the JAX-on-CPU path with no pool (the PyAutoFit#1608 ruling):
each of the 25 AnalysisFactors is fitted by its own `af.Nautilus(number_of_cores=1)` under
`LaplaceOptimiser`, max_steps 12, SBATCH `--mem=64gb`, 10 kernel threads.

- 76 factor searches completed in ~11 h (22:25 → 09:16), i.e. ~3 EP steps of 25 factors.
- Every factor search logged "JAX jit compiling vectorized (vmap) likelihood function" — 76
  compiles, one per search (`grep -c 'jit compiling vectorized' output.342410_0.out` = 76).
  Each factor step builds a fresh Fitness / jitted function for the same 25 analyses, so
  nothing is reused across steps.
- At 09:15:58 the `.err` fills with `E … execution_engine.cc:54] LLVM compilation error:
  Cannot allocate memory` and `contiguous_section_memory_manager.cc:71] releaseMappedMemory
  failed`; factor dataset_24 then raises `jax.errors.JaxRuntimeError: INTERNAL: Failed to
  materialize symbols: { (<xla_jit_dylib_22>, { subtract_select_fusion }) }` and the EP
  optimiser skips it ("Factor dataset_24 raised on 1 consecutive step(s)"); the next factor
  search hits `LLVM ERROR: Unable to allocate section memory!` and the process aborts
  (core dumped) at 09:29:41.
- Logs: `slope_hierarchy_scale/hpc/batch_cpu/output/output.342410_0.out`,
  `hpc/batch_cpu/error/error.342410_0.err` (pulled to the local clone).

Hypothesis to test first: XLA's CPU JIT keeps every compiled executable's section memory
alive for the life of the process (the jitted callable is dropped but the dylib is not, or
the `jax_compile.py` wrapper caches on a key that includes the fresh Fitness object), so the
footprint grows by one executable per factor search. Candidates: reuse the compiled
likelihood across EP steps for the same analysis (cache on the analysis + model structure,
not the Fitness instance), or `jax.clear_caches()` / explicit executable release between
factor searches, with a test that asserts the compile count stays at one per factor over
several steps.

Not the same defect as PyAutoFit#1608 (pool hang) — that path is fixed; this is the memory
ceiling of the path we now take.

<!-- formalised by the Intake (Conception) Agent on 2026-09-15 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/32df3fc7-e0cc-4fc7-98c7-0f160dca158c/scratchpad/intake_ep_compile_memory.md -->
