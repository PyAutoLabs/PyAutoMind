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
