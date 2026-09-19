# Group the PyAutoArray checkout under array/

Issued: 2026-09-19
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/422
Type: maintenance
Target: @PyAutoMind (manifest), local @PyAutoArray checkout placement

## Original request

move it, but make sure array wouldnt cause import issues

## Approved scope

Move the remaining canonical PyAutoArray checkout into array/PyAutoArray, preserving data and existing worktrees. Use the existing shared resolver and journaled migration. Keep array/ a plain grouping directory with no __init__.py; PYTHONPATH must contain array/PyAutoArray, not turn array/ into a Python package. Prove import array still resolves to the standard library and behaves correctly from the root, family and repo directories, with and without activation; validate autoarray/autogalaxy/autolens imports and manifest coverage.

## Detailed plan

1. Survey Mind and Array branches/claims; edit only Mind repos.yaml on a task worktree, adding path: array/PyAutoArray. No PyAutoArray source changes.
2. Check generated manifest consumers and resolver/migration tests. Confirm standard-library array resolution in a temporary equivalent folder layout before moving. Ship manifest PR with green checks.
3. Refresh canonical manifest, generate routing table, plan and inspect one-repo journal at .migration/array/cutover.json. Apply, repairing registered Git worktrees, dependency links, IDE/config and root activation.
4. Verify directory identity, commit/status preservation, standard-library array and scientific imports, twelve smoke bootstraps, manifest coverage and retained worktrees. Close task and preserve evidence.

Branch: feature/workspace-array-regroup
