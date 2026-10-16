# Python Version Matrix smoke legs bypass run_smoke.py — no ENV declarations, no profile env, no per-script cap (6h XLA vmap hangs + witt_wynne failure)

Type: bug
Target: pyautohands
Repos:
- PyAutoHands
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issued: 2026-10-16
Consequence: glance
Witness: A dispatched `Python Version Matrix` run on main completes all legs (3.12/3.13/3.14 × autofit/autogalaxy/autolens) in under 60 min with `guides/misc/witt_wynne.py` passing, and the smoke step invokes `<ws>/.github/scripts/run_smoke.py` (visible in the job log), not a bash `python scripts/$script` loop.
Filed: 2026-10-16

## Finding (health session 2026-10-16, read-only diagnosis)

`organs/PyAutoHands/.github/workflows/python_matrix.yml:117-140` runs smoke scripts with its own bash loop over `smoke_tests.txt` and a hard env block (`:83-89`: PYAUTO_TEST_MODE=1, SMALL_DATASETS=1, FAST_PLOTS=1). It never goes through `run_smoke.py` → `autohands/run_python.py`, so it loses profile_smoke.yaml (TEST_MODE=2, DISABLE_JAX=1), per-script `ENV:` declarations, the per-script timeout + process-group kill and the report.

1. **6h cancellations (09-21, 09-28, 10-05, 10-12)** — only autolens_workspace legs; each wedged ~350 min in a Nautilus+JAX vmap fit (`shapelets/modeling.py`, `extra_galaxies/modeling.py`, `scaling_relation/modeling.py`; varies by leg) at `autofit/non_linear/jax_compile.py:249 _block_until_ready`, "still waiting for the result to materialize" ×~700. This is the known XLA CPU Eigen thread-pool wedge (complete/2026/08/jax-vmap-materialisation-hang.md; workaround `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false`). The matrix runs it because TEST_MODE=1 + JAX on, with no cap.
2. **witt_wynne.py fails only here** (run 38235988094, jobs 114766665351/114766665487): it declares `ENV: full_datasets` (autohands/env_config.py:94 unsets SMALL_DATASETS); the loop ignores it.
3. **3.13 install failure** (job 108867068107): `[optional]` extras → tfp-nightly → dm-tree has no 3.13 wheel; smoke_install.sh already gates `[optional]` to 3.12. unit_tests leg installs `[optional]` on 3.13/3.14 too.

## Proposed fix (Hands only)

Replace the bash loop + env block with the workspace harness: check out PyAutoHands beside the workspace, `PYTHON_VERSION=… bash <ws>/.github/scripts/smoke_install.sh`, then `PYTHONPATH=PyAutoHands/autohands python <ws>/.github/scripts/run_smoke.py --report-dir …`. If the matrix intends real JAX fits, add `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false` as the *_workspace_test profiles do. Do not raise timeouts or skip scripts. Gate the unit_tests `[optional]` install by version the same way.

Evidence logs: health-session scratch (not retained); job IDs above.
