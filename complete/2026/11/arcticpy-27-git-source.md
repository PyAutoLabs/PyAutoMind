## Outcome
arcticpy 2.7 (numpy 2 / Cython 3, upstream jkeger/arctic #73 + #75) could not go to PyPI: the only PyPI owner of arcticpy is Jammy2211, whose PyPI MFA is broken (open PyPI support case), and the Hands `PYPI` secret is rhayes777's whole-account token — a no-publish probe (byte-identical re-upload of the 2.6 sdist) returned `403 The user 'rhayes777' isn't allowed to upload to project 'arcticpy'`. Stopgap shipped: the organism builds arcticpy 2.7 from the pinned commit `6f5153582aca00b7b0cc11ab04b2c58a7502400d`.

- PyAutoLabs/PyAutoHeart#373 (merged e1cf49e): `install_arcticpy.sh` gains `ARCTICPY_SOURCE` (default the pinned git URL); `ARCTICPY_VERSION` defaults empty and, when set, installs that PyPI version. Build deps `numpy>=2` / `cython>=3`. Tests assert a full 40-hex pin. All consumers (lib-tests, smoke-tests, docs-build, Hands python_matrix, local smoke, Nerves Colab) switched on merge.
- PyAutoLabs/PyAutoCTI#132 (merged 8c3781d): pyproject note, `.readthedocs.yaml`, AGENTS.md recipe.
- PyAutoLabs/autocti_workspace_test#28 (merged 67b73bc): pins.py provenance lines — verified unchanged under 2.7.
- Evidence: test_autocti 279 passed; smoke autocti 44/44, autocti_test 10/10; likelihood pins unchanged (the 2b draft's expected DR2 pin movement did not occur); arcticpy action self-test green on 3.12/3.13; independent review CLEAN.
- #373 was opened under the Heart RED development override (reason "PyAutoHeart: Heart Tests failure on main", unrelated date drift), cleared by the corrective PyAutoHeart#375 before merge; all merges were on green checks with Heart dev readiness GREEN.

## Follow-ups
- Revert path: `draft/maintenance/pyautoheart/arcticpy_pin_bump_after_upstream_release.md` — publish 2.7 to PyPI from the same commit once the login works, then default `ARCTICPY_VERSION` to `2.7`; also consider adding rhayes777 as an arcticpy maintainer so Hands can release it.
- 2c install-docs rewrite (`draft/docs/autocti/installation_docs_arcticpy_recipe.md`) can now use the git recipe.

## Original prompt

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
