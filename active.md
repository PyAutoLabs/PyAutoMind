
## chameleon-analytic-potential
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/682
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session
- status: library-shipped, awaiting-merge (workspace PR also open; /prm library first)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/683
- heart-ack: release validation stale: source moved since rehearsal (human ack 2026-10-30)
- worktree: ~/Code/PyAutoLabs-wt/chameleon-analytic-potential
- repos:
  - PyAutoGalaxy: feature/chameleon-analytic-potential
  - autolens_workspace_test: feature/chameleon-analytic-potential
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/350
- prompt: active/chameleon_potential_inconsistent_with_deflections.md
- tier: judge — merge mode: human /prm (decision-taken: docstring follows code, parametrisation unchanged)

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## r2-pages-function-access
- issue: https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/issues/4
- issued: 2026-10-29
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/r2-pages-function-access
- repos:
  - ECLIPSE_lens_catalogue: feature/r2-pages-function-access
- tier: judge — merge mode: human /prm

## pixelization-mesh-mag-docs
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/605
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session
- status: blocked — awaiting library fix draft/bug/autoarray/adaptive_rectangular_mesh_grid_is_uniform_overlay.md (human 2026-10-30: library first); WIP commit 7c30f74f local, findings on #605
- worktree: ~/Code/PyAutoLabs-wt/pixelization-mesh-mag-docs
- repos:
  - autolens_workspace: feature/pixelization-mesh-mag-docs
- prompt: active/pixelization_source_science_py_document_mesh_mag.md
- epic: cluster-strong-lensing (phase 4e)
- tier: judge — merge mode: human /prm (merge with/after release carrying PyAutoArray#664/#666)

## results-library-p1-index
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1739
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/results-library-p1-index
- repos:
  - PyAutoFit: feature/results-library-p1-index
- prompt: active/results_library_p1_index.md
- epic: results-library (phase 1)
- concurrency: ruling F11 — shares PyAutoFit with hpc-campaign-p2-campaign-core; owns autofit/results/, aggregator/, status/identity.py, ResultState in states.py, identity hook
- tier: judge — merge mode: human /prm

## hpc-campaign-p2-campaign-core
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1740
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session (background fork)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/hpc-campaign-p2-campaign-core
- repos:
  - PyAutoFit: feature/hpc-campaign-p2-campaign-core
- prompt: active/hpc_campaign_p2_campaign_core.md
- epic: hpc-campaign (phase 2)
- concurrency: ruling F11 — shares PyAutoFit with results-library-p1-index; owns autofit/campaign/ only
- tier: judge — merge mode: human /prm
