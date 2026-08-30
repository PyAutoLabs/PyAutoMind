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
