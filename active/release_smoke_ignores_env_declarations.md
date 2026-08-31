# release.yml's smoke loop ignores `__Env__` declarations — witt_wynne.py fails every LIVE run

Type: bug
Target: ci
Repos:
- @PyAutoHands
- @autolens_workspace
Themes:
- ci-smoke
- release
Difficulty: small
Autonomy: supervised
Consequence: judge
Review-minutes: 20
Unattended: ready
Priority: high
Filed: 2026-08-29
Issued: 2026-08-31

Surfaced by the 2026-08-29 live release (PyAutoHands run 33259478535): the
release published cleanly — all 5 packages at `2026.8.29.1` on PyPI, tags,
notebooks, release notes, Colab bumps and announce all green — but the run
concluded **failure** because `run_smoke_tests (3.12, autolens_workspace)`
failed on one script:

```
FAIL: guides/misc/witt_wynne.py  (line 913)
AssertionError: The caustic-matched projection did not reproduce the PointSolver
verdict on every case. ... PYAUTO_SMALL_DATASETS short-circuits
PointSolver.solve to a fixed pair of positions...
verdict agreement: caustic 2/5, vector-sum 2/5
```

## Root cause (verified, deterministic — not a flake)

- `witt_wynne.py` carries a valid `ENV: full_datasets` declaration —
  PyAutoHands' own `read_env_declaration` (`autohands/env_config.py`) parses it
  to `['full_datasets']` against the live file.
- But the `run_smoke_tests` job in `PyAutoHands/.github/workflows/release.yml`
  (~lines 300–380) is a plain bash loop (`python "scripts/$script"` over
  `smoke_tests.txt`) with job-level `PYAUTO_SMALL_DATASETS: "1"`. It never
  routes through the `env_config.py` resolver, so in-file `__Env__`
  declarations are silently ignored in this job.
- Under SMALL_DATASETS every PointSolver case returns the fixed 2-image pair,
  so the script's verdict assertion fails every time. A re-run fails
  identically, and **every future LIVE release run stays red** on this job
  until fixed — while validating nothing.

## Fix options (pick one)

1. **PyAutoHands `release.yml`** — make the release smoke loop honor `__Env__`
   declarations: route through the env_config-aware runner, or unset
   `PYAUTO_SMALL_DATASETS` per script when its declaration asks for
   `full_datasets`. (The Heart-side workspace-validation harness already
   resolves per-script env; this loop predates that.)
2. **`autolens_workspace/smoke_tests.txt`** — drop `guides/misc/witt_wynne.py`
   from the release smoke list as incompatible with this harness as-is (loses
   its coverage; option 1 is the real repair).

## Fallback

If the env-aware routing turns out to be a larger refactor of release.yml than
a small task carries, ship option 2 with a comment pointing back here, and
re-file option 1 as its own maintenance task.
