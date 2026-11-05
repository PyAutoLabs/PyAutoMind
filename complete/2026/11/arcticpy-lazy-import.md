## arcticpy-lazy-import
- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/117
- completed: 2026-11-05
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/118

Merged PyAutoCTI#118 (d36f307c) into main 2026-11-05 via human-typed /prm. Issue #117 closed. cti-upkeep phase 2c, ruling R2.

`import autocti` now works without arcticpy:
- `autocti/_arcticpy.py` provides `arcticpy()`, an accessor whose ImportError names the PyAutoHeart `install_arcticpy.sh` recipe, and `optional_import()`, which returns the real objects or, without arcticpy, placeholder classes that raise that error when called.
- The nine re-exports (`ac.TrapInstantCapture`, `ac.CCDPhase`, `ac.ROE`, ...) resolve through a PEP 562 `__getattr__`.
- clocker/, model/ and ou_sim_ci.py use `optional_import`.

With arcticpy installed, every name is the same object as before.

Design note: the approved plan's `TYPE_CHECKING` imports broke `af.Model`, because PyAutoFit evaluates constructor type hints at runtime. The placeholders are real classes, so those hints still resolve.

Evidence:
- The 4 new tests in `test_autocti/test_lazy_arcticpy.py` hide arcticpy with `sys.modules` and all fail on unchanged main.
- `test_autocti` gives 275 passed serially. Under `-n 8` the acs FITS tests collide, and they do the same on main.
- The 0b likelihood pins (10 literals) still match at rtol 1e-8, and the smoke scripts pass 3/3.
- CI: unittest 3.12 / 3.13 / nojax green.

Workspace impact: none.

PyAutoCTI is not yet in the pending-release published set; the merged PR carries the GitHub `pending-release` label, which release.yml's clear_pending_release_labels now covers.

## Original prompt

# autocti: `import autocti` works without arcticpy (lazy arcticpy import)

Type: feature
Target: autocti
Repos:
- @PyAutoCTI
Themes:
- cti
- install
Difficulty: medium
Autonomy: human-required
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: never
Epic: cti-upkeep
Phase: 2c
Issued: 2026-11-05

Ruling R2 (human, 2026-11-04): make `import autocti` succeed without arcticpy
installed. Anything that needs arcticpy should raise a clear error that names
the install recipe (PyAutoHeart `install_arcticpy.sh`). Drop the idea only if
the test suite or the factor-graph path cannot stay clean that way, and record
why.

## Facts (2026-11-05 survey)

- `autocti/__init__.py` re-exports nine arcticpy names as public API (`ROE`,
  `ROEChargeInjection`, `CCD`, `CCDPhase`, `TrapInstantCapture`,
  `TrapSlowCapture`, `TrapInstantCaptureContinuum`, `TrapSlowCaptureContinuum`,
  `PixelBounce`). Workspace scripts use them as `ac.TrapInstantCapture` inside
  `af.Model(...)`.
- Module-level `from arcticpy import ...` statements:
  - `clocker/abstract.py`, `clocker/one_d.py`, `clocker/two_d.py` (`add_cti`, `remove_cti`, `ROE`, `PixelBounce`, `CCD`, `CCDPhase`)
  - `model/model_util.py`, `model/settings.py`
  - `charge_injection/ou_sim_ci.py`
- arcticpy's trap, CCD, ROE and pixel-bounce classes are pure Python, but
  `arcticpy/__init__.py` always imports the compiled `wrapper` extension. That
  means autocti cannot import just the pure-Python parts; it has to defer the
  whole `arcticpy` import.
- pyproject already excludes arcticpy from the pip dependencies (its sdist is
  source-only and needs GSL and a C++ toolchain).

## Approach to evaluate

- Use a module-level `__getattr__` in `autocti/__init__.py` (PEP 562) for the
  nine re-exports. Accessing one of them imports arcticpy on first use, and if
  arcticpy is missing it raises an `ImportError` that names the recipe.
- Move the clocker, model and simulation imports into function bodies, or
  behind a single `autocti/_arcticpy.py` accessor.
- Type hints use string annotations or `TYPE_CHECKING`.
- Witness: in a venv with arcticpy hidden (for example a `sys.modules`
  `None` stub in a test), `import autocti` succeeds, `ac.Dataset1D` / `ac.Layout2DCI`
  build, and `ac.TrapInstantCapture` raises the recipe error. The full
  `test_autocti` suite and the 0b likelihood pins (autocti_workspace_test
  `scripts/*/likelihood/pins.py`) stay unchanged with arcticpy installed.
