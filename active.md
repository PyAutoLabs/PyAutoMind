# Active Tasks

## science-project-memory
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/315
- prompt: active/science_project_memory_a_fresh_chat_pointed.md
- follow-up-prompt: active/finish_the_science_project_memory_propagation_au.md (folded in,
  not a separate issue — `Folded-into: PyAutoBrain#315`)
- issued: 2026-08-28
- status: 3 of 5 PRs merged; 2 open on a pre-existing CI red (see library-pr below)
- worktree: ~/Code/PyAutoLabs-wt/science-project-memory
- classification: library (four independent assistant/organ repos; no workspace follow-up)
- repos:
  - PyAutoBrain: feature/science-project-memory (d2b1af9)
  - autolens_assistant: feature/science-project-memory (6b7c5c4)
  - autocti_assistant: feature/science-project-memory (df8408d)
  - autogalaxy_assistant: feature/science-project-memory (7964ff7)
  - autofit_assistant: feature/science-project-memory (1bc7675)
- library-pr: PyAutoBrain#316 (MERGED 8f5f7697658d585b42fa52ea6d6c0fcdd1988bda),
  autocti_assistant#27 (MERGED 0242d7be673673aa93c701d8b7ec37cbeba55566),
  autofit_assistant#31 (MERGED d5df11fba0bc2e9a54bf0318d705f0a4d0b3a1f1),
  autolens_assistant#116 (OPEN), autogalaxy_assistant#20 (OPEN)
- next-skill: /prm on autolens_assistant#116 + autogalaxy_assistant#20 once their `wiki-currency`
  red is resolved (or merged on the same pre-existing-red judgement their previous PRs took);
  then record the task complete and remove the worktree
- ci-blocker (2026-08-28): `wiki-currency` FAILS on both open PRs — autolens_assistant#116
  "Symbol audit (--scope all) exited 1" (missing/broken: 1); autogalaxy_assistant#20 the same
  plus "Citation paths (--check-citations) exited 1" (`wiki/core/operations/sandbox.md` cites
  `PyAutoGalaxy:autogalaxy/plot/plot_utils.py`, absent from the source tree). Both are
  `wiki/core` / skill-audit drift; this branch touches neither. Pre-existing: the same leg
  failed on both repos' previous PRs (#115, #19 — pynufft residue phase 2, 2026-08-23), which
  were merged anyway. No code was modified to make the leg pass.
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

## witt-wynne-projection
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/510
- issued: 2026-08-28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/witt-wynne-projection
- repos:
  - autolens_workspace: feature/witt-wynne-projection

## cmap-magma-default
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/509
- prompt: active/cmap_magma_default.md
- issued: 2026-08-28
- status: library-shipped, workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/cmap-magma-default
- classification: combined (library first, then the Euclid pipeline workspace)
- epic: euclid-dr1-prep (phase 0 of 10; gates nothing, gated by nothing)
- repos:
  - PyAutoArray: feature/cmap-magma-default
  - euclid_strong_lens_modeling_pipeline: feature/cmap-magma-default
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/510
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/42
- commit: c8fe47f35e37f4ea8a51303ece0ab5f708def460 (PyAutoArray); c7c3941a3ccd5a1a28c5327cd1ef09be004e8fd0 (euclid pipeline)
- tests: 1337 passed, 0 failed (test_autoarray, 2026-08-28); euclid PR is config+docs only, no scripts changed
- merge-gate: library-first — PyAutoArray#510 must merge before euclid#42
- heart-ack: Heart RED at ship time for an unrelated reason, verbatim: "release validation
  FAILED (stage integrate)". YELLOW, also unrelated, verbatim: "workspace validation not
  passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py,
  autolens_test scripts/imaging/rectangular_mge_rtu.py)"; "manifest drift: session-start hooks
  (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml". PR opened under the standing human
  authorisation recorded 2026-08-28 ("open prs under red and merge i acknowledge"); NOT merged.
