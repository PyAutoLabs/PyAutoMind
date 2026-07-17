## preserve-in-zip
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1389 (closed)
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1390 (phase 1), https://github.com/PyAutoLabs/PyAutoGalaxy/pull/507, https://github.com/PyAutoLabs/PyAutoLens/pull/620 (phase 2, all MERGED)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/79 (MERGED — stopgap removal rider + post-fast-path reference)
- summary: Promoted the search-zip preservation concern to public AbstractPaths.preserve_in_zip (no-op sans zip, idempotent; tests incl. survive-restore) and switched the ag/al fast-path callers to it, deleting the private _append_to_search_zip + cross-import. Rider closed with it: bypass-.completed stopgap removed from pipeline_resume (no-op since Fit#1388); post-fast-path reference recorded — cold 159s -> any resume ~11-13s (cold run writes the caches itself, so even the FIRST resume is fast; remaining floor = imports + stage-1 check_likelihood_function). Gotchas: phase 2 ran under a parallel-claim override on ag/al (potential-correction-port owns profiles/mass/input; zero file overlap, user-instructed); autolens_profiling main carried 2 CI-blocking ruff errors in jax_compile/trace_profile.py — fixed in #79 (isort: skip on a sys.path-dependent import; ruff --fix would have broken it). Suites 991p/388p; profiling ruff clean.

## Original prompt

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
