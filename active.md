
## autonomous-orchestrators-p4c
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/574
- issued: 2026-11-04
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: human-ops (pilot run; no worktree — briefs land in PyAutoMind/batches/ by the human)
- prompt: active/autonomous_orchestrators_p4c_pilot_run.md
- epic: autonomous-orchestrators (phase 4c of 4a–4c)
- pre-check: open shadow tick on system python3.10, minimal env — 6 notify proposals, 0 spawns (2026-11-04)
- tier: judge — merge mode: human /prm

## pyautolens-ii-case-studies
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/147
- issued: 2026-11-12
- session: OpenAI Codex desktop
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/pyautolens-ii-case-studies
- repos:
  - autolens_workspace_developer: feature/pyautolens-ii-case-studies
- prompt: active/pyautolens_ii_case_studies.md
- coordination: human approved PyAutoLens/paper_jax/paper.md-only edits alongside magnification-maps-wiring; no library code changes
- next: validate JWST PSF/noise and export calibrated ALMA visibilities, then joint gradient check and bounded pilots
- tier: judge — merge mode: human /prm

## website-lensing-intro
- issue: https://github.com/Jammy2211/Jammy2211.github.io/issues/1
- issued: 2026-11-12
- session: OpenAI Codex desktop
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/scratch/website-lensing-intro
- repos:
  - Jammy2211.github.io: feature/website-lensing-intro
- prompt: active/website_lensing_intro.md
- tier: judge — merge mode: human /prm
- scope: personal static website, outside organism registry; no library/workspace runtime changes

## three-autos-public-framing
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/832
- issued: 2026-11-12
- session: Codex desktop; session ID unavailable
- status: human-review (Lens/Galaxy merged; PyAutoFit copy awaiting discussion)
- prompt: active/three_autos_public_framing.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/three-autos-public-framing
- tier: judge — merge mode: human /prm
- repos:
  - PyAutoFit: feature/three-autos-public-framing

- validation: six-file scope and rendering checked; pre-existing Galaxy metadata warning reproduced on base; see prompt checkpoint
- preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/three_autos_public_framing_2026-11-12/revised_introductions.html

- heart-red-override:
  authorization: live user approved development-only override for #832, commit/push/open PRs; follow-up explicitly "Open PRs and merge Lens/Galaxy after checks pass". No release.
  reasons: ["PyAutoLens: 1 uncommitted source change(s)", "PyAutoLens: 6 commit(s) behind origin", "install verification FAILED (testpypi; checks F)", "release validation FAILED (stage integrate)"]
  gates: four-file scope, exact titles, CommonMark/Sphinx excerpt rendering, diff checks and author review pass; runtime tests/smoke not applicable to prose-only edits; required CI must pass before merge.

- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/833
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/703
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/833
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/703

- merged: PyAutoLens#833 fdf569cd786bcdd78566dc3dee54fff63dc2873c; PyAutoGalaxy#703 8e68a6a7edfd65692e34b9bf8072b7c19f387b92
- merge-validation: all four jobs (Docs, Python 3.12, Python 3.13, no-JAX) passed per exact PR head; freeze clear, merge states CLEAN; explicit live human merge authority
- retained-repos: PyAutoLens and PyAutoGalaxy merged worktrees retained within the bundle; PyAutoFit still dirty and uncommitted. No release performed.

## homepage-flow-polish
- issue: https://github.com/Jammy2211/Jammy2211.github.io/issues/3
- issued: 2026-11-12
- status: awaiting-merge
- workspace-pr: https://github.com/Jammy2211/Jammy2211.github.io/pull/4
- worktree: /home/jammy/Code/PyAutoLabs/scratch/website-lensing-intro
- repos:
  - Jammy2211.github.io: feature/homepage-flow-polish
- prompt: active/homepage_flow_polish.md
- tier: judge — merge mode: human /prm

## start-here-plot-ai
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/647
- issued: 2026-11-12
- status: awaiting-merge
- session: OpenAI Codex desktop
- prompt: active/start_here_plot_ai.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/start-here-plot-ai
- repos:
  - autolens_workspace: feature/start-here-plot-ai
- tier: judge — merge mode: human /prm
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/651
- commit: 8087a94e174ae9dbc82bd45ef630e60be2b535ed
- next: human /prm after CI green
- heart-red-override:
  authorization: "new user guide updates merged so work those in and then get this stuff in"
  reasons: ["PyAutoNerves: 2 commit(s) behind origin", "PyAutoArray: 2 commit(s) behind origin", "PyAutoGalaxy: 4 commit(s) behind origin", "PyAutoLens: on branch feature/extra-galaxies-review (not main)", "PyAutoLens: 2 uncommitted source change(s)", "PyAutoCTI: 2 commit(s) behind origin", "install verification FAILED (testpypi; checks F)", "release validation FAILED (stage integrate)"]
  gates: full regenerated notebook passed all 13 code cells; 42 script smokes passed; 2 notebook smokes passed; author review and diff check passed; no release or merge authority inferred

- heart-red-override:
  authorization: "Yes, override Heart RED for #838 and go ahead with the commits, pushes and all four PRs, including the images and start_here notebooks. Don't merge yet."
  reasons: ["PyAutoNerves: 2 commit(s) behind origin", "PyAutoArray: 2 commit(s) behind origin", "PyAutoGalaxy: 4 commit(s) behind origin", "PyAutoLens: on branch feature/los-halos-review (not main)", "PyAutoLens: 2 uncommitted source change(s)", "PyAutoCTI: 2 commit(s) behind origin", "install verification FAILED (testpypi; checks F)", "release validation FAILED (stage integrate)"]
  gates: Focused Sphinx builds pass; notebook schema, code and metadata parity pass; image parity and diff checks pass; human editorial review approved. No runtime code changed; workspace smoke paths excluded by no_smoke_relevant_changes. Full numerical suites not run locally.

- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/839
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/705
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/649
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/275

## premise-lane-checks
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/608
- issued: 2026-11-12
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (programme lead)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/premise-lane-checks
- prompt: active/pre_dispatch_premise_and_lane_checks.md
- epic: autonomous-orchestrators (programme M1.3 slices 1–2, phase 8; slice 3 = M2.3)
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
- repos:
  - PyAutoBrain: feature/premise-lane-checks
  - PyAutoMind: feature/premise-lane-checks

## dev-metrics-boards
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/338
- issued: 2026-11-12
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (programme lead)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/dev-metrics-boards
- prompt: active/dev_metrics_trends_on_boards.md
- epic: autonomous-orchestrators (programme M1 side lane; re-check SIG-2/SIG-3 first)
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
- repos:
  - PyAutoHeart: feature/dev-metrics-boards
