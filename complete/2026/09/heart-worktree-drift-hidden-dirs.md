- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/198 (closed, completed)
- completed: 2026-09-04
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/200 (MERGED 2026-09-04T16:31:41Z, 911d7740)
- shipped: `heart/checks/worktree_drift.py::scan` now skips hidden directory names when it
  *discovers* worktrees under the wt root, so `~/Code/PyAutoLabs-wt/.idea` — the user's
  JetBrains project dir, a directory claimed by neither `active.md` nor `parked.md` — stops
  being reported as a permanent, unclearable ORPHAN. The claims leg is deliberately
  untouched: `active_claims + parked_claims` still go through `note()` unconditionally, so a
  task whose `worktree:` genuinely points at a dotted path (`PyAutoLabs/.codex-worktrees/<task>`,
  the case the path test in #123 exists for) is still noted, still counted in `on_disk`, and
  still never reported MISSING. The filter governs what the sweep *discovers*, not what the
  Mind *claims*. `scan()`'s signature and return shape are unchanged; the check is
  monitoring-only and never a readiness reason.
- verified: witness met — `pytest tests/test_worktree_drift.py -q` green with the new case;
  full `pytest tests/ -q` in the task worktree `681 passed in 60.09s`. The new test **fails
  without the fix**: reverting only the `startswith(".")` guard gives `1 failed, 9 passed`
  with `At index 0 diff: '.idea' != 'mystery'`, so the guard is what the assertion measures.
  Live check against the real wt root (which currently holds a `.idea`): `orphans: []`,
  `on_disk_count: 7`, where before `.idea` was in the orphan list. CI on head `c9d3c89f`:
  the sole run for the sha (Heart Tests, `pull_request`) completed/success on both pytest
  legs; `mergeStateStatus` CLEAN.
- tests: two added to `tests/test_worktree_drift.py` —
  `test_hidden_dirs_under_wt_root_are_not_orphans` (a `.idea` dir with a `workspace.xml`
  child beside a genuine unclaimed worktree; orphans names only the genuine one,
  `on_disk_count == 1`) and `test_hidden_dir_that_is_explicitly_claimed_is_still_tracked`
  (a claimed `.codex-worktrees/some-task`; `missing == []`, `orphans == []`,
  `on_disk_count == 1`) — the regression guard for the leg that was *not* filtered.
- notes: `pyauto-heart readiness --json` was RED at ship time for a reason unrelated to and
  pre-dating this branch (`release validation FAILED (stage integrate)`, owned by the active
  task `profiles-jit-powerlaw-exact-zero-atol`, autolens_workspace_test#291/#292), plus a
  yellow `PyAutoArray: open PR 12d old`. Merge was the human call at `/prm`.
  `pyauto-heart freeze --show` reported not frozen, and PyAutoHeart is an organ repo rather
  than a `category: library` one, so the freeze gate did not apply. No `pending-release:`
  obligation — organ repos do not publish.

## Original prompt

# Worktree drift reports hidden dirs (.idea) under the wt root as orphan worktrees

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Issued: 2026-09-04
Consequence: notify
Witness: `pytest tests/test_worktree_drift.py -q` passes with a new case asserting a `.idea` directory sitting under the wt root beside a genuine unclaimed worktree yields exactly one orphan (the genuine one)
Review-minutes: 5
Unattended: ready

## Symptom

`heart/checks/worktree_drift.py::scan` enumerates the worktree root with

```python
if wt_root.is_dir():
    for entry in sorted(wt_root.iterdir()):
        if entry.is_dir():
            note(entry, entry.name)
```

Every directory under `~/Code/PyAutoLabs-wt/` is therefore treated as a task
worktree. The user's JetBrains project directory `~/Code/PyAutoLabs-wt/.idea`
is a directory, is claimed by neither `active.md` nor `parked.md`, and so is
reported as an ORPHAN — a permanent, unfixable drift line that degrades the
Heart worktree-drift surface for something that is not a worktree at all and
never will be.

## Original request (verbatim)

> heart/checks/worktree_drift.py (~line 107) treats every directory under the
> worktree root (~/Code/PyAutoLabs-wt/) as a task worktree, so the user's
> JetBrains `.idea` project dir is reported as an orphan and degrades Heart
> readiness. Fix: skip hidden directories (name starts with "."). Extend the
> existing worktree_drift test in PyAutoHeart/tests/ with a case where a
> `.idea` dir sits under the wt root beside a real orphan and assert only the
> real one is reported.

## Fix direction

Skip hidden entries in the wt-root sweep only — `entry.name.startswith(".")`.
Claimed paths keep going through `note()` unconditionally, so a task whose
`worktree:` claim genuinely points at a dotted path is still tracked and never
reported missing; the filter is about what the sweep *discovers*, not about
what the Mind *claims*.

## Tests

Extend `tests/test_worktree_drift.py` with a case placing a `.idea` directory
under the wt root next to a genuine unclaimed worktree, asserting the orphan
list names only the genuine one.
