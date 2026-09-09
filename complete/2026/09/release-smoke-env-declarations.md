## release-smoke-env-declarations
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/272
- hands-pr: PyAutoHands#274 (merged 2026-09-01; commit b7df526f110884dd2d56d23ed6da6938be396d08, authored 2026-08-31)
- completed: 2026-09-01
- retired-from-draft: 2026-09-09 — this prompt was filed 2026-08-29 and **never issued**. The
  fix shipped from another session straight onto PyAutoHands, so the prompt sat in
  `draft/bug/ci/` rendering as pickable backlog for nine days. Retired on evidence by the
  `ci-smoke` bundle session, which read it as a bundle member and found the work already done.
  This record is the retirement, not a re-ship: nothing was implemented for it here.
- what shipped: fix option 1 of the two the prompt offered — the real repair, not the fallback.
  `run_smoke_tests` in `PyAutoHands/.github/workflows/release.yml` no longer runs a bare
  `python scripts/<script>` bash loop under blanket job-level `PYAUTO_*`. It checks PyAutoHands
  out beside the workspace and runs `autohands/run_python.py "<workspace>" scripts
  --list smoke_tests.txt --env-config config/build/profile_release.yaml --report-dir test-results`,
  the same per-script resolution the PR smoke gates and Heart's workspace-validation already use.
  `guides/misc/witt_wynne.py`'s `ENV: full_datasets` declaration is therefore honoured and
  `PYAUTO_SMALL_DATASETS` released for it.
- job-level `PYAUTO_*` dropped: env_config's managed-prefix scrub (`MANAGED_ENV_PREFIXES =
  ("PYAUTO_",)`) made it unreachable on this path anyway; the release profile owns that family
  now. Only infrastructure vars (`NUMBA_CACHE_DIR`, `MPLCONFIGDIR`, `JAX_ENABLE_X64`) stay in
  the job env, for the install steps and the runner process itself.
- guards added by the shipping PR: `tests/test_release_smoke_env.py` pins the new job shape, so
  a regression to a bare loop fails PyAutoHands' own suite. The step also hard-fails when
  `smoke_tests.txt` exists but `config/build/profile_release.yaml` does not — a smoke run with
  no env policy is now an error rather than a silent blanket-env run. `--report-dir` is
  load-bearing and commented as such: without a report the runner cannot propagate failures and
  always exits 0.
- fallback NOT taken, and that is the right outcome: option 2 was to drop
  `guides/misc/witt_wynne.py` from `autolens_workspace/smoke_tests.txt`, which the prompt itself
  called a loss of coverage. The script is still in the list and still asserts 5/5 verdict
  agreement, so the trap it was built to spring — see
  `complete/2026/08/witt-wynne-projection.md`, "smoke trap" — still guards the runner.
- consequence: the 2026-08-29 LIVE release (run 33259478535) published all 5 packages at
  `2026.8.29.1` cleanly and still concluded failure on this one job. That class of red is closed.
- no follow-up owed. The prompt's own fallback clause ("re-file option 1 as its own maintenance
  task") does not apply — option 1 is what shipped.

## Original prompt

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
