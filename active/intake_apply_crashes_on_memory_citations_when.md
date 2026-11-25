# intake --apply crashes on memory citations when the Mind is a worktree

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: with a Mind directory whose parent holds several sibling `*/PyAutoMind` checkouts, `intake --apply classify --file` writes the prompt with a `Memory:` line from the workspace-root PyAutoMemory (unit test pins it; the test fails on main before the fix)
Review-minutes: 0
Unattended: ready
Lane: any
Issued: 2026-11-25

Source: human report in a Science session, 2026-11-25. Request copied verbatim below; the approved plan follows it.

PyAutoBrain bug (repo: ~/Code/PyAutoLabs/organs/PyAutoBrain). Follow ~/Code/PyAutoLabs/AGENTS.md and the PyAutoLabs dev workflow (plan first, wait for approval before editing source).

Symptom, observed 2026-11-25: `pyauto-brain intake --apply classify --file <raw.md>` crashes when PYAUTO_MIND points at a temporary PyAutoMind worktree created under ~/Code/PyAutoLabs-wt (the doctrine route for Mind writes: `git worktree add --detach ~/Code/PyAutoLabs-wt/<name> origin/main`). The dry run (no --apply) works; only the write path fails.

Traceback tail:

    agents/conductors/intake/_intake.py:1036 write_prompt
    agents/conductors/intake/_intake.py:933 memory_citations
    agents/conductors/intake/_intake.py:919 _memory_home  ->  repo_path(mind.parent, "PyAutoMemory")
    agents/_repo_paths.py:203 repo_path -> manifest_paths(root) -> manifest_text(root) -> bootstrap_repo_path(Path(root), 'PyAutoMind')
    agents/_repo_paths.py:166 ValueError: PyAutoMind: ambiguous checkouts: ~/Code/PyAutoLabs-wt/digest-review-table/PyAutoMind, ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p5f/PyAutoMind, ~/Code/PyAutoLabs-wt/parked-hold-grace/PyAutoMind

Cause: `_memory_home(mind)` treats `mind.parent` as the workspace root. For a worktree under ~/Code/PyAutoLabs-wt the parent holds many task folders each with their own PyAutoMind, so bootstrap_repo_path raises instead of resolving. Workaround that worked: export PYAUTO_MEMORY=~/Code/PyAutoLabs/organs/PyAutoMemory.

Wanted: memory citations should resolve PyAutoMemory from the real workspace root (agents/_pyauto_root.py `pyauto_root()`, which honours PYAUTO_ROOT and the .pyauto-root marker) rather than from the Mind checkout's parent, or at least degrade to "no citations" instead of crashing the write, as the docstring of `_memory_home` ("or None when it is absent") implies. Add a regression test that runs the apply path with a Mind directory whose parent contains several sibling */PyAutoMind checkouts. Check whether other callers of `repo_path(mind.parent, ...)` in _intake.py have the same assumption.

## Findings (read-only investigation, 2026-11-25)

- Reproduced: `_memory_home(<Mind worktree under PyAutoLabs-wt>)` raises the ValueError above; the canonical Mind resolves.
- Only non-organ targets reach `memory_citations` (`_cites_memory(target)`), so organ-targeted prompts file without crashing.
- The lookup is wrong even when it does not raise: with exactly one task folder holding a PyAutoMind, it would read that task's feature-branch `repos.yaml`.
- `_intake.py:919` is the only `repo_path(mind.parent, ...)`.

## Approved plan (human approved 2026-11-25)

1. `_memory_home`: `PYAUTO_MEMORY` override first, then `repo_path(pyauto_root(), "PyAutoMemory")`, matching the shell `resolve_memory`.
2. Catch `ValueError`/`OSError` from resolution, return `None`, print one stderr line with the reason: no citations rather than a crashed write.
3. Drop the unused `mind` argument from `_memory_home` and `memory_citations` (one source call site, the test call sites, `tests/test_grouped_organ_consumers.py`).
4. Regression test in `tests/test_intake_memory.py`: a Mind directory whose parent holds several sibling `*/PyAutoMind` checkouts, a separate marked workspace root with a fixture PyAutoMemory, `--apply classify --file` run through `main()`; the prompt is written with a `Memory:` line from the workspace Memory. It must fail on main first.
5. Degrade test: `PYAUTO_ROOT` pointed at the ambiguous directory; the write succeeds with no `Memory:` line.
6. The existing memory tests set `PYAUTO_ROOT=tmp_path`; a `conftest.py` autouse guard points `PYAUTO_MEMORY` at a nonexistent path unless a test opts in, so a test filing into a tmp Mind never reads the real PyAutoMemory on a developer box.

## Out of scope (separate task, human decision)

`looks-shipped` and `reconcile --strong` default `--root` to `mind.resolve().parent` (`_intake.py:4411`, `:4441`). `_shipped.local_repos` catches the error, so they do not crash, but with a worktree Mind they scan only the Mind, and with the canonical Mind they see `organs/` only (15 checkouts, no libraries; the workspace root has 54).

<!-- formalised by the Intake (Conception) Agent on 2026-11-25 from file:/tmp/claude-1000/-home-jammy-Science/e7c0d88c-b4d4-45be-adc2-790feac4d7bc/scratchpad/raw.md -->
