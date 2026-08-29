# Active Tasks

## science-project-memory
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/315
- prompt: active/science_project_memory_a_fresh_chat_pointed.md
- follow-up-prompt: active/finish_the_science_project_memory_propagation_au.md (folded in,
  not a separate issue — `Folded-into: PyAutoBrain#315`)
- issued: 2026-08-28
- status: pushed, pr-blocked (Heart RED)
- worktree: ~/Code/PyAutoLabs-wt/science-project-memory
- classification: library (four independent assistant/organ repos; no workspace follow-up)
- repos:
  - PyAutoBrain: feature/science-project-memory (d2b1af9)
  - autolens_assistant: feature/science-project-memory (6b7c5c4)
  - autocti_assistant: feature/science-project-memory (df8408d)
  - autogalaxy_assistant: feature/science-project-memory (7964ff7)
  - autofit_assistant: feature/science-project-memory (1bc7675)
- next-skill: open the five PRs once Heart is GREEN (or under a human-authorized corrective
  exception naming the RED reason) — all branches are pushed and the work is complete
- heart-red-at-ship: "release validation FAILED (stage integrate)" — verbatim from
  `pyauto-heart readiness --json` at 2026-08-28T21:34:42Z; not caused by this task (markdown
  + one conductor mode + a hermetic test file). Reasons posted verbatim on the issue.
- note: phased — Phase 1 PyAutoBrain `clone sync` lever (9 new tests; suite 627 passed),
  Phase 2 autolens_assistant (the reference copy, deliverables A-D), Phase 3 propagated to
  autocti_assistant + autogalaxy_assistant via the new sync with the rejected hunks
  hand-resolved (autocti's orphan state.md reconciled into the template, not deleted).
  euclid_assistant was OUT OF SCOPE and never opened. Supporting commit already on Mind
  main: 2b764e48 (tenant-firewall allowlist).
- follow-up-folded-in (2026-08-28): the maintenance follow-up is part of THIS task, not a new
  issue. Leg B — the clone conductor's rename table is now one shared `name_substitutions()`
  for birth and sync, carrying the UPPERCASE package rule birth omitted plus `DOMAIN_NOUNS` /
  `DOMAIN_ALIASES` (the science's own noun; `microlensing` and `lensing-fluent` survive the
  anchor); unknown target science = no domain rule + a warning, never a guess. Brain suite
  627 -> 634 (clone-sync tests 9 -> 16). autocti_assistant re-synced: both birth gaps closed
  from the conductor's own substitution output, its profile examples hand-adapted, and its
  stale `.claude/skills/start-new-project.md` copy restored as the symlink every sibling has.
  autogalaxy carries neither gap. Leg A — autofit_assistant synced (`--since ee306ac`), all
  four rejected files hand-resolved keeping its domain adaptation and layering on #315's
  structure; 56 tests pass, boundary complete. Reported not-fixed: autocti's lensing *example
  strings* (slacs_subhalo, the SLaM run row, README filename examples) and three more
  `.claude/skills/` real-file copies — human domain adaptation, not substitutions.
- heart-ack: human authorisation 2026-08-28 — "open prs under red and merge i acknowledge".
  Heart RED reason acknowledged verbatim: "release validation FAILED (stage integrate)".
  YELLOW reasons acknowledged verbatim: "workspace validation not passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py, rectangular_mge_rtu.py)";
  "manifest drift: session-start hooks (generated) — 32 mismatch(es) vs PyAutoMind/repos.yaml".
  None of these reasons is caused by this task; the human authorised PR-open and merge under RED.

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
- heart-ack: human authorisation 2026-08-28 — "open prs under red and merge i acknowledge".
  Heart RED reason acknowledged verbatim: "release validation FAILED (stage integrate)".
  YELLOW reasons acknowledged verbatim: "workspace validation not passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py, rectangular_mge_rtu.py)";
  "manifest drift: session-start hooks (generated) — 32 mismatch(es) vs PyAutoMind/repos.yaml".
  None of these reasons is caused by this task; the human authorised PR-open and merge under RED.

## witt-wynne-projection
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/510
- issued: 2026-08-28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/witt-wynne-projection
- repos:
  - autolens_workspace: feature/witt-wynne-projection
