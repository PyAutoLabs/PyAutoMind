Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/661
Issued: 2026-11-12

# Features overview polish
Consequence: judge
Targets: @PyAutoLens @PyAutoGalaxy @autolens_workspace @autogalaxy_workspace

## Original request
I like the gallery at the top. Apply this to both RTD Features pages and the main start_here notebooks, using the new images. Open the PRs for review, don't merge yet. Point Sources belongs on the new user guide, as does interferometry I guess, they are more datasets someone chooses rather than features. But I think they belong in both, but I think their imafges coudl go in the other guide too? Overall I think this is goood

I guess just make sure the features page doesnt feel like its repeating the guide where users do those selections

great

## Approved plan
- Gallery-first Features pages with modelling capabilities first: pixelization, MGE and dark-matter tools for Lens; galaxy structure tools for Galaxy. Short grouped descriptions and expandable complete feature directories.
- Preserve 68 Lens +21 Galaxy feature intro links and scientific use cases; pixelization routes to start_here, not source_science. Remove model.info graphs, solver-panel sequences and Array2D group figure from overview only.
- Reuse six approved AI illustration drafts. Place dataset-choice pictures in New User Guide cards: Lens Point Sources, Interferometry, Data Cubes and Multi-band; Galaxy Interferometry and Multi-band. Features retains short capability descriptions, avoiding repeated setup selection.
- Apply same feature-listing content to canonical root start_here.py, regenerate notebooks, synchronize rendered Markdown prose preserving executable walkthrough and output. Detailed teaching guides unchanged.
- Validate source AST/code-cell parity, notebook/Markdown links and asset parity, Sphinx, responsive gallery, navigator and compatibility with #658.
- Four PRs for review, no merge or release.

Tier: judge — merge mode: human /prm
Coordination: reuse live approval to work separately alongside #658; preserve its README/images/new-user-guide changes and check combination.

## Applied checkpoint — 2026-11-12
Four repositories staged on feature/features-overview-polish; no source commits or PRs yet. Passed: both focused Sphinx builds, notebook schema and executable parity, 89 feature intro links, asset parity, navigator/search-memory/size checks, browser galleries and #658 patch compatibility. Applied preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/features_overview_polish_20261112/applied/index.html. Heart RED; task-specific development-only override #661 pending. PR bodies: organs/PyAutoMind/tmp/features_overview_polish/*_pr.md. Lens multi-wavelength artwork appears in expanded Features gallery; #658 owns the new Multi-band guide card, avoiding duplicate insertion.

## Shipped for review — 2026-11-12
Live authorization: “Approve development-only override for #661”. All four PRs open, no merge or release.
- PyAutoLens: https://github.com/PyAutoLabs/PyAutoLens/pull/855
- PyAutoGalaxy: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/713
- autolens_workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/663
- autogalaxy_workspace: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/280
