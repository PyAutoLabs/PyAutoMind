
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

## heart-dev-scope
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/340
- issued: 2026-11-12
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (programme lead)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/heart-dev-scope
- prompt: active/dev_ship_reason_scope_and_feed_age.md
- epic: autonomous-orchestrators (programme M2.1, phase 9; ruled at M1 gate 2026-11-12)
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
- repos:
  - PyAutoHeart: feature/heart-dev-scope

## lane-fail-closed
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/614
- issued: 2026-11-12
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (programme lead)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/lane-fail-closed
- epic: autonomous-orchestrators (programme M2.3 + AUTONOMY record of all M2 rulings, phase 9; ruled at M1 gate 2026-11-12)
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
- repos:
  - PyAutoBrain: feature/lane-fail-closed
  - PyAutoMind: feature/lane-fail-closed

## release-rehearsed-shas
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/337
- issued: 2026-11-12
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (programme lead)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/release-rehearsed-shas
- prompt: active/release_builds_rehearsed_shas.md
- epic: autonomous-orchestrators (programme M2.4, phase 9; ruled at M1 gate 2026-11-12)
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
- repos:
  - PyAutoHands: feature/release-rehearsed-shas

## cortex-ledger-merge-pages
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/90
- issued: 2026-11-13
- session: claude-code desktop (WSL), ~/Science session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/cortex-ledger-merge-pages
- prompt: active/cortex_ledger_merge_pages.md
- tier: judge — merge mode: human /prm
- repos:
  - PyAutoCortex: feature/cortex-ledger-merge-pages
- pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/91
- heart-red-override:
  - authorization: live human, 2026-11-13, choosing "Override both (Recommended)" for (a) PyAutoCortex#90 ledger-merge Pages fix and (b) the STATE.md table render in PyAutoBrain: "Push and open both PRs, recorded in the four override sinks. CI must pass; merging stays with your /prm."
  - heart-red: PyAutoNerves: 4 commit(s) behind origin; PyAutoFit: 2 commit(s) behind origin; PyAutoArray: 4 commit(s) behind origin; PyAutoGalaxy: on branch feature/galaxy-guide-rebalance (not main); PyAutoGalaxy: 1 uncommitted source change(s); PyAutoLens: 1 uncommitted source change(s); PyAutoLens: 45 commit(s) behind origin; PyAutoCTI: 4 commit(s) behind origin; install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); manifest drift: tenant firewall (organ code) — 40 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: workspace checkouts (manifest ↔ disk) — 3 mismatch(es) vs PyAutoMind/repos.yaml; PyAutoArray: open PR 9d old
  - gates: PyAutoCortex tests 105 passed (tests/); workflow YAML parses; smoke n/a (CI workflow change only); review: in-session diff review (one step gains a second gh workflow run dispatch mirroring dashboard_refresh.yml). None of the RED reasons are in PyAutoCortex.

## cortex-state-md-tables
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/618
- issued: 2026-11-13
- session: claude-code desktop (WSL), ~/Science session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/cortex-state-md-tables
- prompt: active/cortex_state_md_tables.md
- tier: judge — merge mode: human /prm
- note: shares PyAutoBrain with lane-fail-closed (disjoint files: agents/conductors/cortex/ only); parallel approved by the human 2026-11-13
- repos:
  - PyAutoBrain: feature/cortex-state-md-tables
- pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/619
- heart-red-override:
  - authorization: live human, 2026-11-13, choosing "Override both (Recommended)" for (a) PyAutoCortex#90 ledger-merge Pages fix and (b) the STATE.md table render in PyAutoBrain: "Push and open both PRs, recorded in the four override sinks. CI must pass; merging stays with your /prm."
  - heart-red: PyAutoNerves: 4 commit(s) behind origin; PyAutoFit: 2 commit(s) behind origin; PyAutoArray: 4 commit(s) behind origin; PyAutoGalaxy: on branch feature/galaxy-guide-rebalance (not main); PyAutoGalaxy: 1 uncommitted source change(s); PyAutoLens: 1 uncommitted source change(s); PyAutoLens: 45 commit(s) behind origin; PyAutoCTI: 4 commit(s) behind origin; install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); manifest drift: tenant firewall (organ code) — 40 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: workspace checkouts (manifest ↔ disk) — 3 mismatch(es) vs PyAutoMind/repos.yaml; PyAutoArray: open PR 9d old
  - gates: cortex conductor tests 104 passed (tests/test_cortex_conductor.py; rerun by the orchestrating session); smoke n/a (Brain organ renderer, no library code); review: in-session review of the diff and a preview rendered from the real ledgers. None of the RED reasons are in PyAutoBrain.
