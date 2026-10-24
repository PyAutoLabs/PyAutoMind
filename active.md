## finufft-cpu-nufft-backend
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/654
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/finufft-cpu-nufft-backend
- prompt: active/finufft_cpu_nufft_backend.md
- user-facing: true
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/655 (finufft CPU NUFFT)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1715 (Fitness.prepare_for_fork warm-up; ROOT CAUSE = numba first-imported in forked workers, NOT JAX — see issue correction comment)
- heart-ack: YELLOW acknowledged by human 2026-10-24 (manifest drift x4, Hands/Mind PRs 7d old, no rehearsal for current source)
- next: human /prm 655 + 1715; phase 2 E2E running on RAL (scratch aris_cpu_check_20261024/e2e, mass_1 job 412868) → Aris Slack handoff (his scripts need the source_pix_0 reload via NumPy + preprocessing use_jax=False; copies in session scratch aris_e2e/slam)
- repos:
  - PyAutoArray: feature/finufft-cpu-nufft-backend
  - PyAutoFit: feature/finufft-cpu-nufft-backend

## likelihood-lifecycle-p2a-imaging-campaign
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/456
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-imaging-campaign
- prompt: active/likelihood_lifecycle_p2a_imaging_campaign.md
- epic: likelihood-lifecycle
- next: PR A (standard size + parity.json writer + submits; Opus worker → independent review → ship) → batch 0 timing (human go) → batch 1 (human go) → PR B
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
