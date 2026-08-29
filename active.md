# Active Tasks

## science-project-memory
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/315
- prompt: active/science_project_memory_a_fresh_chat_pointed.md
- issued: 2026-08-28
- status: pushed, pr-blocked (Heart RED)
- worktree: ~/Code/PyAutoLabs-wt/science-project-memory
- classification: library (three independent assistant/organ repos; no workspace follow-up)
- repos:
  - PyAutoBrain: feature/science-project-memory (55e9fd4)
  - autolens_assistant: feature/science-project-memory (6b7c5c4)
  - autocti_assistant: feature/science-project-memory (523015b)
  - autogalaxy_assistant: feature/science-project-memory (7964ff7)
- next-skill: open the four PRs once Heart is GREEN (or under a human-authorized corrective
  exception naming the RED reason) — all branches are pushed and the work is complete
- heart-red-at-ship: "release validation FAILED (stage integrate)" — verbatim from
  `pyauto-heart readiness --json` at 2026-08-28T21:34:42Z; not caused by this task (markdown
  + one conductor mode + a hermetic test file). Reasons posted verbatim on the issue.
- note: phased — Phase 1 PyAutoBrain `clone sync` lever (9 new tests; suite 627 passed),
  Phase 2 autolens_assistant (the reference copy, deliverables A-D), Phase 3 propagated to
  autocti_assistant + autogalaxy_assistant via the new sync with the rejected hunks
  hand-resolved (autocti's orphan state.md reconciled into the template, not deleted).
  autofit_assistant is dry-run only (diverged 193/221/56/101 lines across the four generic
  files) — its report is on the issue for a human. euclid_assistant was OUT OF SCOPE and
  never opened. Supporting commit already on Mind main: 2b764e48 (tenant-firewall allowlist).

## anonymise-wfc3-ir-hole-regression-target
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/73
- prompt: active/anonymise_the_named_science_target_in_the.md
- issued: 2026-08-28
- status: library-dev, branch-pushed, pr-blocked-heart-red
- worktree: ~/Code/PyAutoLabs-wt/anonymise-wfc3-ir-hole-regression-target
- classification: library (PyAutoReduce only)
- repos:
  - PyAutoReduce: feature/anonymise-wfc3-ir-hole-regression-target
- commit: b4ee3697097fe91fe332b12d61c8479a6756a3fb
- tests: 299 passed, 3 skipped (test_autoreduce/, 2026-08-28)
- next-skill: ship_library step 4 (open the PR) once Heart clears; PR body is drafted verbatim
  on the issue comment https://github.com/PyAutoLabs/PyAutoReduce/issues/73#issuecomment-5458441602
- blocked-by: Heart readiness RED 2026-08-28T21:34:42Z - red_reasons: "release validation FAILED
  (stage integrate)". None of the RED/YELLOW reasons touch PyAutoReduce; needs a human to clear
  the RED or authorise the AUTONOMY.md corrective-PR exception.
- note: comment/test-name/doc rename only, no behaviour change. PyAutoMind history records
  (complete/, condemned.md, autonomy_log.md) are deliberately left untouched.

## witt-wynne-projection
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/510
- issued: 2026-08-28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/witt-wynne-projection
- repos:
