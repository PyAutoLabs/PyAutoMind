# Active Tasks

## imshow-origin-lower-overlays
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/565
- discussion: https://github.com/orgs/PyAutoLabs/discussions/14
- user-facing: true
- author: @ClarkGuilty (external)
- issued: 2026-10-07
- prompt: active/imshow_origin_lower_overlays.md
- session: Claude CLI (Fable 5.1, /community → /start_dev); session ID unavailable
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/imshow-origin-lower-overlays
- repos:
  - PyAutoArray: feature/imshow-origin-lower-overlays
- summary: plot_array vector overlays ignore imshow_origin "lower" (raster mirrored, overlays not). Fix: reflect overlay y about the extent midpoint, regression test from the Discussion.
- resume: Plan approved 2026-10-07 and posted on #565. Next: implement in the worktree (Opus), ship_library, glance auto-merge on green, then reply on Discussion #14 and mark answer once released.

## scribbler-wave2-radial-panels-regrid
- discussion: https://github.com/orgs/PyAutoLabs/discussions/23
- user-facing: true
- author: @samlange04 (external)
- issued: 2026-10-07
- session: Claude CLI (Fable 5.1, /community); session ID unavailable
- status: library-merged, pending-release
- repos:
  - PyAutoGalaxy: samlange04:feature/scribbler-radial-panels-regrid (PR #641 MERGED 12c1cafaa, 2026-10-07)
  - PyAutoLens: feature/scribbler-regrid-reexport (PR #770 MERGED, 2026-10-07)
  - autolens_workspace: samlange04:feature/scribbler-radial-panels-regrid (DRAFT PR #583, fixup f81a3577)
  - autogalaxy_workspace: samlange04:feature/scribbler-radial-panels-regrid (DRAFT PR #254, no changes needed)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/641
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/770
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/583
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/254
- summary: Wave 2 of the Scribbler proposal (radial-subtracted side-by-side panels, cross-grid mask regrid, white/black brushes, arcsinh default). Wave 1 (#635, docs #579/#251) is released in autogalaxy 2026.10.2.1.
- resume: Library half merged (PyAutoGalaxy#641, PyAutoLens#770) on 2026-10-07, unreleased. Next: a release carrying both, then approve fork CI on autolens_workspace#583 / autogalaxy_workspace#254, mark ready, human /prm. Workspace prose describes white/black brushes, so neither docs PR may merge before the release.
- pending-release: PyAutoGalaxy#641, PyAutoLens#770 (merged 2026-10-07, unreleased)

## profiling-browser-completion
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/21
- issued: 2026-10-07
- prompt: active/profiling_browser_completion.md
- session: Codex local
- status: workspace-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-browser-completion
- repos:
  - PyAutoPulse: feature/profiling-browser-completion
- summary: Approved Phase C setup-browser parity, preserving captured provenance and scientific qualifications.
- coordination: Human explicitly said "Coordinate in parallel" with dashboard-freshness (#486). This branch owns setup_browser.* and browser tests; freshness owns board/ingest/workflows. Re-render generated dashboard from merged sources when reconciling.
- resume: Phase C PR #23 open at 3cfb95b; 192 Python tests and expanded Chromium pass; independent Sol CLEAN. Next human /prm when CI green; reconcile generated board if freshness branch merges first.
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/23
- heart-yellow-reasons: manifest drift: shared-standards blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml
- heart-stale-reasons: release validation stale: source moved since rehearsal (PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens)
- heart-ack: Human's "I acknowledge, go" in this session covers the same exact reason set, repeated unchanged before Phase C shipping. Development PR only; human /prm for merge.
