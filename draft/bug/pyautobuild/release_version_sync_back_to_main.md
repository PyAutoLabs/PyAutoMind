# Release does not sync __version__ stamps and workspace pins back to main

Type: bug
Target: PyAutoBuild
Repos:
- PyAutoBuild
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## Symptom

A successful release (including the nightly build) leaves the organism's version
references in a **split, stale state**. After the `2026.7.9.1` release the whole
stack was still stamped with the now-yanked `2026.7.6.649` in five library
`__init__.py` files, every workspace `version.txt` / `config/general.yaml:
workspace_version` pin, and two READMEs — while the same repos' Colab URLs had
already moved to `2026.7.9.1`. Fixing it by hand took a 15-repo bump on
2026-07-13.

## Root cause

`PyAutoBuild/.github/workflows/release.yml` bumps and pushes to `main` only:

- Colab URL tag refs (`release.yml:652,697`),
- regenerated notebooks (`:605`),
- stamped wheels + git tags (`:403,411`).

It intentionally does **not** commit back to `main`:

- library `__init__.py` `__version__` — `sed`'d for the wheel only (`:128,403`),
  never committed to the library mains,
- workspace `version.txt` / `config/general.yaml:workspace_version` — the
  "Write workspace version" step was **removed** under **PyAutoBuild#120**'s
  compatibility-floor redesign (`:607-611` comment).

So a release moves the URLs and tags but freezes the `__version__` stamps and
version pins → the observed drift.

## Fix

Make a successful release bump **every live version reference consistently** and
commit it back, so this stale/split state cannot recur. Expected scope:

- `PyAutoBuild/.github/workflows/release.yml` — re-add (or re-model) the
  write-back of library `__init__.py` stamps and workspace pins alongside the
  existing Colab-URL / notebook / tag commits.
- `PyAutoBuild/pre_build.sh` — the README "pkg vX" pin bump path (`:53`) that
  also drifted.
- `PyAutoHeart` `version_skew` check — `internals.md` already flags it "needs a
  follow-up rework to compare floors against release tags rather than
  stamp-vs-pin"; reconcile it with whatever model this fix adopts.

## Constraints / design note

This partially reverses/extends the **PyAutoBuild#120** floor-model redesign
(wheels/tags as the release anchor, `minimum_library_version` as a deliberate
floor). Weigh the churn vs. consistency tradeoff #120 was avoiding, and respect
the never-rewrite-history rules, before choosing between "commit stamps back to
every main on each release" vs. an alternative that keeps mains authoritative.

**Must NOT touch** historical/provenance references to old versions:
`autolens_profiling/**` result files and filenames (e.g. `..._v2026.7.6.649.json`),
`scripts/yank_pypi_browser_console.js` (the yank list), PyAutoHeart/PyAutoConf
test fixtures, and PyAutoMind history.

<!-- formalised by the Intake (Conception) Agent on 2026-07-13 from user-intake; re-homed triage/ -> bug/pyautobuild/ by hand (classifier low-confidence) -->
