# M3.6f Shift worker cost: scoped smoke, hermetic Brain tests, no `pgrep` waits, `ruff format`, worker PATH

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-17
Epic: autonomous-orchestrators
Phase: 10
Consequence: glance
Witness: (1) `PYAUTO_MIND=/nonexistent PYAUTO_BRAIN=/nonexistent PYAUTO_SHIFT_SLOT=x python -m pytest -q` in PyAutoBrain gives the same pass count as a clean environment, with 0 failures; (2) the tests red on main under a shift-worker environment (`test_orchestrator_mind_writer`, `test_questions_inbox`, the prompt_budget/node and grouped_organ_consumers tests named in the PyAutoBrain#655 gate line) pass; (3) `grep -rn "pgrep -f" skills/ship_library skills/ship_workspace` matches only the sentence that forbids it; (4) a smoke-planner test: a `glance` ship whose impact check reports "no migration" selects only the impact-scoped scripts, not all six workspaces; (5) a dry worker spawn's first turn prints a path for both `command -v pyauto-heart` and `command -v pytest`
Lane: any
Unattended: ready

## Why

Worker minutes in shift 2026-11-16-pm went to things that were not the task.

- **Smoke out of proportion.** A full six-workspace smoke for a six-line config default took
  32 of the 43 minutes of `ellipse_multipole_latent_missing_m`. The worker's own impact check
  had said "no migration". It waited for smoke before opening the PR, so PyAutoGalaxy#720
  opened at 19:24:59Z, after the digest.
- **Brain tests not hermetic.** `PYAUTO_MIND`, `PYAUTO_BRAIN` and `PYAUTO_SHIFT_*` leak into
  tests meant to be hermetic, and three tests are red on main. About 22 worker-minutes across
  two workers (the #655 gate line: "7F/10E identical on main 678dba7 … shift-worker env").
- **A `pgrep -f` wait loop matched itself.** One worker waited 9 minutes.
- **Formatting and PATH.** Workers pushed unformatted code and found `pyauto-heart` or
  `pytest` missing from PATH.

## What

1. For `glance` work, the ship skills scope smoke to the impact check's answer, and open the PR
   before any smoke that will take more than a few minutes; smoke results land on the PR.
2. An autouse fixture in PyAutoBrain's `conftest.py` unsets `PYAUTO_MIND`, `PYAUTO_BRAIN` and
   `PYAUTO_SHIFT_*` for every test. Fix the three tests that are red on main.
3. The ship skills say: never wait with a `pgrep -f` loop; wait on the process id you started.
4. The ship skills run `ruff format` on changed files before push.
5. The worker session template puts `pyauto-heart` and `pytest` on PATH (the venv's `bin`).

## Out of scope

- The worker environment as a whole: venv choice, SSH keys, `sacct` (infrastructure review).
- Heart counting behind or dirty local checkouts as RED (infrastructure review; R1 is M3.6h).
