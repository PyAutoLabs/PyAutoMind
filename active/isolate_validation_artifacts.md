# Preserve artifact directories during workspace validation

Issued: 2026-10-26
Type: bug
Target: pyautoheart
Repos: @PyAutoHeart
Consequence: judge

## Original user request

I dont want any open PRs, including community stuff, scan all repos and work out if we need to do anything to reach this state

ok do all that, but note that Pulse we are working on so ignore

## Approved scope

User authorized development under the surfaced Heart RED reasons, including addressing release blockers needed for the Galaxy dependency. No publication or rehearsal through RED. Pulse #79 is excluded.

## Plan

Fix `.github/workflows/workspace-validation.yml` artifact download to preserve a directory per artifact rather than flattening same-named smoke_timings.json files. Keep recursive provenance and aggregation behavior. Add regression coverage in tests/test_workflow_wiring.py and tests/test_result_provenance.py for nested artifacts and malformed genuine result shards. Replay retained successful script artifacts from Heart run 40288100810 to establish report correctness without rerunning fits. Preserve adverse smoke evidence and freshness requirements; do not claim a release-ready verdict from partial validation.

The separate group/slam smoke zero-width-prior failure needs diagnostic confirmation of a narrowly scoped sampler-mode override; do not change scientific prior bounds in this task.

## Branch survey

Canonical PyAutoHeart is clean main, no existing worktree or registry conflict. Worktree `.worktrees/isolate-validation-artifacts/PyAutoHeart`, branch `feature/isolate-validation-artifacts`.

Tier: judge — merge mode: explicit live human approval for green in-turn merges.
