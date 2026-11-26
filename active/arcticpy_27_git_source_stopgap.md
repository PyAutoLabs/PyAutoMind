# Heart: install arcticpy 2.7 from GitHub until it reaches PyPI (stopgap)

Type: maintenance
Target: PyAutoHeart
Repos:
- @PyAutoHeart
- @PyAutoCTI
- @autocti_workspace_test
Themes:
- cti
- install
Difficulty: small
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: never
Lane: any
Epic: cti-upkeep
Phase: 2b
Issued: 2026-11-26
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/372
Supersedes-blocker-of: draft/maintenance/pyautoheart/arcticpy_pin_bump_after_upstream_release.md (that draft stays as the switch back to PyPI)

## Request (human, 2026-11-26, verbatim)

> arcticpy 2.7 interim GitHub-install stopgap (cti-upkeep phase 2b unblock): tag v2.7 on
> jkeger/arctic (after heads-up to Richard Massey), add an arcticpy source setting to
> PyAutoHeart's install-arcticpy script defaulting to git+https://github.com/jkeger/arctic@v2.7
> instead of PyPI 2.6, update PyAutoCTI pyproject comment + install docs to the git install.
> Reason: PyPI arcticpy owner is only Jammy2211, whose PyPI MFA is broken (open PyPI support
> issue); Hands PYPI token is rhayes777's and was probed 403 on arcticpy 2026-11-26. Revert to
> arcticpy==2.7 on PyPI once login is restored.

## Facts established 2026-11-26 (don't re-derive)

- PyPI arcticpy roles: Owner `Jammy2211` only. Hands `secrets.PYPI` is a whole-account token
  of `rhayes777`; a no-publish probe (re-upload of the identical 2.6 sdist) returned
  `403 The user 'rhayes777' isn't allowed to upload to project 'arcticpy'`.
- Upstream `jkeger/arctic` main = `6f5153582aca00b7b0cc11ab04b2c58a7502400d` (PR #73 + #75
  merged, pyproject version 2.7). No tags exist upstream.
- Local pilot: `pip install --no-build-isolation --no-deps "arcticpy @ git+…@6f51535"` builds
  on Python 3.13 / numpy 2.5.4 / Cython 3.3 with libgsl-dev 2.7.1; Heart `arcticpy_smoke.py`
  OK; `test_autocti` 279 passed; autocti_workspace_test `scripts/{dataset_1d,imaging_ci}/likelihood/pins.py`
  both OK unchanged. The 2b draft's "pins will move" trap did not fire.
- Every consumer (Heart lib-tests/smoke-tests/docs-build, Heart local smoke.py, Hands
  python_matrix, Nerves setup_colab) runs the single `install_arcticpy.sh` from Heart main.
