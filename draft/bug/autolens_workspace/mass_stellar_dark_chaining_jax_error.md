# group/mass_stellar_dark chaining fails with a JAX exception on release wheels

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
- PyAutoGalaxy
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Surfaced burning down the 2026-07-13 release-validation tail (PyAutoHeart#72). On the
release wheels under the release profile:

```
scripts/group/features/advanced/mass_stellar_dark/chaining.py ... FAIL (26.6s)
  For simplicity, JAX has removed its internal frames from the traceback of the following
  exception. Set JAX_TRACEBACK_FILTERING=off to include these.
```

The run-runner captured only the filtered banner, not the actual exception — it is a **real
JAX error** during a group-scale mass_stellar_dark **chaining** pipeline (real sampler,
`PYAUTO_TEST_MODE=1` for user workspaces), and fails fast (26.6 s), so it is NOT a timeout
(distinct from the other `group/`/`chaining` scripts that TIMEOUT and are handled by the
release timeout bump PyAutoHeart#c19c948).

Reproduce from the `autolens_workspace` checkout on current main under the release profile,
with `JAX_TRACEBACK_FILTERING=off` to get the real traceback:

```
cd autolens_workspace
JAX_TRACEBACK_FILTERING=off PYAUTO_TEST_MODE=1 PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1 \
  python scripts/group/features/advanced/mass_stellar_dark/chaining.py
```

The dev venv is now jax 0.10.2 (matches the release stack — see
[[reference_laptop_gpu_jax_setup]]), so this should reproduce locally. Candidate causes given
the release-validation context: a jax-0.10.2 numerical/behaviour change in the chained
group-scale fit (cf. the jax-drift and LinAlg-not-PD siblings), a NaN/inf in a chained-prior
pass, or a real group/mass_stellar_dark modelling issue. Classify (jax regression vs real
bug) and fix at the right layer. Release run: PyAutoHeart workspace-validation `29279095224`,
TestPyPI `2026.7.13.1.dev65601`. See [[project_release_2026_07_13_blocked_3bugs]] and
PyAutoHeart#72.
