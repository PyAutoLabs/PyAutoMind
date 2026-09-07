# autogalaxy_workspace_test multi_dataset/jax_likelihood/delaunay.py passes in 15 s under the smoke profile but times out at 1805 s under the release profile

Type: bug
Target: autogalaxy_workspace_test
Repos:
- autogalaxy_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-09-07
Witness: `scripts/multi_dataset/jax_likelihood/delaunay.py` completes under `profile_release.yaml` in under 300 s (it was 1805 s TIMEOUT on 2026-09-07 and 14.99 s under `profile_smoke.yaml`), with the triggering release-profile setting named in the PR.
Unattended: ready
Issued: 2026-09-07

On the Release Integrate rehearsal (PyAutoHeart run 34094964905, and the preceding
34018429178 on 2026-09-06) the `autogalaxy_workspace_test` leg fails on:

```
scripts/multi_dataset/jax_likelihood/delaunay.py   TIMEOUT (1805s)   [profile_release.yaml, cap 1800]
```

Same run, same script under the smoke profile: passed in 14.99 s. The sibling
`delaunay_mge.py` passes at ~28 s under both profiles. The script was touched by the
2026-09-06 smoke-dataset rebuild commit `eec09d6`.

A 15 s -> 1805 s split between env profiles on one script, with its MGE sibling unaffected,
looks like a JAX compile explosion under the release env grid (precedent: a non-uniform
over-sample map tripled jit compile time and pushed SLaM simultaneous.py past its 1800 s
cap). Reproduce locally under `profile_release.yaml`, profile compile vs execute time,
identify which release-profile env setting triggers it (over-sample grid, dataset
resolution, jit config), and fix either the script or the library path it exposes. Do
not resolve by raising the cap.
