
## tutorial-documentation-style
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/539
- issued: 2026-10-24
- session: Codex (local CLI; session ID unavailable)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/tutorial-documentation-style
- prompt: active/tutorial_documentation_style_resource.md
- repos:
  - PyAutoBrain: feature/tutorial-documentation-style
- heart-red-override:
  - authorized: 2026-10-24 — live human “I authorize”
  - red: `PyAutoLens: 2 commit(s) behind origin`
  - gates: 4 targeted tests + 1263 broader Brain tests PASS; PyAutoBrain discovery, agent surface and diff checks PASS; smoke n/a (Brain docs/skill wiring); in-session diff/link/single-source review CLEAN
  - authorization: https://github.com/PyAutoLabs/PyAutoBrain/issues/539#issuecomment-6384318621
  - scope: commit/push/PR-open only; no merge/release/check bypass; this branch does not repair Heart

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
