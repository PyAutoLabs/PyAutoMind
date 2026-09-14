`autolens_workspace/config/build/profile_release.yaml`'s existing `imaging/start_here` override
(which already set `PYAUTO_SMALL_DATASETS: "0"`) now also carries
`BUILD_SCRIPT_TIMEOUT: "3600"`, giving that one script a per-script cap in the release profile.
The run-wide 1800 s cap is untouched — it remains the only guard on the other 84 entries.
Config-only: no scripts, notebooks or library source in the diff.

## Why

`scripts/imaging/start_here.py` was killed at the run-wide 1800 s cap in **3 of the last 8**
Release Integrate runs (2026-09-09, 2026-09-12, 2026-09-14 run 34898325503, each logging 1805 s),
while passing runs of the same script span 586-1695 s and every sibling in the leg is stable.
Each kill lands inside one ~26 min XLA CPU compile of `MultiStartProdigy` (`n_starts=48`,
`batch_size=None`) under this script's non-uniform over-sample map, *before the first gradient
step* — compiling, not iterating, when the cap fires. No library commit in the window touches
that path, and the 09-09 kill predates the commits in it, so it is a compile-time flake rather
than a regression.

Cost: worst case +30 min on the single slowest leg of a ~72 min job, and only when the flake
fires; a healthy run is unchanged.

## Shipped

- autolens_workspace PR #548 — merged 2026-09-15 as `b581bfcbf518b44f3234250aef8d66ceab5bf228`
  (https://github.com/PyAutoLabs/autolens_workspace/pull/548)
- Issue #547 closed as completed.
- CI at merge: all 7 checks green on head `52301be7` — Navigator Check (paths+banner lint,
  catalogue staleness, unbatched multi-start search), Script Size Guard, Smoke Tests
  (changes, 3.12, 3.13).

## Follow-up

The real fix — the `MultiStartProdigy` compile time itself — stays filed as
`draft/bug/autolens_workspace/start_here_multistart_compile_time.md`. This record raises the cap;
it does not close that.

## Original prompt

# Per-script BUILD_SCRIPT_TIMEOUT for imaging/start_here in the release profile

Type: maintenance
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- release-validation
- ci-timing
Difficulty: easy
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: `config/build/profile_release.yaml` carries `BUILD_SCRIPT_TIMEOUT: "3600"` on the existing `imaging/start_here` override; `validate_env_profiles.py` passes; PyAutoHands `build_util.timeout_for` resolves 3600 for that script and 1800 (workflow global) for its siblings
Review-minutes: 5
Filed: 2026-09-14
Issued: 2026-09-14

User request (verbatim, 2026-09-14):

"""
can you fix the PyAutoHeart being red
"""
(follow-up "continue"; plan approved 2026-09-14 23:50.)

## Context

PyAutoHeart release-integrate (cap BUILD_SCRIPT_TIMEOUT=1800, workspace-validation.yml:387) has killed
`autolens_workspace/scripts/imaging/start_here.py` 3 times in the last 8 runs (09-09, 09-12, 09-14 22:32
run 34898325503) at 1805 s; passing runs range 586-1695 s while every sibling in the leg is stable. All three
kills are inside one ~26-min XLA CPU compile in `MultiStartProdigy` (`n_starts=48, batch_size=None`) under
the script's non-uniform over-sample map, before the first gradient step. It is a compile-time flake, not a
regression (no library commit in the window touches that path; the 09-09 kill predates them).

`PyAutoHands/autohands/build_util.py:55-86` `timeout_for()` reads a per-script `BUILD_SCRIPT_TIMEOUT` from the
profile env first and it wins over the workflow global (precedent
`autolens_workspace_test/config/build/profile_smoke.yaml:123`). `profile_release.yaml` already has an
`overrides` entry `pattern: "imaging/start_here"` setting `PYAUTO_SMALL_DATASETS: "0"`.

## Fix

Add `BUILD_SCRIPT_TIMEOUT: "3600"` to that existing override (do not raise the run-wide 1800 s; it guards the
other 84 entries). Note the cost in the PR: up to +30 min on the worst leg of a ~72 min job. The real fix
(explicit batch_size / uniform over-sample map for the compile) is filed separately:
draft/bug/autolens_workspace/start_here_multistart_compile_time.md.
