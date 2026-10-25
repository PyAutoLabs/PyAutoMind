
## likelihood-lifecycle-p2x-same-host
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/464
- issued: 2026-10-25
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2x-same-host
- prompt: active/likelihood_lifecycle_p2x_same_host_projection.md
- epic: likelihood-lifecycle
- next: PR #465 OPEN (ef6e6014/362a28c7/7b11cba3). NEXT: lint green → HUMAN /prm → close #464. Then Pulse view + 2b (each needs its own RED override while Heart is RED).
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/465
- heart-red-override:
  - authorized: 2026-10-25, live human selected "2x same-host fix" (AskUserQuestion: which tasks to authorise under RED)
  - reasons: install verification FAILED (testpypi; checks F) · release validation FAILED (stage integrate) · Release Integrate failure · (rest as on autolens_profiling#462)
  - scope: commit/push/PR only; no release; branch does not fix Heart
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2x-same-host

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
