# arcticpy: upstream packaging PR to jkeger/arctic + request a modern PyPI release

Type: release
Target: arcticpy
Repos:
- jkeger/arctic (third-party upstream; PR from a fork)
Themes:
- cti
- install
- upstream
Difficulty: medium
Autonomy: human-required
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: never
Epic: cti-upkeep
Phase: 2a

Ruling R1 (human, 2026-11-04): fix arcticpy UPSTREAM. PyAutoLabs publishes no
wheels and no renamed fork. The human asks Richard Massey to cut the PyPI
release.

## Scope

- **PR to `jkeger/arctic`:**
  - `numpy>=1.21,<3` instead of `~=1.21` (the current pin downgrades numpy below 2.0)
  - Cython 3
  - an unpinned `setuptools_scm`
  - declared `[build-system] requires` (numpy, Cython), so `--no-build-isolation` is no longer required
  - pyproject `version` bumped. It currently says 2.5 while PyPI has 2.6, and main
    carries the 2026-04-06 Euclid DR2 well-filling (#71) and pixel-bounce (#69)
    changes.
  - Optional, if feasible: `cibuildwheel` wheels with GSL vendored or statically
    linked (manylinux plus macOS).
  - Optional and small: wrap the `arcticpy.wrapper` import in `__init__.py` so the
    pure-Python model classes import without the compiled extension.
- **Verify on the fork:** a clean build on Python 3.12 and 3.13 with numpy 2.x
  (cp313 builds locally today), plus `arcticpy_smoke.py` from PyAutoHeart.
- **Hand-off:** a short note the human can send to Richard Massey asking for the
  2.7 release.

Opening a PR on a third-party repository is outward-facing, so it needs explicit
human approval before it is sent.

## Prepared 2026-11-05 (NOT sent; awaiting human go-ahead to fork + open)

- Local clone `~/Code/PyAutoLabs-wt/arcticpy-upstream-packaging/arctic`, branch
  `packaging-modern-numpy-cython3`, commit 53534d0 (pyproject.toml + 2 lines of setup.py, CRLF kept).
- Drafts beside it: `PR_BODY.md` (the PR text) and `NOTE_TO_MASSEY.md` (release request).
- Found while testing, now fixed in the same commit:
  - `matplotlib` and `scipy` are imported by `import arcticpy` but undeclared.
  - `setup.py` links only `gsl`; it needs `gslcblas` and `library_dirs`. Only Debian's system libgsl links without them.
- Evidence (Linux, Python 3.13, GSL 2.7.1 from source):
  - the isolated wheel and sdist both build
  - a fresh venv (numpy 2.5.4) passes `pip check`
  - upstream `pytest test/` gives 7 passed
- Not tested: macOS, Windows, numpy 1.x at runtime.
- To open: `gh repo fork jkeger/arctic --clone=false`, push the branch to the fork, then
  `gh pr create -R jkeger/arctic --head Jammy2211:packaging-modern-numpy-cython3 --body-file PR_BODY.md`.
  After that, the human sends the note to Richard Massey.
