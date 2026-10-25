## likelihood-lifecycle-p2x-node-throughput
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/462
- issued: 2026-10-25
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2x-node-throughput
- prompt: active/likelihood_lifecycle_p2x_node_throughput.md
- epic: likelihood-lifecycle
- next: Opus worker implements the issue #462 plan (row fields, 2a sacct backfill, reference hosts, projected_node_throughput, @3 additive check) → ship_workspace → human /prm. Then the Pulse view task (draft/feature/pyautopulse/likelihood_lifecycle_p2x_throughput_view.md) → 2b.
- heart-red-override:
  - authorized: 2026-10-25, live human, "I authorise work on red and prm" (this task)
  - reasons: install verification FAILED (testpypi; checks F) · release validation FAILED (stage integrate) · PyAutoHeart/workflows/Release Integrate: failure · manifest_drift/checks/workspace checkouts (manifest ↔ disk): red · PyAutoArray interferometer test_interferometer_sparse_operator__mapped_reconstructed_data_dict_matc… · Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×) · Release validation: NOT release_ready — v2026.10.25.1.dev83701 · F: colab gate: finufft (declared by autoarray, absent on Colab, imported)
  - scope: commit/push/PR only; no release; branch does not fix Heart
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2x-node-throughput

## pre-release-docs-config
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/261
- issued: 2026-10-25
- status: workspace-dev
- session: codex health/hygiene cleanup
- location: /workspace/scratch/f77499d15f98 (session clones)
- prompt: active/pre_release_docs_config.md
- next: HowToFit PR #76 and autogalaxy_workspace PR #262 opened after local validation; human requested prm, requires every exact-head CI run/leg green. AutoFit six config mirrors remain locally preserved and blocked on two notebook checks; keep task open and claims intact.
- repos:
  - HowToFit: feature/pre-release-docs-config
  - autofit_workspace: feature/pre-release-docs-config
  - autogalaxy_workspace: feature/pre-release-docs-config

- heart-red-override:
  - authorized: 2026-10-25, live human, "Ok do final bits and inprovememtns  and then prm what weve done"; prior "Ok continue i approve" retained for this task #261.
  - reasons: install verification FAILED (testpypi; checks F) · release validation FAILED (stage integrate)
  - scope: commit/push/PR for independently validated HowToFit and autogalaxy_workspace branches; current-turn merge only if every required CI leg passes. AutoFit remains blocked pending notebook validation. No release/rehearsal; this patch does not fix Heart.
- workspace-pr: HowToFit https://github.com/PyAutoLabs/HowToFit/pull/76
- workspace-pr: autogalaxy_workspace https://github.com/PyAutoLabs/autogalaxy_workspace/pull/262

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
