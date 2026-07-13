## pyauto-test-mode-rename
- issue: none — silent no-op cleanup discovered during autofit_workspace smoke tests
- completed: 2026-04-18
- library-pr: https://github.com/PyAutoLabs/PyAutoBuild/pull/46
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/9, https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/3
- notes: Renamed `PYAUTOFIT_TEST_MODE` → `PYAUTO_TEST_MODE` everywhere. The old name was a silent no-op because autoconf only reads `PYAUTO_TEST_MODE`. After rename, Nautilus smoke test dropped from ~60s (full sampling) to ~4s (test mode skipped sampling). Skipped autolens_workspace_test (active worktree conflict with interferometer-mge-gradients task) and z_projects/autolens_assistant/euclid_strong_lens_modeling_pipeline (out of scope).
