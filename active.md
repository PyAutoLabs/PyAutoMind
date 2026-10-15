

## adaptsplit-logdet-backend-parity
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/627
- issued: 2026-10-15
- prompt: active/adaptsplit_regularization_log_det_differs_betwee.md
- session: Claude Code CLI (Fable 5.1); session 3e3dea38; launched --auto
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/631
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/631
- decision: human chose (b) 'Delaunay only (Recommended by review)' on 2026-10-15 (https://github.com/PyAutoLabs/PyAutoArray/issues/627#issuecomment-6200058449); un-parked
- worktree: ~/Code/PyAutoLabs-wt/adaptsplit-logdet-backend-parity
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 3e3dea38, AskUserQuestion answer 'Yes, override for development (Recommended)' (evening launch, three PyAutoArray Aris prompts)
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoMind/workflows/Lifecycle Drift: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready"; "[red] Worktree drift"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red" (as listed on PyAutoArray#626)
  - permitted: commit, push, PR-open; merge separate
- repos:
  - PyAutoArray: feature/adaptsplit-logdet-backend-parity

## search-ext-b5c-family
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/14
- issued: 2026-10-15
- prompt: active/search_ext_b5c_second_model_family.md
- status: workspace-dev (stage 1: protocol, exact references, pilot manifest + pilot submit; B5c-2 = freeze + scored wave)
- session: Claude Code CLI (Fable 5.1); session 6ffb59e9; launched --auto 2026-10-15 night (claim released by ral-category-paths-phase2)
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b5c-family
- repos:
  - autofit_inference: feature/search-ext-b5c-family
  - PyAutoInsight: feature/search-ext-b5c-family
  - PyAutoCortex: feature/search-ext-b5c-family
- classification: research (autofit_inference primary, PyAutoInsight; PyAutoCortex ledger lines by the architect), Consequence judge, Autonomy supervised; Feature Agent: split-into-phases — #14 scopes stage 1 (protocol, references, pilot manifest + submit), scoring/freeze/scored wave = B5c-2
- suggested-branch: feature/search-ext-b5c-family
- epic: search-extensibility
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 6ffb59e9, AskUserQuestion answer 'Both, override for development (Recommended)' (third grant, night launch)
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready"; "[red] Worktree drift"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red"
  - permitted: commit, push, PR-open; merge separate
