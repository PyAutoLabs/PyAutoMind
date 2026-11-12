
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

## merge-actor-audit
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/606
- issued: 2026-11-12
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (programme lead)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/merge-actor-audit
- prompt: active/autonomy_log_merge_actor_and_random_audit.md
- epic: autonomous-orchestrators (programme M1.4, phase 8)
- decision: human 2026-11-12 "All three as recommended" (actor classes + count rule; seeded 1-in-5 audits; read-by column non-gating) — doctrine edit authorized
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
- repos:
  - PyAutoBrain: feature/merge-actor-audit
  - PyAutoMind: feature/merge-actor-audit

## new-user-guide-visuals
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/838
- issued: 2026-11-12
- session: OpenAI Codex desktop
- status: human-review
- prompt: active/new_user_guide_visuals.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/new-user-guide-visuals
- repos:
  - PyAutoLens: feature/new-user-guide-visuals
  - autolens_workspace: feature/new-user-guide-visuals
  - PyAutoGalaxy: feature/new-user-guide-visuals
  - autogalaxy_workspace: feature/new-user-guide-visuals
- scope: Lens and Galaxy RTD and start_here applied with images; no PRs authorized
- tier: judge — merge mode: human /prm

## start-here-plot-ai
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/647
- issued: 2026-11-12
- status: workspace-dev
- session: OpenAI Codex desktop
- prompt: active/start_here_plot_ai.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/start-here-plot-ai
- repos:
  - autolens_workspace: feature/start-here-plot-ai
- tier: judge — merge mode: human /prm
- next: validated edits; ship-time Heart RED requires development-only override before PR publication

## extra-galaxies-review
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/648
- issued: 2026-11-12
- session: OpenAI Codex desktop; session ID unavailable
- status: library-dev
- prompt: active/extra_galaxies_review.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/extra-galaxies-review
- tier: judge — merge mode: human /prm; do not merge
- coordination: user approved separate documentation worktrees alongside new-user-guide-visuals and start-here-plot-ai; preserve both and verify compatibility
- repos:
  - PyAutoLens: feature/extra-galaxies-review
  - autolens_workspace: feature/extra-galaxies-review
