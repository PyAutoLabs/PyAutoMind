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
