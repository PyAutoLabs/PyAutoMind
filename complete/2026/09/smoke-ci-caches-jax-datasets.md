# CI caches in the smoke workflow — compile and datasets survive between runs, and every timing row says hot or cold

PyAutoHeart#211 → `bfcd302`, closing PyAutoHeart#210, merged 2026-09-06 on
branch `claude/ci-test-timing-epic-ke2lul`. Phase 7 of the
`ci-timing-fast-tests` epic (`draft/feature/pyautoheart/ci_timing_fast_tests_epic.md`),
pulled ahead of the phase-5/6 rebuild waves per the ledger's Fable review.
Fable-planned on the issue, implemented by an Opus subagent under the Brain's
delegation ladder from a web session (no task worktree).

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/210
- completed: 2026-09-06
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/211

## What shipped

- **`smoke-tests.yml`** (the reusable workflow every workspace / `_test` /
  HowTo gate calls `@main`): the JAX persistent compilation cache is restored
  and saved per runner OS × Python leg × jaxlib version × a manual epoch salt
  (`PYAUTO_CACHE_EPOCH`, job-level env; bump to invalidate everything), run-id
  suffixed so each save is a fresh superset; `JAX_COMPILATION_CACHE_DIR` set
  to an explicit workspace path in the runner env (the runner copies the job
  env into every script subprocess). The workspace's simulated `dataset/`
  tree is restored/saved keyed on the hash of every simulator script × the
  dependency-chain HEAD SHAs × the salt, with **no broader fallback**; not
  keyed on the Python leg. JAX saves even on a red run; datasets only on a
  green one; neither re-uploads an unchanged cache.
- **Cache state as data.** A `Record cache state` step (`if: always()`)
  writes `test-results/cache_state.json` (restored key, hit/miss, sizes and
  entry counts before/after) into the report dir the smoke-timings upload
  already globs. `smoke_timings` ingests it: legs, rollup items, the board's
  per-repo lines (`[jax cache hit|miss]`) and `timings/scripts` record lines
  carry `cache`; `classify_drift` never compares two known but different jax
  cache states. Artifacts from before the sidecar read `unknown` and compare
  as before.
- **Blast radius held**: 243 insertions and 0 deletions in the workflow;
  every new step `continue-on-error`; the runner command byte-identical (its
  env gained one variable); the upload step untouched. A wiring test pins
  the step order, the non-fatality, the key components, the single dataset
  restore-key and the `if:` conditions.
- Tests 864 → 893; fake names; tenant firewall OK.

## Key traps / findings

- **`should_simulate` makes dataset restoring safe by construction.** It
  keeps a restored dataset only while its `SMALLDAT` regime matches the one
  in force and re-simulates otherwise — so a stale or wrong-regime cache
  entry costs a re-simulation, never a wrong result. What it cannot detect
  is a dataset that a *different library commit* would have written
  differently, hence the chain SHAs in the key and no broader fallback:
  correctness over hit rate.
- **A killed simulator leaves a truncated FITS that `should_simulate` would
  keep** — the reason the dataset cache saves only on a green run while the
  compile cache saves always (an entry is complete or absent).
- **A cache landing looks like a 4× speedup and its invalidation like a 4×
  regression** unless the timing row says which it was. The sidecar is the
  unit of measurement; the drift rule "never across two known but different
  cache states" is what keeps the board from crying wolf on exactly the runs
  where the cache is doing its job.
- **`hashFiles()` is an expression, not a command** — it resolves in `env:`
  and the script reads it back as a variable, the same way caller inputs
  reach `run:` bodies in this workflow.
- **The measurement is a follow-up, not a deliverable of the PR.** No live
  run had happened at close-out; hot-vs-cold comes from the record once each
  repo has had two runs.

## Follow-ups (tracked, not started here)

- **Measure hot vs cold** (item 3 of the phase prompt): after two runs per
  `_test` repo, compare `jax_likelihood` per-script seconds and gate p50 in
  `timings/scripts/` and `timings/gates.jsonl` (rows carry `cache.jax`), and
  the restore/save overhead on autocti_workspace_test (3 entries); write the
  numbers into the epic ledger. Phase 5 should read them first.
- Phase 5 of the epic: `draft/test/autogalaxy_workspace_test/physical_fast_rebuild.md`
  — its PR appends the next epoch boundary (`fast-tests`) when it lands.

## Original prompt

# CI caches in the reusable smoke workflow: JAX compile cache + dataset builds

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoNerves
Difficulty: large
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 7
Issued: 2026-09-06

CI caches in the reusable smoke workflow: persist the JAX compile cache and dataset builds across runs.

`autonerves/jax_wrapper.py:98-125` already auto-writes a persistent JAX compilation cache
to `~/.cache/pyauto_jax` (JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS=1), and the closed
jax-compile-time arc certified the cache at both scales (51x local, 5.9x A100 end-to-end).
But `PyAutoHeart/.github/workflows/smoke-tests.yml` — the one reusable workflow every
workspace/_test/HowTo smoke gate calls — has NO actions/cache step: the cache helps within
one job (scripts are subprocesses) and is discarded between runs.

1) Add an `actions/cache` step for `~/.cache/pyauto_jax`, keyed on jaxlib version + python
matrix leg (+ a manual epoch salt for invalidation). Expected: removes the 12-18s+ compile
from every `ENV: jax` script on cache-hit runs — plausibly 30-50% off the jax_likelihood
wall total. Traced-code changes miss the cache naturally, which is correct. (Run
33078033016 already refuted any interaction between the cache and the Eigen-pool hang.)

2) Same mechanism for simulated dataset builds: `should_simulate` auto-simulation persists
datasets locally but CI runners start clean, so each job re-simulates each dataset family
(~10-20s incl. import per family). Cache the dataset build trees keyed on a hash of the
simulator scripts so any simulator edit invalidates.

3) Measure honestly: compare cache-hit vs cache-miss gate wall-clock on the phase-1/2
timing surface, and confirm cache restore/save overhead doesn't eat the win for the small
repos (autocti: 3 entries).
