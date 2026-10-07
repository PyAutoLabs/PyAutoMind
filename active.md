# Active Tasks

## imshow-origin-lower-overlays
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/565
- discussion: https://github.com/orgs/PyAutoLabs/discussions/14
- user-facing: true
- author: @ClarkGuilty (external)
- issued: 2026-10-07
- session: Claude CLI (Fable 5.1, /community); session ID unavailable
- status: library-merged, pending-release
- repos:
  - PyAutoArray: feature/imshow-origin-lower-overlays (PR #616 MERGED 93961c68, 2026-10-07)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/616
- summary: plot_array (and uniform rectangular inversion) overlays now respect imshow_origin "lower". Record: complete/2026/10/imshow-origin-lower-overlays.md.
- resume: Merged, unreleased. Discussion #14 reply drafted (human approves before posting). After a release carrying #616: post the release note on #14 and mark the reply as the accepted answer, then drop this entry.
- pending-release: PyAutoArray#616 (merged 2026-10-07, unreleased)

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
