Shipped 2026-08-23 across three repos (issue @PyAutoHands#258, closed 2026-08-24):
@PyAutoHands `736abfe`, @PyAutoHeart `fedcd91`, @PyAutoCTI `28c84710` — all three
on `origin/main`. Direct-to-main commits, no PRs.

Phase 3 of 3 of the pynufft-removal residue sweep. Parent ledger:
`draft/maintenance/workspaces/pynufft_removal_downstream_residue.md` (still live —
see "What this does NOT close" below). Siblings:
`complete/2026/08/pynufft-removal-residue-phase-1.md`,
`complete/2026/08/pynufft-removal-residue-phase-2.md`.

## What changed

- **@PyAutoHands** `.github/workflows/release.yml` — dropped
  `pip install pynufft==2025.1.1` from three steps: `release_test_pypi → Tests`,
  `run_smoke_tests → Install from TestPyPI at pinned version`, and
  `release_workspaces → Regenerate API audit baseline`. `numba` kept at both
  sites where the two shared a line; the adjacent "matplotlib deliberately
  unpinned" comments are about matplotlib and were untouched.
- **@PyAutoHeart** `.github/workflows/workspace-validation.yml` — dropped the same
  install from the `mode=release` "Install TestPyPI wheels" step. `numba` kept
  (it shared the line); the `nufftax>=0.6.1,<0.7.0` install below it is the live
  NUFFT backend and was untouched.
- **@PyAutoCTI** `docs/installation/source.rst` — deleted the
  `pip install pynufft` line from the "For unit tests to pass you will also need
  the following optional requirements" list.

## The PyAutoCTI line was verified, not assumed

The prompt said "confirm PyAutoCTI's suite genuinely has no such need before
deleting the line — verify, do not assume". The commit records the verification:

- `.github/workflows/main.yml` calls PyAutoHeart's reusable `lib-tests.yml`, which
  installs `./PyAutoCTI[optional]` plus the Nerves/Fit/Array chain and never
  installs pynufft in either leg.
- `pyproject.toml`'s `optional` extra is `["numba"]` — pynufft is not in it.
- The latest `main` run of that workflow was green on every leg (unittest 3.12,
  unittest 3.13, unittest-nojax).
- A full-tree grep found `pynufft` only in `paper/paper.bib` and
  `files/citations.tex` (published-record material, deliberately out of scope).

## Severity, as filed

Not urgent and never red: the recipes pinned `2025.1.1`, not the `2022.2.2` that
hits the `scipy.linalg.pinv2` failure. This was install time and resolver surface
only. Side effect worth knowing: these recipes were the only reason a fresh local
dev environment still ended up with `pynufft 2025.1.1` installed at all.

## Verified state (2026-09-14 triage)

`grep -c pynufft` returns **0** on all three files, and each commit is contained
in `origin/main`. Acceptance met: no PyAuto CI workflow installs pynufft, and the
PyAutoCTI install doc no longer instructs users to.

## What this does NOT close

The parent prompt stays live. Still outstanding on it:

- **@autogalaxy_workspace `markdown/`** — `markdown/interferometer/start_here.md`
  and `markdown/interferometer/simulator.md` still carry the stale pynufft text
  (verified 2026-09-14). `generate_markdown.py` executes curated scripts for real
  and is an at-release step, so phase 2 deliberately did not run it. The
  top-level `markdown/start_here.md` is now clean.
- Two findings the parent recorded but never filed anywhere: @autolens_workspace_developer's
  committed datasets do not reproduce from their own scripts, and that repo has no
  test CI.

## Original prompt

# Phase 3: stop installing pynufft in Hands/Heart CI and PyAutoCTI install docs

Type: maintenance
Target: ci
Repos:
- @PyAutoHands
- @PyAutoHeart
- @PyAutoCTI
Themes:
- ci-smoke
- hygiene
- interferometer
Difficulty: low
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-08-23

Phase 3 of 3. Parent: `pynufft_removal_downstream_residue.md`. Independent of
phases 1 and 2.

`pynufft` is no longer a dependency of any PyAuto library (@PyAutoArray#475
dropped it from both `optional` and `dev`), but four CI recipes and one install
doc still install it.

## Sites

- `@PyAutoHands/.github/workflows/release.yml:296,355,774` —
  `pip install pynufft==2025.1.1` (once bare, twice with `numba`)
- `@PyAutoHeart/.github/workflows/workspace-validation.yml:302` — same
- `@PyAutoCTI/docs/installation/source.rst:58` — `pip install pynufft`, listed
  under "For unit tests to pass you will also need the following optional
  requirements". **Confirm PyAutoCTI's suite genuinely has no such need before
  deleting the line** — verify, do not assume.

## Severity

Not urgent. These pin **2025.1.1**, not the broken `2022.2.2`, so they are
**not** hitting the `scipy.linalg.pinv2` failure and no build is red. This is
wasted install time and unnecessary resolver surface.

Worth knowing while working: these recipes are the only reason the local dev
environment still has `pynufft 2025.1.1` installed at all — removing them
changes what a fresh local env contains.

## Acceptance

- No PyAuto CI workflow installs `pynufft`.
- PyAutoCTI's install doc no longer instructs users to, with evidence its tests
  pass without it.
- The affected workflows are confirmed green afterwards — **every run and every
  matrix leg**, not just the first one reported.
