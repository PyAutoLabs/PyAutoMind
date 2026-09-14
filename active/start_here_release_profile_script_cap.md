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
