# setuptools package discovery picks up build/ (recursive build/lib/build/lib… nesting)

Type: bug
Target: libraries
Repos:
- PyAutoNerves
- PyAutoArray
- PyAutoCTI
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
- PyAutoReduce
Themes:
- packaging
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Filed: 2026-10-07
Issued: 2026-10-07

Original request (verbatim, from the parent session):

> packaging: setuptools package discovery picks up build/ (recursive build/lib/build/lib… nesting).
> Cause: `[tool.setuptools.packages.find]` in pyproject.toml has only an `exclude` list, so each local `pip install .`/`python -m build` re-packages the previous build/ one level deeper (autonerves.egg-info/top_level.txt lists `build`). Published wheels are clean (CI builds fresh) — local-only bug, but a local build would ship it.
> Affected repos (7): organs/PyAutoNerves, array/PyAutoArray, cti/PyAutoCTI, fit/PyAutoFit, galaxy/PyAutoGalaxy, lens/PyAutoLens, reduce/PyAutoReduce. organs/PyAutoHeart already uses `include` — mirror its style.
> Fix per repo: add `include = ["<pkg>*"]` (the repo's top-level package(s) — check the actual package dirs; keep existing excludes, keep tests excluded) to packages.find. lens/PyAutoLens's .gitignore does not ignore build/ — add `build/` there. Check any other repos' .gitignore too.
> Verify per repo: `python -m build --wheel` into a scratch dir and confirm the wheel's top-level entries are only the package + dist-info. For PyAutoNerves, refresh the editable install's stale egg-info top_level.txt.

Finding at filing (2026-10-07): the published wheels are NOT fully clean —
`autofit-2026.10.4.1` on PyPI installs top-level `docs/`, `files/`, `paper/` and
`scripts/` directories into site-packages (105 stray files), because the
`exclude = ["docs", ...]` patterns exclude only the top-level name, not its
subpackages. The `include` allow-list fixes that too.
