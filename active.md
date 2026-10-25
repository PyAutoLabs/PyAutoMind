
## likelihood-lifecycle-p2x-pulse-view
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/76
- issued: 2026-10-25
- session: claude-code (local CLI, Opus 5.5)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2x-pulse-view
- prompt: active/likelihood_lifecycle_p2x_throughput_view.md
- epic: likelihood-lifecycle
- next: Opus worker implements → ship_library → human /prm → 2b. Heart door YELLOW after release 2026.10.25.1 (Heart Health dispatched 21:40 UTC refreshed the feed).
- repos:
  - PyAutoPulse: feature/likelihood-lifecycle-p2x-pulse-view

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## mass-sheet-jax
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/658
- issued: 2026-10-25
- prompt: active/mass_sheet_deflections_fail_under_jax.md
- status: library-shipped, awaiting-merge
- session: Codex; session ID unavailable
- worktree: /workspace/scratch/e0d55f00a4c5/worktrees/mass-sheet-jax
- repos:
  - PyAutoGalaxy: feature/mass-sheet-jax
  - autogalaxy_workspace_test: feature/mass-sheet-jax
- coordination: user-requested four mass-profile fixes; sequential edits on isolated branches

- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/662
- library-head: 36ec41b232d827f5342831f4d62939a9e7b4b64f
- validation: Python 3.12 full suite 1356 passed, 6 skipped; Heart GREEN score 100; exact-head GitHub Tests/Docs running
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/128 (draft, library dependency first)
- workspace-head: 19605d9069128d47b85627f842859fc6d5252393
- witness: NumPy/eager JAX/JIT regression passes on branch, fails on main; workspace smoke-list entry added
- next: human /prm after required CI is green; then validate and merge companion workspace regression where present

## power-law-jax-axis
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/659
- issued: 2026-10-25
- prompt: active/jax_power_law_deflections_exact_unit_vector_transform.md
- status: library-shipped, awaiting-merge
- session: Codex; session ID unavailable
- worktree: /workspace/scratch/e0d55f00a4c5/worktrees/power-law-jax-axis
- repos:
  - PyAutoGalaxy: feature/power-law-jax-axis
  - autogalaxy_workspace_test: feature/power-law-jax-axis
- coordination: user-requested four mass-profile fixes; sequential edits on isolated branches

- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/663
- library-head: 499827fe23c5804351d936823d1b01e7917527a4
- validation: Python 3.12 full suite 1356 passed, 6 skipped; Heart GREEN score 100; exact-head GitHub Tests/Docs running
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/129 (draft, library dependency first)
- workspace-head: b42a011a6eeebaa68a05d32671a5c7672f77d022
- witness: NumPy/eager JAX/JIT regression passes on branch, fails on main; workspace smoke-list entry added
- next: human /prm after required CI is green; then validate and merge companion workspace regression where present

## sersic-core-sph-ml
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/660
- issued: 2026-10-25
- prompt: active/sersiccoresph_has_no_mass_to_light_ratio.md
- status: library-shipped, awaiting-merge
- session: Codex; session ID unavailable
- worktree: /workspace/scratch/e0d55f00a4c5/worktrees/sersic-core-sph-ml
- repos:
  - PyAutoGalaxy: feature/sersic-core-sph-ml
- coordination: user-requested four mass-profile fixes; sequential edits on isolated branches

- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/664
- library-head: 0fee6daf0e299539d43bdfa185200b76436ef2a3
- validation: Python 3.12 full suite 1360 passed, 6 skipped; Heart GREEN score 100; exact-head GitHub Tests/Docs running
- next: human /prm after required CI is green; then validate and merge companion workspace regression where present

## multipole-isothermal-guard
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/661
- issued: 2026-10-25
- prompt: active/power_law_multipole_m1_singular_at_isothermal_slope.md
- status: library-shipped, awaiting-merge
- session: Codex; session ID unavailable
- worktree: /workspace/scratch/e0d55f00a4c5/worktrees/multipole-isothermal-guard
- repos:
  - PyAutoGalaxy: feature/multipole-isothermal-guard
  - autogalaxy_workspace_test: feature/multipole-isothermal-guard
- coordination: user-requested four mass-profile fixes; sequential edits on isolated branches

- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/665
- library-head: 9be12cae62318cf27fcfce37059a9cd0b43302e2
- validation: Python 3.12 full suite 1363 passed, 6 skipped; Heart GREEN score 100; exact-head GitHub Tests/Docs running
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/130 (draft, library dependency first)
- workspace-head: 7888d4905371bf60547557e5c1d9334b5133dd40
- witness: NumPy/eager JAX/JIT regression passes on branch, fails on main; workspace smoke-list entry added
- next: human /prm after required CI is green; then validate and merge companion workspace regression where present
