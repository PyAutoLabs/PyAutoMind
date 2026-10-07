# setuptools package discovery picks up build/ — include allow-list

Completed: 2026-10-07
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/194
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/195
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/622
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1664
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/651
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/775
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/114
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/81
- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/195
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/622
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/651
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1664
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/775

All seven library PRs merged 2026-10-07 in library order (Nerves → Array → Fit → Galaxy → Lens, then CTI, Reduce) under a human `/prm`.

- `[tool.setuptools.packages.find]` in each repo's pyproject.toml now carries an `include = ["<pkg>*"]` allow-list (mirroring PyAutoHeart), keeping the existing excludes, so a local `pip install .` / `python -m build` no longer re-packages `build/` one level deeper.
- The fix also removes the stray top-level `docs/`, `files/`, `paper/` and `scripts/` directories (105 files) that the published autofit wheel (2026.10.4.1) installed into site-packages: the old `exclude` patterns excluded only the top-level names, not their subpackages.
- `build/` added to .gitignore where it was missing (PyAutoLens).
- Nerves, Array, Fit, Galaxy and Lens are merged but unreleased (pending-release above); CTI and Reduce are outside the published set.

## Original prompt

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
