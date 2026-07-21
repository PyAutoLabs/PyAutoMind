# Analysis `log_likelihood_function` masks the real error behind a bare FitException

Type: bug
Target: autolens
Repos:
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Surfaced 2026-07-21 during the interferometer-Delaunay marker re-diagnosis (autolens_workspace#308/#309).
The numpy-path `log_likelihood_function` in all three lens analyses wraps the fit in a bare
`except Exception as e: raise af.exc.FitException` — and **discards `e`** (no `from e`, no log):

- `PyAutoLens/autolens/imaging/model/analysis.py:143-144`
- `PyAutoLens/autolens/interferometer/model/analysis.py:181-182`
- `PyAutoLens/autolens/point/model/analysis.py:138-139`

The FitException itself is CORRECT and must stay (PR#607 path-parity: a numpy-path non-PD `LinAlgError`
→ `FitException` → the sampler resamples, mirroring the JAX NaN-resample). The problem is purely
**observability / debuggability**:

1. **The cause is thrown away.** `as e` is captured but never used — no exception chaining. When a fit
   raises, the traceback is just `FitException` at `analysis.py:182`; the true error (which inversion,
   which matrix, non-PD vs a real bug) is invisible. This directly cost time on #308/#309 (had to comment
   out the re-raise to see the cause).
2. **`except Exception` is maximally broad.** A genuine code bug (KeyError, typo, shape error) is
   silently reclassified as "resample this model" — indistinguishable from a legitimately pathological
   model. A latent bug can hide as a slightly-lower acceptance rate forever.

## Fix (minimal, no behaviour change to real fits)

- Chain the cause: `raise af.exc.FitException from e` in all three sites (keeps resample semantics; the
  original traceback survives for anyone who unwraps).
- Optionally, an opt-in debug escape hatch (env, e.g. `PYAUTO_RAISE_ANALYSIS_EXCEPTIONS=1`) that re-raises
  the original `e` instead of wrapping — so a developer can see real crashes without editing library source.
  Default OFF (production must keep wrapping so searches resample).
- Do NOT narrow the `except` to specific types — path-parity needs to catch the numpy non-PD raise (and
  future analogous raises); the goal is visibility, not a tighter catch.

Out of scope (separate concern, if wanted): `TEST_MODE=2` bypass tolerance so a single-eval FitException
does not hard-fail a smoke run (that was the #308 symptom; the marker turned out stale so it was not needed
there, but it is the general fragility).

First step: confirm the three sites are still `raise af.exc.FitException` (no `from e`); add `from e`;
add the opt-in raise-through env; verify a deliberately-crashing model shows the real traceback with the
env set and a clean resample without it. Unit test in `test_autolens` (numpy-only, no JAX).
