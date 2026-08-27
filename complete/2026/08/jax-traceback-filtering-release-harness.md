# Release/smoke script harness stopped filtering JAX tracebacks

Issue: PyAutoLabs/PyAutoHeart#186 (CLOSED 2026-08-27)

## What was wrong

JAX removes its own frames from a traceback by default and, in practice, takes
the exception that names the failure with them. A workspace script failing under
JAX inside Heart's script harness reported only:

```
scripts/interferometer/start_here.py ...  FAIL (19.5s)
For simplicity, JAX has removed its internal frames from the traceback of the
following exception. Set JAX_TRACEBACK_FILTERING=off to include these.
```

Which script failed, and nothing about why.

The cost was measured, not hypothetical. Heart run 30516167217 (2026-07-30)
failed **both** interferometer shards (`autogalaxy` and `autolens`) with exactly
that placeholder, so that night read as an unidentified failure. The real cause —
`jax.errors.JaxRuntimeError: RESOURCE_EXHAUSTED: Out of memory allocating
85898814480 bytes` — became legible only in run 30607596240 the following night,
where the message happened to survive. One night was spent identifying a failure
the harness already had the information to name.

## What shipped

| Repo | PR | Merged | Change |
|---|---|---|---|
| PyAutoHeart | [#187](https://github.com/PyAutoLabs/PyAutoHeart/pull/187) | 2026-08-27 (`c8b093e1`) | `JAX_TRACEBACK_FILTERING: "off"` — workflow-level `env:` in `workspace-validation.yml`, and the workspace-runner step's `env:` in `smoke-tests.yml`. 2 files, +18/−0 |

Workflow-level `env:` reaches every job and step of `workspace-validation.yml`,
so both `mode=smoke` and `mode=release`, and every project in the matrix, inherit
it. `run_python.py`'s per-script env profiles inherit it too — a profile only
*sets* the keys it is given and never clears inherited vars, which is the
behaviour `profile_release.yaml`'s own header already relies on.
`workspace-smoke.yml` needed no edit: it is a thin caller of
`workspace-validation.yml`.

CI before merge: Heart Tests run 33093776599, `pytest (3.12)` + `pytest (3.13)`
both success, `mergeable_state: clean`. Locally `python3 -m pytest -q -n auto` →
641 passed.

## The exit criterion is deferred, not met

The issue asked that a real JAX exception print its own type and message in a job
log, "verified against a real (or deliberately induced) JAX failure in a CI run,
not only by reading the diff". Nothing has failed under JAX since the merge, so
that has not been observed. The next JAX failure in `run_scripts` or the smoke
runner is the proof. This is recorded as shipped-but-unproven on purpose: the
whole defect is that the diff looks obviously right and the log is what has to
change.

## Traps worth keeping

- **`off` must be quoted in YAML.** Bare `off` is a YAML 1.1 boolean, so
  `JAX_TRACEBACK_FILTERING: off` hands GitHub Actions `false`, not the string JAX
  expects. Checked with `yaml.safe_load` rather than assumed.
- **A stale prompt can outlive its own fix by a month.** This task exists only
  because `/start_dev` on
  `draft/bug/autolens/interferometer_release_leg_oom.md` found the prompt's
  headline OOM already shipped —
  `complete/2026/08/interferometer-start-here-integrate-oom.md`, 2026-07-31,
  `MultiStartProdigy` running 48 starts as one unbatched `vmap`. That prompt sat
  in `draft/` as pickable backlog for 27 days, and its triage notes pointed at
  the wrong subsystem (NUFFT/transformer). It was retired to
  `complete/archive/shelved/` in the same run. **Check `complete/` for the slug
  before planning a bug prompt**, not after.
- **A prompt's own amendment can be the only live part of it.** The retired
  prompt's 2026-08-04 amendment carried two consequences. One ("it is not
  autolens-specific") was already closed — both workspaces carry `batch_size=4`.
  The other was this task. Reading only the headline would have lost it.

## Original prompt

`active/jax_traceback_filtering_release_harness.md`, filed and issued
2026-08-27 by the same `/start_dev` run that retired its parent.

## Not done

12 workspace scripts still call `MultiStartProdigy` with no `batch_size`
(autolens: `group/`, `point_source/`, `multi_dataset/`, `cluster/`, `weak/`, …;
autogalaxy: `multi_galaxy/modeling.py`, `multi_dataset/start_here.py`,
`cluster/modeling.py`). Cheaper datasets than a 108k-visibility interferometer
fit, so likely fine — surfaced during this run, deliberately not filed.

## Original prompt

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
