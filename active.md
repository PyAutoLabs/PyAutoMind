
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## power-law-jax-axis
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/663
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/659
- issued: 2026-10-25
- prompt: active/jax_power_law_deflections_exact_unit_vector_transform.md
- status: library-merged, workspace-awaiting-ci
- session: Codex; session ID unavailable
- worktree: /workspace/scratch/e0d55f00a4c5/worktrees/power-law-jax-axis
- repos:
  - autogalaxy_workspace_test: feature/power-law-jax-axis
- coordination: user-requested four mass-profile fixes; sequential edits on isolated branches

- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/663
- library-head: 499827fe23c5804351d936823d1b01e7917527a4
- validation: Python 3.12 full suite 1356 passed, 6 skipped; Heart GREEN score 100; exact-head GitHub Tests/Docs running
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/129 (ready; library merged)
- workspace-head: cd96d90dbf305c8d8fc9ad0fe1cbe94d60388109
- witness: NumPy/eager JAX/JIT regression passes on branch, fails on main; workspace smoke-list entry added
- next: /prm after companion #129 CI run 40240713169 passes; preserve all smoke-list entries
- merge-progress: PyAutoGalaxy#663 confirmed merged 2026-10-25. Workspace smoke-list conflict resolved by a merge commit retaining every main entry; fresh CI in progress.

## multipole-isothermal-guard
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/665
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/661
- issued: 2026-10-25
- prompt: active/power_law_multipole_m1_singular_at_isothermal_slope.md
- status: library-merged, workspace-awaiting-ci
- session: Codex; session ID unavailable
- worktree: /workspace/scratch/e0d55f00a4c5/worktrees/multipole-isothermal-guard
- repos:
  - autogalaxy_workspace_test: feature/multipole-isothermal-guard
- coordination: user-requested four mass-profile fixes; sequential edits on isolated branches

- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/665
- library-head: 9be12cae62318cf27fcfce37059a9cd0b43302e2
- validation: Python 3.12 full suite 1363 passed, 6 skipped; Heart GREEN score 100; exact-head GitHub Tests/Docs running
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/130 (ready; library merged)
- workspace-head: 14bff78a9e6e45804a90d859f9768392f1336bfd
- witness: NumPy/eager JAX/JIT regression passes on branch, fails on main; workspace smoke-list entry added
- next: /prm after companion #130 CI run 40240716788 passes; preserve all smoke-list entries
- merge-progress: PyAutoGalaxy#665 confirmed merged 2026-10-25. Workspace smoke-list conflict resolved by a merge commit retaining every main entry; fresh CI in progress.
