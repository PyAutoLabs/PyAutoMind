# Active Tasks

## phase8b-f2-ruling-scorer-verdict
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/185
- issued: 2026-08-28
- prompt: active/phase8b_f2_ruling_scorer_verdict.md
- session: claude --resume 3ebe0d5d-2ca4-45f2-9d81-8521e3266e29
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/186
- worktree: ~/Code/PyAutoLabs-wt/phase8b-f2-ruling-scorer-verdict
- repos:
  - autolens_profiling: feature/phase8b-f2-ruling-scorer-verdict
- note: architect ruling recorded in DECISIONS.md BEFORE scoring. Verdict is PRELIMINARY (24/39); re-run when RAL job 341978's 15 arms land.

## joint-clipper-compose-with-bijector
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1539
- issued: 2026-08-28
- prompt: active/joint_clipper_compose_with_bijector.md
- session: claude --resume 3ebe0d5d-2ca4-45f2-9d81-8521e3266e29
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/joint-clipper-compose-with-bijector
- repos:
  - PyAutoFit: feature/joint-clipper-compose-with-bijector
- note: Option B (approved). Compose the joint clipper with identity-kind linear maps (R -> R/s), refuse only genuinely non-linear ball pairs. Campaign follow-up (Phase 8B logit arm restated as BijectorPerPath excluding ell_comps.*) is an autolens_profiling config change, NOT in this PR.
