# SersicCore alpha=0 ZeroDivisionError (multi-wavelength modeling)

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- autolens_workspace
- HowToLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Split out from `bug/autolens/slam_advanced_fitexception_cascade.md` (2026-07-21 reproduction sweep):
the multi-wavelength failure proved unrelated to the SLaM adapt-image / inversion cascade.

## Reproduction (clean main, test mode)

```
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib \
PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1 PYAUTO_SKIP_FIT_OUTPUT=1 PYAUTO_SKIP_VISUALIZATION=1 \
python scripts/multi/features/wavelength_dependence/modeling.py
```

Fails with:
```
File ".../PyAutoGalaxy/autogalaxy/profiles/light/standard/sersic_core.py", line 68, in intensity_prime
    ((2.0 ** (1.0 / self.alpha)) * self.radius_break)
ZeroDivisionError: float division by zero
```

## Root cause

The source galaxy is `al.lp_linear.SersicCore`. `SersicCore.intensity_prime` divides by `self.alpha`
(`2.0 ** (1.0 / self.alpha)` and again `2.0 ** (-self.gamma / self.alpha)`). When the model instance
carries `alpha == 0` (the test-mode/prior-median instance for this script), the profile raises
`ZeroDivisionError`. Other multi scripts don't hit this because they don't compose a `SersicCore`
source with the wavelength-dependent effective_radius relation.

## First step

Confirm whether `alpha=0` is (a) a bad config default / prior for `SersicCore` in this script's model,
or (b) a genuine robustness gap in `SersicCore.intensity_prime` that should be guarded (alpha lower
bounded away from 0, or the profile made to fail loudly with a physical message rather than a bare
ZeroDivisionError — respecting the no-silent-guards rule: fix the producer/prior, don't None-guard).
Decide library (PyAutoGalaxy prior/config or profile) vs workspace (script model) fix accordingly.

Affected (remove NEEDS_FIX once green):
- autolens_workspace: `multi/features/wavelength_dependence/modeling`
- HowToLens: multi-wavelength tutorial equivalent (verify the real path — the parent prompt's
  HowToLens paths were the workspace paths; HowToLens uses a chapter_N layout).
