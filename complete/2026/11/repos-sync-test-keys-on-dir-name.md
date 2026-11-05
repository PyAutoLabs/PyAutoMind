- summary: already shipped — closed as stale draft. Commit 679b1319f (2026-10-16, "test: Mind suite green on main — shadow line says window reached; standards test keys on PyAutoMind") changed `test_mind_owns_an_exact_generated_block` to key on the literal `specs["PyAutoMind"]`, so the lookup no longer depends on the checkout directory name.
- witness: `pytest tests/test_repos_sync_standards_block.py tests/test_autonomy_log_shadow.py` → 47 passed on main (2026-11-05).
- found by: queue check-in 2026-11-05 (the draft was never closed when the fix landed directly on main).

## Original prompt

# repos_sync standards-block test keys on the checkout dir name (KeyError in non-canonical worktrees)

Type: bug
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: easy
Autonomy: safe-capped
Priority: low
Status: formalised
Consequence: glance
Witness: `pytest tests/test_repos_sync_standards_block.py` passes from a worktree whose directory is not named `PyAutoMind`.
Filed: 2026-10-16

## Finding

`test_mind_owns_an_exact_generated_block` looks itself up as `specs[MIND.name]` where MIND is the checkout directory, so any worktree named otherwise raises `KeyError: 'mind'` (passes in a dir named PyAutoMind). Introduced by 968ff2b9 (10-06). Fix: key on the literal "PyAutoMind" or resolve from repos.yaml by path.
