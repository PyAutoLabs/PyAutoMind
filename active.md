## likelihood-lifecycle-p2x-node-throughput
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/462
- issued: 2026-10-25
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2x-node-throughput
- prompt: active/likelihood_lifecycle_p2x_node_throughput.md
- epic: likelihood-lifecycle
- next: PR #463 OPEN (5 commits 85c4f1ea..9c167d59; @3 additive, no bump; 50/55 current runtime records projected). NEXT: lint green → HUMAN fresh /prm (RED-override merge grant expired with the turn) → close #462 → Pulse view task draft/feature/pyautopulse/likelihood_lifecycle_p2x_throughput_view.md → 2b.
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/463
- heart-red-override:
  - authorized: 2026-10-25, live human, "I authorise work on red and prm" (this task)
  - reasons: install verification FAILED (testpypi; checks F) · release validation FAILED (stage integrate) · PyAutoHeart/workflows/Release Integrate: failure · manifest_drift/checks/workspace checkouts (manifest ↔ disk): red · PyAutoArray interferometer test_interferometer_sparse_operator__mapped_reconstructed_data_dict_matc… · Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×) · Release validation: NOT release_ready — v2026.10.25.1.dev83701 · F: colab gate: finufft (declared by autoarray, absent on Colab, imported)
  - scope: commit/push/PR only; no release; branch does not fix Heart
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2x-node-throughput

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
