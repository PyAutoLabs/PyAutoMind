# Induct PyAutoReduce into the PyAutoHands release machinery (date versioning)

Type: release
Target: pyautoreduce
Repos:
- PyAutoHands
- PyAutoReduce
- PyAutoBrain
- PyAutoHeart
- PyAutoMind
Themes:
- release
- reduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: never
Filed: 2026-08-24

## Original request (verbatim)

> also update it to use date version in line with all other repos this could be
> a whole induction into pyautohands etc

## Why this is separate

Split out of `active/autoreduce_pypi_name_collision.md` (PyAutoReduce#71). That
task establishes a distribution name PyAutoLabs can actually publish under
(`pyautoreduce`; `autoreduce` on PyPI belongs to an unrelated, actively
maintained project). **This task must not start until #71 has merged** — every
step below uploads or verifies under the new name.

## The gap

PyAutoReduce has never been released. `git ls-remote --tags` returns nothing,
and PyAutoHands has zero references to it:

- `.github/workflows/release.yml` — the `release_test_pypi`, `release`,
  `release_notes` and `release_workspaces` matrices name only PyAutoNerves,
  PyAutoFit, PyAutoArray, PyAutoGalaxy and PyAutoLens.
- `pre_build.sh` — `WORKSPACE_SPECS` has no `autoreduce_workspace` entry.
- The TestPyPI install-verify loop hardcodes
  `PACKAGES=("autonerves" "autoarray" "autofit" "autogalaxy" "autolens")`.

## Date versioning is not a packaging change

Worth stating plainly, because the request sounds like one. PyAutoReduce's
build config is *already* identical to PyAutoLens's:

```toml
[build-system]
requires = ["setuptools>=79.0", "setuptools-scm", "wheel"]
[project]
dynamic = ["version"]
[tool.setuptools_scm]
version_scheme = "post-release"
local_scheme = "no-local-version"
```

The family's `2026.8.23.1` versions come from the annotated tag `release.yml`
pushes immediately before `python -m build`; setuptools-scm reads it. So
PyAutoReduce gets date versioning the moment it is in the release matrix — no
`pyproject.toml` change required. Nothing here should reintroduce a hand-managed
version string.

One genuine difference: `autoreduce/__init__.py` resolves `__version__` through
`importlib.metadata` rather than carrying a literal `__version__ = "..."`. The
release job's stamping step seds `*/__init__.py` and **hard-fails** if no file
carries a `__version__ = ` line ("No `__init__.py` carries a `__version__`
stamp — the sed matched nothing"). Decide deliberately between:

- exempting PyAutoReduce from the stamp step (its `importlib.metadata` lookup is
  the mechanism the family wanted anyway — recorded as the "`__version__` via
  `importlib.metadata`" polish follow-up in `complete/2026/07/release-stamping-slim.md`), or
- adding a literal stamp line for the sed to find.

The first is better and should be the default; it needs the stamp step to become
conditional rather than universal.

## Scope

In @PyAutoHands:

- Add `PyAutoLabs/PyAutoReduce` to the `release_test_pypi`, `release` and
  `release_notes` matrices, with its own `pat` secret name.
- Add `pyautoreduce` to the TestPyPI install-verify `PACKAGES` array and the
  `pip install "<pkg>[optional]==$VERSION"` loop — note PyAutoReduce has **no**
  `optional` extra (its extras are `hst`/`keck`/`psf`/`starred`/`frames`/`test`/
  `dev`), so the loop's `[optional]` suffix needs handling rather than copying.
- Make the `__init__.py` stamp step tolerate a package with no literal
  `__version__` (see above) without weakening the existing guard for the five
  packages that do carry one.
- Add `autoreduce_workspace` to `pre_build.sh`'s `WORKSPACE_SPECS` **only if**
  notebook generation is wanted there; it has no notebooks today, so the
  default answer is probably no. Decide explicitly and comment the decision.
- `release.yml` carries a comment explaining why `autocti_assistant` is
  deliberately not wired in. Add the equivalent note for whatever is left out
  here, so the next reader does not read omission as oversight.

In @PyAutoReduce:

- Whatever the stamp decision above requires (likely nothing).
- A `pending-release` label, if `ensure_workspace_labels.sh` does not already
  cover the repo.

In @PyAutoBrain:

- Add PyAutoReduce to the nightly driver's activity-gate repo list
  (`nightly-release.yml`), so a day whose only merged work is here is not
  skipped as "no activity".

In @PyAutoHeart:

- Check whether `version_skew`, `wiki_currency` and the readiness checks
  enumerate the five libraries by name and need PyAutoReduce added, or whether
  they read the body map.

In @PyAutoMind:

- `repos.yaml` currently gives PyAutoReduce `category: library` with no release
  role. Confirm it needs no field change once the repo is release-bearing, and
  re-run `python3 scripts/repos_sync.py --write`.

## Answered by the human (2026-08-24)

1. **Cadence — nightly, with the other projects.** PyAutoReduce joins the
   scheduled nightly rather than releasing on demand. Consequence beyond the
   `release.yml` matrices: the nightly driver is *activity-gated* over a list of
   release-relevant repos (`complete/2026/07/nightly-release-activity-gate.md`,
   PyAutoBrain `nightly-release.yml` / `docs/nightly_release_design.md` §2), so
   PyAutoReduce must be added to that list too — otherwise a day whose only
   merged work is in PyAutoReduce reads as "no activity, skipped" and its
   changes never ship. Heart GREEN still gates every nightly.

2. **First version — the family's date scheme, `2026.8.24.1`-shaped.** Asked for
   as `YYYY.MM.DD.1`; recorded here as the family format because the two are the
   same thing on PyPI and no work separates them:

   - `release.yml`'s `version_number` job computes `date +"%Y.%-m.%-d"`, which
     strips leading zeros — hence `autolens 2026.8.4.1`, `2026.8.7.1`.
   - PEP 440 integer normalization drops leading zeros from every segment
     anyway, so a zero-padded tag cannot survive to the index:
     `Version("2026.08.24.1") == Version("2026.8.24.1")`, and PyPI would display
     the unpadded form regardless.

   So PyAutoReduce takes the shared `version_number` output unchanged. **Do not**
   add a padded date format for this repo — it would diverge from the family in
   the source and converge back at the index, which is the worst of both.
   No `0.x` line first.

3. **PyPI token — PyAutoLabs org, `Jammy2211` account.** The first upload of a
   brand-new project cannot use a project-scoped token (the project does not
   exist yet), so it needs an account-scoped token from `Jammy2211`, stored as
   an Actions secret in PyAutoHands alongside the existing per-repo PATs. After
   the first successful publish, narrow it: create a `pyautoreduce`
   project-scoped token, replace the secret, and revoke the account-scoped one.
   Do not leave an account-scoped token in CI once it is no longer needed.

## Done when

- A `pyautoreduce` release runs end to end through `release.yml` — TestPyPI
  first, then a live publish — and the published artifact declares
  `Requires-Python >=3.12`.
- The version is a family-shaped `YYYY.M.D.N` derived from a pushed tag.
- Every omission from the release machinery is deliberate and commented.
