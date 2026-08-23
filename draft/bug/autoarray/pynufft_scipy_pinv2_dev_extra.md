# PyNUFFT dev extra is incompatible with current SciPy on Python 3.13

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: normal
Status: superseded
Filed: 2026-07-29 (backfilled from git)

## Original request

> ok do phase 1b and any other tasks

## Finding

While validating the Python 3.12-floor Phase 1B change, a clean Python 3.13
environment installed with PyAutoArray's development extras failed the legacy
PyNUFFT transformer test. The pinned `pynufft==2022.2.2` calls
`scipy.linalg.pinv2`, which is absent from SciPy 1.17.1.

The identical failure reproduces on unmodified PyAutoArray `main`, while the
official CI-profile Python 3.13 environment (local packages plus `optional`
extras) passes 928 tests with one skip. This is therefore pre-existing dependency
drift, not a regression from the Python-floor diff.

## Task

Reproduce the dev-extra failure on clean `main`, census whether PyNUFFT remains a
supported optional backend, and choose one explicit remedy: constrain SciPy to a
compatible range for that extra, replace/upgrade PyNUFFT if a maintained version
exists, or retire the legacy backend and its tests. Keep this separate from the
`nufftax` dependency and from Phase 1B issue PyAutoArray#418.

## Acceptance

- A clean Python 3.13 development-extra install has a deliberate, documented
  compatibility policy.
- The PyNUFFT test either passes against the supported dependency set or is
  removed together with an explicit backend-retirement decision.
- The standard optional-profile suite remains green.

## Superseded 2026-08-22

Resolved by `draft/maintenance/libraries/remove_pynufft_legacy_transformer.md`,
which takes this prompt's third sanctioned remedy — "retire the legacy backend
and its tests". `pynufft` is gone from PyAutoArray's `optional` and `dev`
extras, so there is no longer a dev-extra install that can hit
`scipy.linalg.pinv2`.

Confirmed on a clean Python 3.13 install (2026-08-22): with
`pynufft==2022.2.2` present, `hasattr(scipy.linalg, "pinv2")` is `False` under
SciPy 1.17.1 — the drift this prompt reported is real, and pre-existing rather
than a Python-floor regression as it said. pynufft 2022.2.2 also emits
`SyntaxWarning: "is" with 'str' literal` on 3.13, i.e. it is unmaintained
against the supported interpreter range.

Close this out when the removal PRs merge.
