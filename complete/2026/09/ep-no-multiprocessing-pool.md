## ep-no-multiprocessing-pool
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1608
- completed: 2026-09-11
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1610
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1610
- summary: |
    Human ruling 2026-09-09: expectation propagation never runs a factor search
    through a Python multiprocessing pool. RAL job 342351_0 (slope_hierarchy_scale
    EP arm, submitted --use_cpu so use_jax=False) hung 27 h on 10 cores with 16 s of
    CPU: two forked likelihood workers segfaulted in _ctypes, Pool._maintain_pool
    replaced them, and because multiprocessing never re-issues a dead worker's
    in-flight task the Pool.map inside nautilus add_samples never returned.
    Shipped in one PyAutoFit PR (#1610, merged 2026-09-11):
    - `AbstractSearch.optimise` (the EP factor-optimiser entry, so every search
      type) refuses `number_of_cores > 1` with a SearchException naming the search,
      the value, and the two fixes (`number_of_cores=1`; `Analysis(use_jax=True)`).
      A refusal, not a silent downgrade: the same search instance is re-entered
      per factor. One log line per factor step says where parallelism comes from.
      `ParallelEPOptimiser` (EP's own opt-in pool across factors) unchanged apart
      from a docstring warning.
    - `_LikelihoodWorkerPool.map` (nautilus/search.py) dispatches via map_async
      and polls (`LIKELIHOOD_POOL_POLL_INTERVAL`, 1 s), checking the exit code of
      every worker Process captured at construction; a replaced worker raises a
      diagnosable SearchException (PID + signal) within seconds instead of hanging
      every multi-core Nautilus fit. Holding the Process objects, not PIDs, keeps
      the exit code readable after the pool prunes the dead worker (~0.1 s).
    - Tests: EP refusal with every fork_context name monkeypatched to fail; EP
      single-core unchanged; SIGKILLed pool worker raises < 5 s with -9 in the
      message (18/18 repeats); healthy 40-task map in order. graphical 281 passed
      serial (279 + 2), rest of suite 2342 passed / 2 skipped serial.
- traps: |
    - `test_autofit/graphical` must be judged SERIALLY: under -n auto 17 tests
      fail on clean main (shared test_autofit/output/<id>/ directory, one worker's
      teardown deletes another's PNG) — filed as
      draft/bug/autofit/ep_test_suite_is_not_xdist_safe.md. The rest of the suite
      also breaks under -n auto (collection-id mismatch from memory addresses in
      test_prior_properties) — already filed by a sibling session as
      draft/bug/autofit/xdist_collection_ids_unstable_in_test_prior.md.
    - `StaticSearch` in test_autofit/graphical/regression/test_static.py subclasses
      NonLinearSearch without calling super().__init__, so the guard reads
      `getattr(self, "number_of_cores", 1)`.
    - Dynesty's single-core path still enters a Pool(1) of its own (the #1442
      shape, never fixed for dynesty) — filed as
      draft/bug/autofit/dynesty_single_core_path_still_builds_a.md.
    - The Mind's `scripts/ledger_merge.py classify --base` reads stdin when it is
      not a TTY and blocks forever in a harness; pass paths explicitly or `</dev/null`.
    - First ledger push failed auto-merge on a dashboard.md/html conflict with a
      sibling session's merge landing the same minute; merge main in, regenerate,
      re-push.
- follow-ups: |
    - Phase 2 (science side): draft/bug/graphical_ep/ep_use_cpu_flag_disables_jax.md —
      slope_hierarchy_scale scripts/ep.py derives use_jax = not use_cpu, so the CPU
      partition silently disables JAX; gated on #1608, now unblocked.
    - draft/bug/autofit/ep_test_suite_is_not_xdist_safe.md (parallel-safe EP tests).
    - draft/bug/autofit/dynesty_single_core_path_still_builds_a.md.
    - Deprecating ParallelEPOptimiser is a separate human decision (not filed).
- session: web-github (session clone, no task worktree; issue, PR and merge driven
    through the GitHub MCP surface; implementation delegated to an Opus subagent).

## Original prompt

# EP must never drive Nautilus through a Python multiprocessing pool

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: an EP fit requesting number_of_cores>1 either runs serially or refuses loudly (never silently forks a pool), demonstrated by the slope_hierarchy_scale EP arm getting past its first factor_step; plus a regression test that kills a pool worker mid-map and asserts the search raises a diagnosable error within seconds instead of blocking forever.
Review-minutes: 25
Unattended: ready
Issued: 2026-09-11
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1608

EP must never drive Nautilus through a Python multiprocessing pool

Witness: an EP fit requesting number_of_cores>1 either runs serially or refuses loudly (never silently forks a pool), demonstrated by the slope_hierarchy_scale EP arm getting past its first factor_step; plus a regression test that kills a pool worker mid-map and asserts the search raises a diagnosable error within seconds instead of blocking forever.

Ruling (human, 2026-09-09): expectation propagation should not be combined with Python multiprocessing at all. EP's per-factor Nautilus searches should run with pool=None / number_of_cores=1, and parallelism should come from a vectorised JAX likelihood, which bypasses Pool.map entirely.

Evidence that forced this. RAL job 342351_0 (slope_hierarchy_scale EP arm) hung for 27 hours consuming 16 seconds of CPU across a 10-core allocation, and was cancelled having produced zero samples. py-spy showed the parent blocked in multiprocessing/pool.py:367 map -> :768 get -> :765 wait, reached via _LikelihoodWorkerPool.map (autofit/non_linear/search/nest/nautilus/search.py:61) <- nautilus/sampler.py:869 evaluate_likelihood <- nautilus/sampler.py:1119 add_samples <- the EP optimiser's factor_step <- ep.py:91. Two of the ten forked workers (PIDs 924667/924668) had segfaulted inside _ctypes.cpython-312 within seconds of the fork ('segfault at 116cd5b08 ... error 4 in _ctypes.cpython-312-x86_64-linux-gnu.so'). Pool._maintain_pool forked replacements and restored the count to ten, but multiprocessing never re-issues a dead worker's in-flight task, so the map() could never return. Nothing reached stderr, because a signal death bypasses Python's exception machinery: every log looked healthy.

Root cause of the path being taken at all: the run was submitted --use_cpu, and scripts/ep.py:58 reads 'use_jax = not use_cpu'. That flag conflates 'run on the CPU partition' with 'disable JAX', so choosing CPU silently disabled the vectorised likelihood and dropped the fit onto the multiprocessing path. JAX-on-CPU, which needs no pool, is unreachable through that flag.

Scope, separable into phased PRs:
1. Primary: EP never constructs a process pool. Force pool=None on the EP factor-optimiser path, or refuse number_of_cores>1 with a clear error rather than forking silently. Note the cost to weigh: with a non-JAX likelihood this makes each factor's search single-core, so the serial guard only pays off alongside the JAX path.
2. Confirm EP drives a vectorised JAX likelihood end to end (the machinery exists: use_jax is threaded through make_factor_graph), so parallelism comes from vectorisation rather than processes.
3. Residual, wider than EP: the dead-worker deadlock affects every multi-core Nautilus fit, not just EP, including per-lens fits and any user running number_of_cores>1. A vanished worker should fail loudly within seconds instead of hanging to the wall clock. Worker count is not a usable health check, because _repopulate_pool refills it; a replacement is distinguishable only by a _maintain_pool frame in its stack. PyAutoFit#1548 is present in the running mirror and does not cover this: it made neural-bound training serial and swapped in likelihood_worker, leaving ordinary likelihood evaluation unguarded. Prior art: PyAutoFit#1439, #1443, #1548.

Raw py-spy dumps for all eleven processes and the dmesg segfault lines were captured while the job was still live.

<!-- formalised by the Intake (Conception) Agent on 2026-09-09 from user-intake -->
