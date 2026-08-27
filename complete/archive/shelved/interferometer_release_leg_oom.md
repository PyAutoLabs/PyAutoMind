> **RETIRED 2026-08-27 — superseded, not actioned as written.**
>
> The OOM this prompt describes was root-caused and fixed before the prompt's own
> amendment was written. See `complete/2026/08/interferometer-start-here-integrate-oom.md`:
> `MultiStartProdigy` ran 48 starts as a single unbatched `vmap` (~86 GB in one
> allocation); `autolens_workspace#450` set `batch_size=4` and the leg was
> discharged by Release Integrate run 30901054267 on 2026-08-04
> (`scripts/interferometer/start_here.py ... PASS (173.5s)`).
>
> Re-verified at retirement (2026-08-27):
> - `autolens_workspace` and `autogalaxy_workspace` **both** carry `batch_size=4`
>   on the 48-start `MultiStartProdigy` in `scripts/interferometer/start_here.py`,
>   so the amendment's consequence 1 ("it is not autolens-specific") is closed too.
> - The interferometer shard is green in the two most recent nightly Release
>   Integrate runs — 32804373015 (2026-08-25, `autogalaxy`) and 33073386315
>   (2026-08-27, `autolens`). No recurrence.
> - The NUFFT/transformer hypothesis in "Notes for triage" was wrong: the
>   allocation was the multi-start batch, not a dense transformer matrix.
>
> The amendment's consequence 2 — `JAX_TRACEBACK_FILTERING=off` in the release
> harness — was **not** done and is still open. It was split out as its own task:
> `draft/bug/ci/jax_traceback_filtering_release_harness.md`.

---

# interferometer/start_here.py OOM in nightly release-validation integrate leg

Filed: 2026-07-31 (backfilled from git)

Filed 2026-07-31 from the phase-4 ship gate of point-source-chi-squared-variants
(#657): Heart RED traced to the nightly Release Integrate run.

## Symptom

Nightly `Release Integrate` run
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/30607596240
(v2026.7.31.1.dev69201, profile=release) fails in job
`integrate / run_scripts (3.12, autolens, interferometer)` — the **release-mode
leg only** (TestPyPI wheels, release profile, no source on PYTHONPATH; the
smoke-mode leg of the same job was skipped/green):

```
scripts/interferometer/start_here.py ...   FAIL (58.8s)
jax.errors.JaxRuntimeError: RESOURCE_EXHAUSTED: Out of memory allocating 85898814480 bytes.
```

~86 GB in a single JAX allocation on a CI runner. All other integrate script
jobs passed (imaging 49m green, cluster, multi_galaxy, weak, autogalaxy, autofit).

## It also hit the night before, in BOTH workspaces (added 2026-08-04)

Reviewing the eight-night blocked streak
(`draft/triage/nightly_release_blocked_eight_nights.md`) surfaced an earlier
occurrence that the 07-31 filing above missed, because its error message was
truncated. PyAutoHeart run 30516167217 (2026-07-30) failed **two** interferometer
shards:

```
integrate / run_scripts (3.12, autogalaxy, interferometer)   FAIL
integrate / run_scripts (3.12, autolens,    interferometer)  FAIL
  scripts/interferometer/start_here.py ...  FAIL (19.5s / 28.2s)
  For simplicity, JAX has removed its internal frames from the traceback of the
  following exception. Set JAX_TRACEBACK_FILTERING=off to include these.
```

The JAX traceback filter ate the real exception, which is why 07-30 read as a
different (unnamed) failure — the 07-31 run is the same bug with the message
intact.

Two consequences for triage:

1. **It is not autolens-specific.** The identically-named
   `scripts/interferometer/start_here.py` in *both* autolens_workspace and
   autogalaxy_workspace blew up in the same run, so the cause is at or below the
   shared layer, not in lens-specific code. This raises the prior on the
   NUFFT/transformer hypothesis already in "Notes for triage" and lowers it on
   anything in PyAutoLens. Repos should probably read @PyAutoArray first.
2. **Set `JAX_TRACEBACK_FILTERING=off` in the release harness**, or this class of
   failure will keep costing a night to identify. A gate whose error messages are
   filtered away is the same category of problem as the exit-code contract fixed
   in PyAutoBrain#196.

Not observed on 08-01, 08-03 or 08-04, so it is intermittent rather than
permanent — measure the rate before concluding a fix worked.

## Notes for triage

- Release profile runs full-resolution (no PYAUTO_SMALL_DATASETS) with JAX
  enabled — an ~86 GB buffer smells like a dense NUFFT/transformer matrix or a
  vmap batch materializing at full uv-resolution rather than a leak.
- Check whether this is a regression from a recent PyAutoArray/PyAutoLens main
  change (nightly wheels) vs a long-standing release-leg gap that only now runs
  this script.
- The same job's earlier `verify_install_release` step logged
  `TestPyPI install failed after 30 attempts` before succeeding on retry —
  probably unrelated flake, but confirm the wheel set installed was current.

## Exit criteria

Release-mode interferometer leg green in the nightly Release Integrate run;
root cause recorded (config/profile fix vs library fix).
