## Outcome

Corrective fix for Heart RED "autocti_workspace: Smoke Tests failure on main"
(live human corrective-PR authorization on PyAutoHeart#330), merged as
PyAutoHeart#331 (6e4be55, 2026-11-11).

- Cause: GitHub runners moved ubuntu-24.04 → 26.04 (libgsl.so.27 → .so.28).
  smoke-tests.yml's pip cache (no image identity in its key) restored an
  arcticpy-2.6 wheel built on 24.04, so `import arcticpy` failed.
- Fix: `install_arcticpy.sh` installs arcticpy with `--no-cache-dir`, so it is
  always built against the GSL present. One shared recipe covers smoke,
  lib-tests, docs-build and heart/smoke.py. Regression test
  `test_arcticpy_build_never_reuses_a_pip_cached_wheel`.
- Evidence: Heart suite 1319 passed; control showed the test fails on the old
  script; independent separate-model review CLEAN; the PR's arcticpy self-test
  built fresh and imported on ubuntu-26.04 with libgsl28.
- Trap hit: the organ-code tenant firewall reds on a workspace repo name in a
  new test docstring. Fixed by rewording (5b11b0b).
- Post-merge: autocti_workspace Smoke Tests run 42883685928 re-run on main.
- Split out: draft/bug/health_fixes/smoke_cache_stats_warnings_nameerror.md.

## Original prompt

# arcticpy install restores a pip-cached wheel built against a missing libgsl

Type: bug
Target: PyAutoHeart
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-11-11
Issued: 2026-11-11
Repos: @PyAutoHeart (consumers: @PyAutoCTI @autocti_workspace @autocti_workspace_test)

## Evidence and reproduction

autocti_workspace Smoke Tests is RED on main
(https://github.com/PyAutoLabs/autocti_workspace/actions/runs/42883685928, push
of 9ab5582 from docs PR #48, 2026-11-10T19:17Z). Both py3.12 and py3.13 legs
fail in "Install arcticpy (CTI workspaces only — source-only C++ sdist)":

- apt installs GSL from Ubuntu 26.04 `resolute`: `libgsl-dev libgsl28` (2.8+dfsg-6).
- `pip install arcticpy==2.6` then reports
  `Using cached arcticpy-2.6-cp312-cp312-linux_x86_64.whl`.
- The import check fails:
  `ImportError: libgsl.so.27: cannot open shared object file`, so the
  verify-import step fails.

The wheel in `~/.cache/pip` was built on the previous runner image against
libgsl.so.27. The pip cache in `.github/workflows/smoke-tests.yml` is keyed
`pyauto-pip-${{ runner.os }}-py<ver>-e${{ env.PYAUTO_CACHE_EPOCH }}-<hash>`
with a matching prefix restore-key. Nothing in the key changes when the runner
OS image changes, so the stale locally-built wheel is reused.

The PR run (42881872398) skipped smoke because nothing relevant changed. The
11-08 push run passed on the old image. Re-running restores the same cache and
fails again. A later `NameError: name 'warnings' is not defined` in a cache-stats
stdin step is a follow-on failure to check, not the root cause.

This is Heart's only release-readiness blocker (Heart RED, score 55, 2026-11-11);
the 2026-11-10 nightly stopped at preflight because of it.

## Repair scope

Fix it at the source in PyAutoHeart, for every consumer of the shared
`install-arcticpy` action and the pip caches around it: smoke-tests.yml,
lib-tests.yml, docs-build.yml and arcticpy-action.yml (PyAutoCTI,
autocti_workspace, autocti_workspace_test, CTI docs). Candidates, tested before
choosing:

- add the runner image identity (`$ImageOS` / `$ImageVersion`, or the GSL
  soname) to the pip cache keys and restore-keys; and/or
- have `install_arcticpy.sh` never reuse a cached locally-built arcticpy wheel
  (`--no-cache-dir` or `--no-binary arcticpy` for that one install), so a
  system-library change can never be masked again.

Also check and fix the `warnings` NameError in the follow-on step. Do not mask
the failure by skipping the import check, the CTI smoke legs or the arcticpy
install. Do not hand-delete caches as the fix. Validate by re-running
autocti_workspace Smoke Tests on main (it must rebuild the wheel against
libgsl28 and pass) and confirm the other CTI consumers stay green. Check current
claims and use start-dev before implementation. No release, merge or CI bypass.
