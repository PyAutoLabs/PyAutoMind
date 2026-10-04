## retired-repo-sidecars
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/278
- completed: 2026-10-04
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/279
- pending-release: PyAutoHeart@https://github.com/PyAutoLabs/PyAutoHeart/pull/279
- summary: Aggregate only repositories in a valid current Heart monitoring roster; preserve all caches, configured adverse evidence and global checks. Missing/malformed configuration conservatively retains observations.
- validation: Two regressions failed before repair; 22 focused and 1200 full tests passed; independent review CLEAN. Exact-head run37203283615 passed both Python3.12 and3.13. Copied-cache replay excluded only retired PyAutoConf/PyAutoBuild and preserved all150 files.
- merge: Human “Yes merge via prm” authorized merge of ba9d2f3 at 3d86fd8684cf30172ff22950d391df3345a3799f. Git ancestry proves the entire task branch merged.
- heart-red-override: Current task-specific development grant recorded on issue, PR, active registry and autonomy log; exact reason release validation FAILED (stage integrate). Merge was separately authorized after all CI passed. No release or bypass.
- remaining: Umbrella #274 remains open. The rectangular_rtu.py release timeout is unresolved; twelve focused diagnostic executions passed but do not clear failed TestPyPI validation. Anthropic credentials/digest workflow explicitly untouched.

## Original prompt

# Exclude retired repository sidecars from current Heart observations

Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/278
Issued: 2026-10-04

Type: bug
Priority: high
Difficulty: small
Autonomy: human-required
Target: @PyAutoHeart

## Original request

Do dashboard repair and continue heart work

Parent request: Check why heart is red, fix it, and then do anything else to make whole dashboard green

## Reproduction

`heart.state.aggregate()` globs all cached per-repository JSON files without consulting current config/repos.yaml. Cached PyAutoConf observations remain in the current dashboard although the repository is not configured for monitoring. The old required Tests workflow is permanently reported in_progress, adding false grey/yellow findings.

## Plan within approved dashboard repair scope

Use the current Heart monitoring configuration to select repository sidecars during aggregation. Retain every cache file on disk; exclude only names proven outside a valid configured roster. Invalid/missing/malformed configuration must retain observations rather than silently manufacture green. Preserve global checks and current configured repository missing-evidence behavior. Keep fixture/test configuration explicit.

Add regression tests for retired and configured observations, cache preservation, missing/malformed config and unchanged global evidence. Run focused and full Heart suites, independent review, and an isolated replay of the existing cache to prove PyAutoConf alone is removed among configured-repo observations. No policy or thresholds change.

Affected repository: PyAutoHeart; source heart/state.py, tests/test_state.py and affected aggregation fixtures/documentation only. Branch feature/retired-repo-sidecars. Tier undeclared; human /prm merge.
