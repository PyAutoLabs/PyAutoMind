
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

## likelihood-lifecycle-p2d-galaxy-group
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/473
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2d-galaxy-group
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2d-galaxy-group
- prompt: active/likelihood_lifecycle_p2d_multi_galaxy_group_campaign.md
- epic: likelihood-lifecycle
- autonomy: --auto (supervised → decide-and-flag; ends at a DRAFT PR for human review)
- parallel-claim: HUMAN 2026-10-28 "also do the work to set up the other dataset types" — parallel worktree stacked on #471 (80bbb028)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"

## likelihood-lifecycle-p2e-cluster
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/474
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/478 DRAFT (2bf2f53a) — D1–D6 await human
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2e-cluster
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2e-cluster
- prompt: active/likelihood_lifecycle_p2e_cluster_campaign.md
- epic: likelihood-lifecycle
- autonomy: --auto (supervised → decide-and-flag; ends at a DRAFT PR for human review)
- parallel-claim: HUMAN 2026-10-28 "also do the work to set up the other dataset types" — parallel worktree stacked on #471 (80bbb028)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"

## likelihood-lifecycle-p2f-dataset-datacube
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/475
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2f-dataset-datacube
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2f-dataset-datacube
- prompt: active/likelihood_lifecycle_p2f_multi_dataset_datacube_campaign.md
- epic: likelihood-lifecycle
- autonomy: --auto (supervised → decide-and-flag; ends at a DRAFT PR for human review)
- parallel-claim: HUMAN 2026-10-28 "also do the work to set up the other dataset types" — parallel worktree stacked on #471 (80bbb028)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"

## likelihood-lifecycle-p2g-weak
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/476
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/477 DRAFT (7f7e7e8f) — D1–D10 await human
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2g-weak
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2g-weak
- prompt: active/likelihood_lifecycle_p2g_weak_campaign.md
- epic: likelihood-lifecycle
- autonomy: --auto (supervised → decide-and-flag; ends at a DRAFT PR for human review)
- parallel-claim: HUMAN 2026-10-28 "also do the work to set up the other dataset types" — parallel worktree stacked on #471 (80bbb028)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"

## likelihood-lifecycle-p2c-point-source
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/472
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2c-point-source
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2c-point-source
- prompt: active/likelihood_lifecycle_p2c_point_source_campaign.md
- epic: likelihood-lifecycle
- autonomy: --auto (supervised → decide-and-flag, ends at PR-open; judge → human /prm)
- parallel-claim: HUMAN 2026-10-28 "yeah do it, run in auto mode" — parallel worktree beside 2b, stacked on #471 (80bbb028); disjoint files except regenerated catalogue/coverage
- batch-go: HUMAN 2026-10-28 "yeah do it" = go for the 2c RAL batch (ral CPU + A100); never touch 2b 413161/413191
- batch0: submit launched detached 2026-10-28 from 2f98e01a (RAL scratch/p2c_submit.sh → p2c_submit.log, marker P2CSUBMITDONE); checkout profiling/autolens_profiling_p2c

## likelihood-lifecycle-p2b-interferometer
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/469
- issued: 2026-10-26
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2b-interferometer
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2b-interferometer
- prompt: active/likelihood_lifecycle_p2b_interferometer_campaign.md
- epic: likelihood-lifecycle
- heart-red-override: live human 2026-10-26 "Yes, authorise for 2b" (PRs + planned RAL batches)
- batch-go: HUMAN 2026-10-27 "do the next tasks to the point interferometry is hopefully running" = go for batch 0
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/471 OPEN 2026-10-27 (PR A, dff89226; Heart GREEN; judge → human /prm)
- batch0: chained on RAL 2026-10-27 (scratch/p2b_batch0_submit.log; CPU 0-13 + refs 0-1 on ral, A100 0-9%2) from branch head dff89226

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

## cortex-birth
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/545
- issued: 2026-10-29
- session: Claude Code (Opus 5.5); session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/cortex-birth
- repos:
  - PyAutoBrain: feature/cortex-birth
  - PyAutoCortex: feature/cortex-birth
- prompt: active/cortex_birth.md
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/546 OPEN 2026-10-29; companion https://github.com/PyAutoLabs/PyAutoCortex/pull/79 OPEN (merge first) — tier judge → human /prm
- heart-red-override:
  - authorized: live human 2026-10-29 "I authorize development only heart override" (PyAutoBrain#545); development ship only; no merge/release/CI bypass
  - red-reasons: PyAutoArray: 4 uncommitted source change(s); PyAutoGalaxy: 9 commit(s) behind origin; PyAutoLens: 7 commit(s) behind origin; release validation incomplete: no rehearsal for current source; release push credential check stale (pyautolabs-bot, 49h old)
  - gates: Brain cortex conductor tests 80 passed (3 skip vs Cortex main); Cortex 70 tests + check OK; smoke n/a; independent review FINDINGS, all addressed
- open-question: development/ births' ral_root (RAL development/ vs active/) — asked on #545
