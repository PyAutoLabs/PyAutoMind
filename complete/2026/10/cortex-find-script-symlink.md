## cortex-find-script-symlink
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/471
- completed: 2026-10-06
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/475
- bundle: pyautobrain-worktree-guards

Merged PyAutoBrain#475 (d08edc8) into main 2026-10-06 via /prm (tier `notify`; PyAutoBrain has no PR test CI, gate was the local full Brain suite). Issue #471 closed.

Cortex find_script walks root.absolute().parents instead of root.resolve().parents, so a task worktree with a symlinked PyAutoCortex finds its own script, not the canonical one. Restored test_a_fixture_tree_finds_the_schema_its_checkout_ships verbatim + tmp_path symlink regression test. Cortex tests 49 passed; full suite 1197 passed.

No workspace impact (Brain tooling only); no pending-release obligation.

## Original prompt

# Cortex conductor test resolves through the worktree symlink and fails in every task worktree

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: notify
Witness: `python3 -m pytest PyAutoBrain/tests/test_cortex_conductor.py::test_a_fixture_tree_finds_the_schema_its_checkout_ships` passes from inside a task worktree root created by `worktree_create` (where the Cortex checkout is a symlink to the canonical checkout) as well as from the canonical root
Review-minutes: 0
Unattended: ready
Issued: 2026-10-05

## Symptom (observed 2026-09-02, task batch-review-integration)

Inside `~/Code/PyAutoLabs-wt/<task>/`, `test_a_fixture_tree_finds_the_schema_its_checkout_ships` asserts
`_cortex.find_script(skeleton) == cortex_root()/"scripts"/"cortex.py"` and gets
the canonical checkout's `scripts/cortex.py` instead: `find_script` resolves the symlinked Cortex checkout
entry to its real path while `cortex_root()` returns the unresolved worktree path. Same test
passes on the canonical checkout, so every Brain task ships with one deselected test and every subagent has to
be told it is an artefact.

## Fix direction

Compare resolved paths on both sides (`Path.resolve()` in the test, or make `find_script` and `cortex_root`
agree on resolution), whichever the conductor's own convention is. Do not weaken the assertion.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/c4232aa1-7376-4851-8e3f-29ef2f9e65cd/scratchpad/intake_cortex_test_v2.md -->
