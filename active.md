
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

## start-here-intro-polish
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/834
- issued: 2026-11-12
- session: Codex desktop; session ID unavailable
- status: pr-open, awaiting-human-merge
- prompt: active/start_here_intro_polish.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/start-here-intro-polish
- tier: judge — text approved; PRs authorized; do not merge
- repos:
  - PyAutoLens: feature/start-here-intro-polish
  - PyAutoGalaxy: feature/start-here-intro-polish
  - autolens_workspace: feature/start-here-intro-polish
  - autogalaxy_workspace: feature/start-here-intro-polish

- heart-red-override:
  authorization: "Yes, override Heart RED for #834 and go ahead with the commits, pushes and all four PRs, including the start_here notebooks. Don't merge yet."
  reasons: ["PyAutoGalaxy: on branch feature/start-here-intro-polish (not main)", "PyAutoGalaxy: 1 uncommitted source change(s)", "PyAutoLens: on branch feature/start-here-intro-polish (not main)", "PyAutoLens: 2 uncommitted source change(s)", "PyAutoLens: 2 commit(s) behind origin", "install verification FAILED (testpypi; checks F)", "release validation FAILED (stage integrate)"]
  gates: focused Sphinx builds, notebook regeneration/schema validation, unchanged executable AST/code cells/metadata, rendered links, diff checks and human text review passed; numerical suites not run for prose-only scope
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/836
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/704
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/644
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/274

## prompt-sync-detached-push
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/556
- issued: 2026-11-12
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (programme lead)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/prompt-sync-detached-push
- prompt: active/prompt_sync_detached_push_target.md
- epic: autonomous-orchestrators (programme M1 side fix, from M1.2 follow-up item 2)
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/557
- heart-red-override:
  authorization: live human 2026-11-12 "Override + merge on green" (programme session); https://github.com/PyAutoLabs/PyAutoMind/issues/556
  reasons: "PyAutoGalaxy: on branch feature/start-here-intro-polish (not main)"; "PyAutoGalaxy: 1 uncommitted source change(s)"; "PyAutoLens: on branch feature/start-here-intro-polish (not main)"; "PyAutoLens: 2 uncommitted source change(s)"; "PyAutoLens: 2 commit(s) behind origin"; "install verification FAILED (testpypi; checks F)"; "release validation FAILED (stage integrate)"
  gates: Mind suite 760 passed; independent review CLEAN; smoke n/a
- repos:
  - PyAutoMind: feature/prompt-sync-detached-push

## los-halos-review
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/645
- issued: 2026-11-12
- session: OpenAI Codex desktop; session ID unavailable
- status: library-dev
- prompt: active/los_halos_review.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/los-halos-review
- tier: judge — merge mode: human /prm; do not merge
- coordination: user explicitly approved separate documentation worktrees alongside start-here-intro-polish; preserve its introductions and verify merge compatibility
- repos:
  - PyAutoLens: feature/los-halos-review
  - autolens_workspace: feature/los-halos-review
