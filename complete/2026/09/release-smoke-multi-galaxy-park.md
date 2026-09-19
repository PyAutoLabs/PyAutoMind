# Release smoke honours the multi-galaxy SLOW park

- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/565 (closed completed)
- completed: 2026-09-19
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/566 (merged 2026-09-19, head `acec7e8a`, merge `7ff94f315b6aac0c37033dc0e7b36ff2442660f5`)
- summary: The curated `smoke_tests.txt` no longer runs `multi_galaxy/start_here.py` while its existing `config/build/no_run.yaml` SLOW park remains. The other 18 multi-galaxy smoke entries stay enabled; no tutorial script, library source, notebook, or release workflow changed.
- validation: 37/37 local smoke scripts and 2/2 notebooks passed; PyAutoHands allowlist/release-smoke tests 15 passed; PR checks 7/7 green across all three workflow runs; branch review CLEAN; Heart STALE only for absent fresh release-validation evidence at ship time.
- follow-up: `draft/bug/autolens_workspace/multi_galaxy_start_here_release_cost.md` remains open to profile the script and restore it to both gates when viable. This task did not dispatch a release.

## Close-out notes

The 2026.9.19.1 live release published all five libraries but had a red workspace smoke leg because the independent explicit allowlist still included the script after PR #564 parked it for release integration. The runner intentionally treats the allowlist as authoritative over `no_run.yaml`, so the one-line allowlist change is scoped to this workspace and does not alter global runner semantics or other workspaces' coverage.

## Original prompt

# Keep the live release smoke gate aligned with the multi-galaxy SLOW park

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Priority: high
Status: formalised
Consequence: block
Issued: 2026-09-19
Witness: a release-smoke selection check excludes `scripts/multi_galaxy/start_here.py` while its `config/build/no_run.yaml` SLOW park remains, and still selects the other `multi_galaxy/` smoke entries. The existing script-cost profiling task remains separate; no tutorial script or library source is weakened.

## Context

autolens_workspace PR #564 merged the SLOW park on 2026-09-18. Subsequent PyAutoHeart release-integration runs 35383847533 and 35402982151 succeeded. The live PyAutoHands release run 35407848659 published all five libraries at 2026.9.19.1, but its independent `run_smoke_tests (autolens_workspace)` job still selected `scripts/multi_galaxy/start_here.py` from `smoke_tests.txt` and failed on a runner shutdown signal (exit 143). `no_run.yaml` does not govern that smoke list.

Keep the park explicit and auditable. Do not change the script's science, lift its runtime cap, dispatch another release, or subsume the separate `draft/bug/autolens_workspace/multi_galaxy_start_here_release_cost.md` investigation.

## Original user request (verbatim)

> ok do that fix
