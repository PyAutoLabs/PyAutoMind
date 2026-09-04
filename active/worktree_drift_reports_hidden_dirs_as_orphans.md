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
