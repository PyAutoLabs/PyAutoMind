## jax-grad-param9-autodiff-fd-mismatch
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/164 (closed)
- completed: 2026-07-14
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/165 (merged 6c4ff26a)
- repos: autolens_workspace_test
- summary: jax_grad imaging pixelization parameter-9 autodiff-vs-FD mismatch → parameter-specific documented FD exclusion. Release-tail item B. Corrective validation GREEN on v2026.7.14.1.dev66001 (integrate:pass); Heart YELLOW.

## Original prompt

# jax_grad imaging pixelization: autodiff vs finite-difference mismatch at parameter 9

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
- PyAutoArray
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Surfaced while burning down the 2026-07-13 release-validation tail (PyAutoHeart#72). Once
the per-script timeout was raised (mode=release now allows these to complete — PyAutoHeart
commit c19c948), `autolens_workspace_test/scripts/jax_grad/imaging_pixelization.py` runs to
completion (~6:38 on CPU) and then **fails its autodiff-vs-finite-difference gradient
assertion**:

```
util.assert_gradients_match(comparison)   # scripts/jax_grad/util.py:171
AssertionError: Autodiff vs finite-difference mismatch at parameter indices [9]:
  ad=[149808.61606031], fd=[-5282762.48254538], abs_err=[5432571.0986057], tolerance=[5282.76258255]
```

The mismatch is gross — **opposite sign, ~35× magnitude** — not a tolerance drift. The earlier
configs in the same script all FD-match and PASS (RectangularUniform; RectangularAdaptDensity
staircase invariance; RectangularAdaptImage + reg.Adapt os_pix=4; RectangularAdaptDensity
os_pix=4). Only the final `compare_gradients` / `assert_gradients_match` (line ~452) trips, at
parameter index 9.

**Leading hypothesis:** `fd=-5.28e6` is characteristic of a **finite-difference blow-up** —
parameter 9's likelihood has a near-discontinuity / boundary where central-FD is unreliable,
so AD (`+1.5e5`) is probably the correct value and FD is the artifact. If so the fix is to add
parameter 9 to the documented `skip_indices` in the script (the gradient-audit README in
`autolens_workspace_developer/jax_profiling/gradient/` documents such FD-unreliable cases),
NOT a library change. **BUT** this MUST be confirmed it is not a **jax-0.10.2 autodiff
regression** first: the dev venv is now jax 0.10.2 (bumped 2026-07-14, see
[[reference_laptop_gpu_jax_setup]]); reproduce the same script on jax 0.9.2 and check whether
parameter 9 matched there. If AD changed between jax versions, this is a real gradient
regression in the pixelized-inversion custom_jvp path (PyAutoArray/PyAutoGalaxy), not a test
fix — do not paper over it with skip_indices ([[feedback_no_silent_guards]]).

Identify which parameter index 9 is (print `param_names[9]`) and which configuration's
comparison fails. Cross-ref [[project_jax_gradient_audit_shipped]] (the 2026-07 gradient
audit that these assertions encode). Sibling `jax_grad/interferometer.py` also failed in the
same release run — check whether it shares the same parameter/root cause.

Repro: `~/venv/PyAuto` (now jax 0.10.2), from `autolens_workspace_test/`,
`python scripts/jax_grad/imaging_pixelization.py` (~7 min; it self-simulates). Release run:
PyAutoHeart workspace-validation `29279095224` (TestPyPI `2026.7.13.1.dev65601`).
See [[project_release_2026_07_13_blocked_3bugs]].
