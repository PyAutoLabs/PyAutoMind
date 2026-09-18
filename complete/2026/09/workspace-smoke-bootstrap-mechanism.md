# Smoke bootstrap mechanism — phase 2c, first stage

Merged [PyAutoMind#417](https://github.com/PyAutoLabs/PyAutoMind/pull/417) on
2026-09-18 at `2e3c54823d30e75782c9129829aa7be3b96542b9`.
This records the mechanism only. Phase 2c remains active under issue #416 and
`active/workspace_smoke_shim_bootstrap.md`; none of the twelve consumer copies
has been changed by this task.

## Shipped

One canonical bootstrap block, manifest opt-ins, exact legacy adoption and
bounded regeneration, installation drift checking, and event-driven propagation
with a disposable-clone dry run. CI's import-first behavior and all five runner
variants are preserved. Local discovery uses the marker/shared-resolver contract
with a bundle containment guard. Writes reject unknown bootstrap shapes,
ambiguous checkout identities, and symlinked destinations including the root and
its ancestors. The token-dependent workflow is excluded from fresh templates.

`smoke_bootstrap_rollout: false` is deliberately retained. Ordinary drift output
says installations are not graded during the hold; the narrow `--check` still
reports actual installation drift. No universal manifest-path rule, directory
move, or Heart install-chain change was made.

## Evidence and corrections

- Full Mind suite: 565 passed. Root-discovery tests require PYAUTO_ROOT unset;
  the task activation script otherwise overrides their fixtures.
- Independent Sol review: CLEAN after fixing its root-symlink escape finding
  and the full suite's missing workflow template classification.
- All twelve actual shim copies import Hands in a nested fixture. One canonical
  source edit regenerates all twelve with byte-identical exterior code.
- Fresh remote-clone dry run: twelve bootstrap-only would-push diffs, no pushes.
- Exact PR head `44d9d3bc4b00642f32d0e0f5cc6e801ddf0bc841`: both workflow runs
  successful; firewall and privacy jobs passed, template publication intentionally
  skipped on pull requests. Mergeability CLEAN. Human authorized merge explicitly.

## Remaining

Coordinate active lens workspace and Euclid pipeline claims before enabling
rollout. Then propagate and verify every installed copy; only that completes the
phase-2c witness. Issue #416, its active prompt and task worktree remain for that
continuation. Phase 3 stays deferred. The canonical Mind checkout's pre-existing
staged draft deletion was preserved.
