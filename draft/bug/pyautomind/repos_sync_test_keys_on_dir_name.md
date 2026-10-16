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
