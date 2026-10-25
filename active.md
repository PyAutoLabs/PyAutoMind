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

## pre-release-docs-config
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/261
- issued: 2026-10-25
- status: blocked
- session: codex health/hygiene cleanup
- location: /workspace/scratch/f77499d15f98 (session clones)
- prompt: active/pre_release_docs_config.md
- next: HowToFit #76 and AutoGalaxy #262 merged. Explicitly authorized validation-only AutoFit draft PR #176 obtains missing notebook smoke evidence through existing CI. Keep draft/unmerged until every required exact-head job and notebook check passes; no tests waived.
- repos:
  - autofit_workspace: feature/pre-release-docs-config

- heart-red-override:
  - authorized: 2026-10-25, live human, "Ok do final bits and inprovememtns  and then prm what weve done"; prior "Ok continue i approve" retained for this task #261.
  - reasons: install verification FAILED (testpypi; checks F) · release validation FAILED (stage integrate)
  - scope: commit/push/PR for independently validated HowToFit and autogalaxy_workspace branches; current-turn merge only if every required CI leg passes. AutoFit remains blocked pending notebook validation. No release/rehearsal; this patch does not fix Heart.
- workspace-pr: HowToFit https://github.com/PyAutoLabs/HowToFit/pull/76
- workspace-pr: autogalaxy_workspace https://github.com/PyAutoLabs/autogalaxy_workspace/pull/262
- merged: HowToFit https://github.com/PyAutoLabs/HowToFit/pull/76 @ bfca6a40420004b489b7ba257c415687b09249c2
- merged: autogalaxy_workspace https://github.com/PyAutoLabs/autogalaxy_workspace/pull/262 @ c40228890eabd6eaad599fea3f849026d2cf711d
- workspace-pr: autofit_workspace https://github.com/PyAutoLabs/autofit_workspace/pull/176 (DRAFT; validation only)
- validation-exception: 2026-10-25 live user "Yeah do it" to explicit validation-only draft PR request. Commit/push/draft permitted despite missing local notebook runtime; merge/release prohibited until required evidence passes.

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
