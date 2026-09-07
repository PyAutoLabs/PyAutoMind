# autogalaxy_workspace_test multi_dataset/jax_likelihood/delaunay.py quarantined as the fifth xla-cpu-eigen-pool-deadlock member

autogalaxy_workspace_test#119 → `f7c9f6d3`, closing autogalaxy_workspace_test#118, merged 2026-09-07. One of six corrective PRs shipped 2026-09-07 under the human-authorised Heart RED corrective-PR exception (reasons: `release validation FAILED (stage integrate)` and `workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)`). Fable session planned; Opus subagents implemented per task; merged via /prm the same day. Validation of the RED clearing is the next scheduled Workspace Smoke and Release Integrate runs on fresh wheels. **Containment, not a fix** — the human ratified the quarantine; remove the entry when the epic lands.

- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/118
- completed: 2026-09-07
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/119
- corrective-red: authorization https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/118#issuecomment-5573412233
- epic: xla-cpu-eigen-pool-deadlock (fifth member; sibling `rectangular.py` and three autolens_workspace_test scripts already quarantined)

## What shipped
- `config/build/no_run.yaml`: forensic `NEEDS_FIX 2026-09-07` entry for `multi_dataset/jax_likelihood/delaunay.py` citing runs 34018429178 and 34094964905, the execution-stage stack, the falsified hypotheses and the local repeat counts. Script stays on the smoke gate.

## Key traps / findings
- The prompt's premise ("a release-profile setting triggers it") is false: the resolved env differs in 2 of 68 keys (`PYAUTO_TEST_MODE`, `PYAUTO_FAST_PLOTS`), neither read by a script that runs no search and draws no plots. The original witness was unsatisfiable.
- CI artifacts: both hangs park in `_pjit_call_impl` via `vmap_f → _pjit_batcher` — execution, not compilation — on the first `_vmap` call (run 34018429178) and the second (run 34094964905, after the first completed in 4.1 s). `Fitness._vmap = jax.vmap(jax.jit(call))` re-traces and eagerly executes the batched pjit on every call, so each script gets two exposures. Library lever filed: `draft/refactor/autofit/fitness_vmap_outer_jit_halves_eigen_pool_exposure.md`.
- The dev box cannot reproduce the family at all: 10/10 release passes and 4/4 with the Eigen flag REMOVED (the configuration that hangs 14/16 in CI), so local negatives carry no information. The mesh/mask-ratio hypothesis is falsified: `delaunay_mge.py` has the identical geometry (500 mesh / 716 px) and passes.

## Original prompt

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
