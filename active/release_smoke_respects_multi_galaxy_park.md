# Keep the live release smoke gate aligned with the multi-galaxy SLOW park

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Priority: high
Status: formalised
Consequence: block
Witness: a release-smoke selection check excludes `scripts/multi_galaxy/start_here.py` while its `config/build/no_run.yaml` SLOW park remains, and still selects the other `multi_galaxy/` smoke entries. The existing script-cost profiling task remains separate; no tutorial script or library source is weakened.

## Context

autolens_workspace PR #564 merged the SLOW park on 2026-09-18. Subsequent PyAutoHeart release-integration runs 35383847533 and 35402982151 succeeded. The live PyAutoHands release run 35407848659 published all five libraries at 2026.9.19.1, but its independent `run_smoke_tests (autolens_workspace)` job still selected `scripts/multi_galaxy/start_here.py` from `smoke_tests.txt` and failed on a runner shutdown signal (exit 143). `no_run.yaml` does not govern that smoke list.

Keep the park explicit and auditable. Do not change the script's science, lift its runtime cap, dispatch another release, or subsume the separate `draft/bug/autolens_workspace/multi_galaxy_start_here_release_cost.md` investigation.

## Original user request (verbatim)

> ok do that fix
