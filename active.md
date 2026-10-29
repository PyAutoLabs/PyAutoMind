
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## rectangular-28sq-profiling-rows
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/468
- issued: 2026-10-26
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/rectangular-28sq-profiling-rows
- repos:
  - autolens_inference: feature/rectangular-28sq-profiling-rows
- released-claims: autolens_profiling (#470 merged a1a4ccf1), PyAutoPulse (#80 merged 5474e3cb) — branches kept in the worktree until close-out
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/49 OPEN 2026-10-27 (size_match 32/0)
- prompt: active/rectangular_28sq_profiling_rows.md
- epic: likelihood-lifecycle
- heart-red-override: authorized by live human 2026-10-26 "I approve of the override" (this task incl. RAL jobs); reasons + gates recorded at ship
- scope-add: HUMAN 2026-10-26 chose "Yes, small Pulse PR first" (option text: "Same RED override extended to it. Ships before the profiling rows.") — PyAutoPulse one-current-per-key adds regime
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/80 MERGED 2026-10-26 5474e3cb via human /prm (regime in @3 one-current key)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/470 MERGED 2026-10-27 a1a4ccf1 via human /prm (rect28 rows, RAL 413044/413046 8/8); task stays open — NEXT autolens_inference size_match leg (branch has no commits yet); witness gap jax_cpu_dense + light_fixed unmeasured

## mesh-magnification-areas
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/659
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); https://claude.ai/code/session_016nhQ8NkVvJhhqNSibeGcBQ
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/mesh-magnification-areas
- repos:
  - PyAutoArray: feature/mesh-magnification-areas
  - autolens_workspace_test: feature/mesh-magnification-areas
- prompt: active/mesh_magnification_areas.md
- epic: cluster-strong-lensing (Source & Cluster arc phase 4a)
- autonomy: --auto launched by human 2026-10-28; effective supervised → decide-and-flag, ends at PR-open; judge → human /prm

## results-library-p0-integrity
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1734
- issued: 2026-10-28
- epic: results-library (phase 0, shared with hpc-campaign)
- session: Claude Code CLI (Opus 5.5) session_016nhQ8N4RdvbZz9cstLYtNF
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/results-library-p0-integrity
- repos:
  - PyAutoFit: feature/results-library-p0-integrity

## hpc-campaign-p1-status-record
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1735
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/206
- issued: 2026-10-28
- epic: hpc-campaign (phase 1; merges after results-library PR 0a)
- session: Claude Code CLI (Opus 5.5) session_016nhQ8N4RdvbZz9cstLYtNF
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/hpc-campaign-p1-status-record
- repos:
  - PyAutoFit: feature/hpc-campaign-p1-status-record
  - PyAutoNerves: feature/hpc-campaign-p1-status-record

## cosmos-web-ring-intro-visuals
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/168
- issued: 2026-10-29
- session: Codex
- status: library-merged, workspace-pending-release
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/661
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/679
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/809
- release-gate: PyAutoArray
- release-gate: PyAutoGalaxy
- release-gate: PyAutoLens
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/169
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/cosmos-web-ring-intro-visuals
- repos:
  - autolens_assistant: feature/cosmos-web-ring-intro-visuals
  - PyAutoArray: feature/cosmos-web-ring-intro-visuals
  - PyAutoGalaxy: feature/cosmos-web-ring-intro-visuals
  - PyAutoLens: feature/cosmos-web-ring-intro-visuals

- heart-red-override:
  - authorization: "Authorize development-only shipping for #168" (2026-10-29; no merge/release)
  - reason: PyAutoArray: 4 uncommitted source change(s)
  - reason: PyAutoGalaxy: 9 commit(s) behind origin
  - reason: PyAutoLens: 7 commit(s) behind origin
  - validation: Array 2155 passed/69 skipped/4 xfailed; Galaxy 1442 passed/6 skipped; Lens 998 passed/1 xfailed; 58 plotting checks and 24 notebook/greeting checks passed; all 10 notebook cells executed; API audit clean; author visual/diff review. Frozen historical assistant reference module needs its separate September wheels (9 setup errors on current runtime).

- coordination: Human authorized "Allow concurrent plotting work" alongside mesh-magnification-areas; PyAutoArray changes limited to plotting code and tests in a separate worktree.


- merge-checkpoint: 2026-10-29 human authorized merge; Array#661, Galaxy#679, Lens#809 merged after all 11 CI jobs passed and freeze clear. Assistant#169 remains open: wiki-currency symbol audit fails against released 2026.10.26.1, which lacks subplot_imaging_dataset_intro. Retain task/worktree until release and green assistant CI; no release or failed-check bypass.

## r2-pages-function-access
- issue: https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/issues/4
- issued: 2026-10-29
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/r2-pages-function-access
- repos:
  - ECLIPSE_lens_catalogue: feature/r2-pages-function-access
- tier: judge — merge mode: human /prm

## files-experiment-scripts-cleanup
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/662
- issued: 2026-10-29
- session: Claude Code (Opus 5.5) desktop
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/files-experiment-scripts-cleanup
- repos:
  - PyAutoArray: feature/files-experiment-scripts-cleanup
- prompt: active/files_experiment_scripts_import_a_removed_module.md
- tier: glance — auto-merge on green if Witness passes (plan approved by human 2026-10-29)
- coordination: Human authorized concurrent work 2026-10-29 alongside mesh-magnification-areas and cosmos-web-ring-intro-visuals; PyAutoArray change limited to deleting files/ (neither branch touches files/).
