## cti-docs-yml-caller
- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/125
- completed: 2026-11-06
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/325
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/126

Merged 2026-11-06 by glance-tier auto-merge, Heart first (b72e7f17), then PyAutoCTI (08040ff5) after re-running its Docs leg against Heart main. Plan approved by the human; Heart STALE ("release validation stale: source moved since rehearsal (PyAutoNerves)") human-acknowledged for this ship. cti-upkeep phase 3c.

- Heart `docs-build.yml`: `autocti) repo=PyAutoCTI; deps="PyAutoNerves PyAutoFit PyAutoArray"`, plus an `Install arcticpy` step gated on `inputs.package == 'autocti'` (the canonical install-arcticpy action, as in lib-tests.yml).
- PLAN CHANGE (human ruling 2026-11-06): the plan said no arcticpy in the docs build. Measured without it, autosummary can't import the arcticpy-backed classes autocti re-exports (TrapInstantCapture, TrapSlowCapture, TrapInstantCaptureContinuum, ROEChargeInjection, ...), so their pages build empty: 147 warning lines vs 15 with it. The human chose installing it over baselining.
- PyAutoCTI: `.github/workflows/docs.yml` thin caller (copy of PyAutoFit's MINUS its `generated-search-docs` job, which is autofit-only; watch for that when cloning callers); `docs/conf.py` PyAutoLens-style (no build-time cloning of rhayes777/Jammy2211 repos, no pyprojroot); `docs/requirements.txt` deleted (RTD installs `.[docs]`; no sibling keeps one); `docs/sphinx_warning_baseline.txt` = 15, which CI confirmed exactly.
- Heart ci_timing already carried CTI rows (derived from required_workflows), so nothing was needed there.

Evidence: CI `Sphinx warnings: 15 (baseline: 15)` green. Witness: a throwaway branch `witness/cti-docs-broken-entry` (workflow_dispatch, no PR) went red with `failed to import autocti.plot.subplot_this_does_not_exist`, then was deleted. Heart pytest 3.12/3.13 and PyAutoCTI unittest 3.12/3.13/nojax green.

Finding: Read the Docs has not built PyAutoCTI since 2024-01-29 (public builds API; the webhook isn't firing), so the published docs predate the resurrection, 5c and 3c. This belongs to phase 5c's "RTD on the released version".

## Original prompt

# PyAutoCTI docs build in CI: docs.yml caller on Heart's docs-build.yml + Sphinx warning baseline

Type: maintenance
Target: autocti
Repos:
- PyAutoCTI
- PyAutoHeart
Themes:
- cti
- docs-hub
- infrastructure
Difficulty: easy
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: a PyAutoCTI PR touching `docs/**` runs the `Docs` workflow through `PyAutoLabs/PyAutoHeart/.github/workflows/docs-build.yml@main` with `package: autocti` and it is green against a committed `docs/sphinx_warning_baseline.txt`; `docs/conf.py` no longer clones PyAutoFit/PyAutoArray at build time; a deliberately broken autosummary entry on a throwaway branch turns the leg red.
Review-minutes: 5
Unattended: ready
Epic: cti-upkeep
Phase: 3
Filed: 2026-11-06
Issued: 2026-11-06

Human request (2026-11-06): "then start_dev the docs.yml caller (3c)".

cti-upkeep phase 3c. PyAutoCTI has no `docs.yml`, so its Read the Docs build is checked by nothing
before merge. The 5c rewrite (PyAutoCTI#124, `complete/2026/11/cti-api-rst-rewrite.md`) took the api/
pages from 53 Sphinx warnings to 0; this phase stops them drifting back.

State found 2026-11-06:

- Heart `docs-build.yml` (reusable) maps `package` → repo + dependency chain for autonerves, autofit,
  autoarray, autogalaxy, autolens and pyautoscientist; it has **no `autocti` case** (an unknown package
  fails with `::error::unknown package`). It installs `./<dep>[optional]` per dependency, then
  `./<repo>[optional,docs]`, builds with `python -m sphinx -b html docs docs/_build/html -w warnings.log`
  and fails when the count goes above `docs/sphinx_warning_baseline.txt` (a missing file means 0).
- The sibling callers (`PyAutoFit/.github/workflows/docs.yml`, PyAutoLens, PyAutoGalaxy) are thin: push to
  main + pull_request on `docs/**`, `<pkg>/**`, `pyproject.toml`, `.readthedocs.yaml`, the workflow
  itself, plus `workflow_dispatch`. Baselines: PyAutoFit 30, PyAutoLens 134.
- PyAutoCTI `pyproject.toml` already has a `docs` extra (sphinx, furo, myst-parser, sphinx_copybutton,
  sphinx_design, sphinx_inline_tabs, sphinx_autodoc_typehints) and does **not** depend on arcticpy (the
  2c lazy import, PyAutoCTI#118), so `import autocti` works without the C++ build. The CI docs build
  should not install arcticpy: that is the point of R2. Expect a few extra autodoc warnings from
  arcticpy-backed signatures if any. Measure them; don't install arcticpy to hide them.
- `docs/conf.py` runs `git clone https://github.com/rhayes777/PyAutoFit` and
  `https://github.com/Jammy2211/PyAutoArray` at build time, `pip install -r` their (nonexistent)
  requirements.txt, and prepends the clones to `sys.path`. That needs `pyprojroot`, and in CI it would
  shadow the branch-matched dependencies Heart installs. Replace it with the PyAutoLens `conf.py` pattern
  (no cloning). Check that RTD still builds: `.readthedocs.yaml` installs `.[docs]` plus an arcticpy
  post_install.
- `docs/requirements.txt` pins `autonerves==2024.11.6.1`, `arcticpy==2.6` and `pyprojroot==0.2.0`.
  RTD does not read it (`.readthedocs.yaml` installs `.[docs]`). Decide: delete it, or align it with the
  docs extra. Check what the siblings do.
- Heart's ci_timing already carries CTI rows (PyAutoCTI `Tests`, the autocti_workspace gates,
  autocti_workspace_test), derived from `required_workflows`. **No ci_timing work is needed**; the
  epic text's "ci_timing rows" item is satisfied. Library `Docs` workflows are not timed for any sibling.
- Local measurement (2026-11-06, PyAuto313 + docs requirements, arcticpy installed, conf.py cloning):
  53 warnings in total, 0 on api/ (26 toc.not_included, 10 bullet-list, 8 myst H2, 5 myst xref, …).
  The CI number will differ (no arcticpy, no clones, `-w` file line count). Take the baseline from the
  first CI run, not from this.

Scope: (1) Heart `docs-build.yml`: add `autocti) repo=PyAutoCTI; deps="PyAutoNerves PyAutoFit PyAutoArray" ;;`
and add autocti to the `package` input description; (2) PyAutoCTI `.github/workflows/docs.yml` thin caller
mirroring PyAutoFit's; (3) `conf.py` de-cloned; (4) `docs/requirements.txt` resolved; (5)
`docs/sphinx_warning_baseline.txt` from the first green CI count (ratchet down only, with justification).
Heart merges first: the caller references `@main`, and the PyAutoCTI PR's Docs leg goes red until the
Heart mapping lands. Tenant firewall: the CTI names are already allowlisted from phase 1.

Out of scope: Python 3.14 (R4 deferred); Heart workspace-validation / release-integrate rows (p1-deferred,
separate); README badges (5c remainder).
