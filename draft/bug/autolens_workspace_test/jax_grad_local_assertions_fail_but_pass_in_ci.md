# jax_grad scripts fail assertions locally that PASS in CI

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised

Running the `jax_grad` scripts locally under the resolved smoke profile produces
deterministic assertion failures in scripts that **pass in CI on the same commit**.
Found while measuring script durations for PyAutoHands#226.

## Evidence

Run via `env_config.build_env_for_script` with the workspace root as CWD (i.e. the
exact env the runner builds — `PYAUTO_SMALL_DATASETS` unset, `PYAUTO_DISABLE_JAX`
unset, `PYAUTO_TEST_MODE=2`, verified by printing the resolved env):

| script | local | CI (run 30858578587 / 30790463134) |
|---|---|---|
| `imaging/jax_grad/lp.py` | **FAIL 41.3s** | **PASS 39.6s / 40.0s** |
| `imaging/jax_grad/knn.py` | PASS 141.6s | PASS 200.0s / 175.8s |
| `imaging/jax_grad/pixelization.py` | **FAIL 57.5s** | PASS 244.8s (06:31Z) |
| `imaging/jax_grad/regularization.py` | **FAIL 131.5s** | (import gap, then TIMEOUT) |
| `point_source/jax_grad/gradient.py` | PASS 665.9s | TIMEOUT (300s cap) |

`lp.py` is the decisive case: it **passes in CI on both runs** and fails locally.

Failures are deterministic and bit-identical across repeated runs, e.g.
`pixelization.py`:

```
AssertionError: Eager (-8354.484097835004) and jitted (-8354.55843260181) evaluations
disagree — possible pure_callback constant-folding; do not trust jitted gradients.
```

(relative difference ~8.9e-6 against `assert_eager_jit_consistent`'s `rtol=1e-10`).

`lp.py` fails with `All source-parameter gradients are ~zero — NNLS zeroed the source`;
`regularization.py` with an AD-vs-FD mismatch marginally over tolerance
(`abs_err=[0.045, 0.042, 0.057]` vs `tolerance=[0.031, 0.008, 0.003]`).

## What is ruled out

- **Not the small-datasets cap.** `full_datasets` correctly unsets
  `PYAUTO_SMALL_DATASETS`; verified by resolving the env directly rather than
  inferring from mask sizes.
- **Not a JAX version difference.** Local jax/jaxlib are 0.10.2 — identical to CI.
- **Not flake.** Repeated runs give bit-identical values.

Prime remaining suspect: **numpy 2.2.6 local vs 2.4.6 in CI**, or another local venv
package differing from the CI install set. Not yet confirmed.

## Why it matters

This is an active trap for anyone validating these scripts locally. During #226 it
looked exactly like two fresh correctness regressions on current main
(`pure_callback` constant-folding, and an FD tolerance breach). Only running a
**control** — `lp.py`, known-passing in CI — revealed that the local environment
itself produces the failures, so none of the three local failures were evidence of
source defects.

Whatever the cause, either the scripts or the documented local-run recipe should make
this reproducible, so a local FAIL means something.

## Suggested scope

1. Bisect the local-vs-CI package delta (start with numpy 2.2.6 -> 2.4.6) against
   `lp.py`, the cleanest discriminator.
2. If numpy is the cause, decide whether the tolerances are under-specified for the
   supported numpy range, or the local env should be pinned to the CI set.
3. Record the outcome in the workspace's local-run instructions.

<!-- Split out of PyAutoHands#226 on 2026-08-04; that task deliberately did not absorb
     this, and explicitly barred setting any timeout budget from local numbers. -->
