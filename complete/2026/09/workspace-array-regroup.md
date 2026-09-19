# PyAutoArray grouped under array/

Moved the canonical checkout to `array/PyAutoArray` using the existing reversible migration tool. Mind PR#423 added the single manifest path and merged with all current-head workflows green. No library source or API changed.

## Import safety

`array/` is a plain grouping directory, with no `__init__.py`. Root activation places `array/PyAutoArray` on PYTHONPATH. Twelve subprocess checks passed both before and after the move across root/family/repo working directories, activated/unactivated environments and active/system Python. Every `import array` selected the standard-library built-in, not a namespace package; `array.array` construction/list conversion passed. AutoArray, Galaxy and Lens imports passed from all three working directories after activation; all six scientific/infrastructure import checks passed.

## Preservation and validation

One directory moved atomically, nine dependency symlinks repaired, fourteen local configs updated. Journal validation preserved directory identity, HEAD, dirty/untracked status. Both canonical Array and its existing linked worktree retained exact HEAD/status. All57 checkouts/worktrees were usable before removing this task's one Mind worktree; all12 deployed smoke bootstrap imports and manifest38/38 passed. Full repos_sync check, generated hooks and firewall passed. Thirty-nine focused manifest tests passed. Heart was STALE score85 (release rehearsal absent); no release performed.

Issue#422 closed; Mind task/registry/dashboard updated. Existing Mind draft deletion preserved. Receipts and rollback journal: `.migration/array/`. Existing shells should source `/home/jammy/Code/PyAutoLabs/activate.sh`.

## Original prompt

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
