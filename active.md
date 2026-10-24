
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## likelihood-lifecycle-p0-profiling
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/442
- issued: 2026-10-23
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p0-profiling
- prompt: active/likelihood_lifecycle_p0_profiling.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/444 (PR 1 of 6, migration map) → aeef2756, 2026-10-23
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/447 (PR 2 of 6, move-only) → 0c6be19b, 2026-10-24
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/448 (PR 3 of 6, catalogue builder @3) → 81183fd8, 2026-10-24
- merged: https://github.com/PyAutoLabs/PyAutoPulse/pull/74 (PR 4, lens re-pin @3, receipt refetched; pulse check OK) → 5f3ec2c8, 2026-10-24
- next: AUTO RUN 2026-10-24 (human --auto, Heart YELLOW ack'd: manifest drift + PyAutoLens release validation stale): stacked PRs 3b (legacy layout; draft folded in) → 5 misc grouping → 6 coverage+parity, each to PR-open; merges human /prm in order
- repos:
  - autolens_profiling: (detached at main; next PR branches fresh)

## point-solver-guide
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/599
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: shipped, awaiting /prm (order: PyAutoLens#801 → ws#600 → ws#601 → HowToLens#101)
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/801
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/600, https://github.com/PyAutoLabs/autolens_workspace/pull/601, https://github.com/PyAutoLabs/HowToLens/pull/101
- worktree: ~/Code/PyAutoLabs-wt/point-solver-guide
- prompt: active/point_solver_guide.md
- epic: cluster-pointsolver-speed
- repos:
  - PyAutoLens: feature/point-solver-guide
  - autolens_workspace: feature/point-solver-guide-move, feature/point-solver-guide
  - HowToLens: feature/point-solver-guide
- heart-ack:
  - manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - release validation stale: source moved since rehearsal (PyAutoLens)
- summary: |
    3 PRs in order: (1) the PyAutoLens residual_threshold docstring fix; (2) a workspace move-only PR, point_source_pairing.py → guides/point_solver/pairing.py; (3) the new guide guides/point_solver/limitations.py plus a notebook (oracle, usage, assumptions, limitations). Judge tier, human /prm. Research follow-up filed as draft/research/autolens/point_solver_root_refinement.md.
