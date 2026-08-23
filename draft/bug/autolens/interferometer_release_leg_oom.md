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
