
## mesh-magnification-knn-areas
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/665
- issued: 2026-10-29
- session: Claude Code (Opus 5.5)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/mesh-magnification-knn-areas
- repos:
  - PyAutoArray: feature/mesh-magnification-knn-areas
  - autolens_workspace_test: feature/mesh-magnification-knn-areas
- prompt: active/mesh_magnification_exact_quadrature_areas.md
- epic: cluster-strong-lensing (Source & Cluster arc phase 4b); also closes PyAutoArray#609 (planned knn-partial-point-block)
- autonomy: human approved plan 2026-10-29 ("Yeah do it go"); judge → human /prm

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## results-library-p0-integrity
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1734
- issued: 2026-10-28
- epic: results-library (phase 0, shared with hpc-campaign)
- session: Claude Code CLI (Opus 5.5) session_016nhQ8N4RdvbZz9cstLYtNF
- status: library-shipped, awaiting-merge (PR 0a #1736 then stacked PR 0b #1737; #1737 HELD on euclid strict-default decision)
- worktree: /home/jammy/Code/PyAutoLabs-wt/results-library-p0-integrity
- repos:
  - PyAutoFit: feature/results-library-p0-integrity
  - PyAutoFit: feature/results-library-p0b-honest-reads
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1736
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1737
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1736
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1737

## hpc-campaign-p1-status-record
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1735
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/206
- issued: 2026-10-28
- epic: hpc-campaign (phase 1; merges after results-library PR 0a)
- session: Claude Code CLI (Opus 5.5) session_016nhQ8N4RdvbZz9cstLYtNF
- status: library-shipped, awaiting-merge (merge #1738 after #1736; workspace #179 after release)
- worktree: /home/jammy/Code/PyAutoLabs-wt/hpc-campaign-p1-status-record
- repos:
  - PyAutoFit: feature/hpc-campaign-p1-status-record
  - PyAutoNerves: feature/hpc-campaign-p1-status-record
  - autofit_workspace: feature/hpc-campaign-p1-status-record
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/207
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1738
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/179
- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/207
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1738

## r2-pages-function-access
- issue: https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/issues/4
- issued: 2026-10-29
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/r2-pages-function-access
- repos:
  - ECLIPSE_lens_catalogue: feature/r2-pages-function-access
- tier: judge — merge mode: human /prm

## lenstwin-p4a-twin-fit-model
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/810
- issued: 2026-10-29
- session: Claude Code (laptop)
- status: library-shipped (DRAFT, HOLD)
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/811
- worktree: ~/Code/PyAutoLabs-wt/lenstwin-p4a-twin-fit-model
- repos:
  - PyAutoLens: feature/lenstwin-p4a-twin-fit-model
- tier: judge — merge mode: human /prm; HOLD — human 2026-10-29: draft PR, nothing merges until the human lifts it
- coordination: PyAutoLens also claimed by cosmos-web-ring-intro-visuals (Lens #809 merged; claim held for assistant#169); human approved concurrent work 2026-10-29 — claim RELEASED 2026-10-29 (task closed, assistant#169 merged)
