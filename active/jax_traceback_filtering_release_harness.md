# Release/smoke script harness filters JAX tracebacks away, hiding the real exception

Type: bug
Target: ci
Repos:
- @PyAutoHeart
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Filed: 2026-08-27
Issued: 2026-08-27

## Symptom

When a workspace script fails under JAX inside PyAutoHeart's script harness
(`.github/workflows/workspace-validation.yml`, job `run_scripts`, both the
`smoke` and `release` legs), JAX's default traceback filter removes its own
internal frames *and*, in practice, the exception that matters:

```
scripts/interferometer/start_here.py ...  FAIL (19.5s)
For simplicity, JAX has removed its internal frames from the traceback of the
following exception. Set JAX_TRACEBACK_FILTERING=off to include these.
```

That is the whole failure record. The reader is told which script failed and
nothing about why.

## Why it matters — the cost is measured, not hypothetical

PyAutoHeart run 30516167217 (2026-07-30) failed both interferometer shards
(`autogalaxy` and `autolens`) with exactly the message above. Because the real
exception was filtered away, that night read as an unidentified failure. The
same defect surfaced its true cause only the following night, run
30607596240 (2026-07-31), where the message survived intact:

```
jax.errors.JaxRuntimeError: RESOURCE_EXHAUSTED: Out of memory allocating 85898814480 bytes.
```

One night was spent identifying a failure the harness already had the
information to name. The underlying OOM was root-caused and fixed the same day
(`autolens_workspace#450`; record:
`complete/2026/08/interferometer-start-here-integrate-oom.md`) — this task is
about the *harness*, which still filters, and will do the same to the next
JAX failure.

A gate whose error messages are filtered away is the same category of problem
as the exit-code contract fixed in PyAutoBrain#196: the signal exists, the
harness discards it before a human sees it.

## Current state (verified 2026-08-27)

`JAX_TRACEBACK_FILTERING` appears nowhere in PyAutoHeart:

```
$ grep -rn "JAX_TRACEBACK_FILTERING" .        # PyAutoHeart @ d576003 — no matches
```

Nor in the workspaces' `config/build/profile_release.yaml` /
`profile_smoke.yaml` defaults, both of which already pin every JAX-adjacent var
they care about (`JAX_ENABLE_X64`, `PYAUTO_DISABLE_JAX`, …) explicitly.

## Proposed fix

Set `JAX_TRACEBACK_FILTERING: "off"` once, in the workflow-level `env:` block of
`PyAutoHeart/.github/workflows/workspace-validation.yml` — the block that
already carries `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK`. One place covers both
the `smoke` and `release` legs and every workspace in the matrix, and
`run_python.py`'s per-script env profiles inherit it (a profile only *sets* the
keys it is given; it never clears inherited vars).

Consider whether the same belongs in the other script-running workflows
(`smoke-tests.yml`, `workspace-smoke.yml`) for the same reason.

## Exit criteria

- A JAX exception raised inside a workspace script under `run_scripts` reports
  its own exception type and message in the job log, not the
  "JAX has removed its internal frames" placeholder.
- Verified against a real (or deliberately induced) JAX failure in a CI run,
  not only by reading the diff.

## Origin

Split out of `draft/bug/autolens/interferometer_release_leg_oom.md` (its
2026-08-04 amendment, consequence 2) when that prompt was retired as superseded
— the OOM it described had already shipped, this harness gap had not.
