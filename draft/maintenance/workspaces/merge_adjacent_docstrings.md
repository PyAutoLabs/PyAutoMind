# Phase 3: Merge adjacent documentation blocks in workspaces and HowTos

Type: maintenance
Target: workspaces
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Depends on:
- `draft/bug/pyautobuild/back_to_back_docstrings_notebook.md`
- `draft/feature/pyautobrain/adjacent_docstring_hygiene.md`

## Requested scope

Run the new Hygiene adjacent-docstring scan across @autofit_workspace,
@autogalaxy_workspace, @autolens_workspace, @autocti_workspace, @HowToFit,
@HowToGalaxy and @HowToLens. Merge every confirmed pair of consecutive top-level
triple-quoted documentation blocks separated only by whitespace, preserving all prose and
section ordering. Do not change ordinary string literals or blocks separated by code.

The initial read-only survey on 2026-07-24 found 79 adjacent boundaries in 56 scripts across
six of the seven repositories (none in HowToFit). Re-run the implemented scanner rather than
treating this provisional count as the source of truth. After cleanup, require a zero-finding
Hygiene result and validate representative generated notebooks, including
`autolens_workspace/start_here.py`, contain no literal `# %%`/triple-quote artifact cells.

This is phase 3 of the original request recorded verbatim in
`draft/bug/pyautobuild/back_to_back_docstrings_notebook.md`.
