# Promote the search-zip preservation helper to a public PyAutoFit paths

Type: refactor
Target: autofit
Repos:
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Session note from the slam-resume-fastpath ship (PyAutoGalaxy#502): the private helper
`_append_to_search_zip` currently lives in @PyAutoGalaxy `autogalaxy/analysis/adapt_images/adapt_images.py`
and is cross-imported by @PyAutoLens `autolens/analysis/result.py`. It appends a post-completion cache
file into a search's `.zip` archive so that `paths.restore()` (which deletes the output dir and
re-extracts the zip) does not destroy it on the next resume.

That concern belongs to the paths layer, not to an adapt-images module: any code writing artifacts into a
completed search's `files/` needs it. Promote it to a public method on @PyAutoFit
`autofit/non_linear/paths/abstract.py` — e.g. `AbstractPaths.preserve_in_zip(file_path)` — with the same
semantics (no-op when the zip does not exist; skip if the member is already present; arcname relative to
`output_path`), plus a unit test (write a file into a zipped search's files/, preserve, restore, assert
the file survives). Then switch the @PyAutoGalaxy caller and the @PyAutoLens caller to
`result.paths.preserve_in_zip(...)` and delete the private helper + cross-import. PRs ordered PyAutoFit
first, then PyAutoGalaxy, then PyAutoLens.

<!-- formalised by the Intake (Conception) Agent on 2026-07-17 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/ce78c7e9-3f34-4983-bb53-8840527c1fb6/scratchpad/intake_preserve_zip.md -->
