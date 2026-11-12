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
