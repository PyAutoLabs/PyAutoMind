# Keep caches off `$HOME` on HPC — phase 2 remainder: euclid pipeline `activate.sh`

Type: maintenance
Target: workspaces
Repos:
- euclid_strong_lens_modeling_pipeline
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Blocked-by: draft/bug/euclid/latent_total_source_flux_jax_vs_numpy_regression.md — euclid_strong_lens_modeling_pipeline main CI "Tests" red since a89a468 (2026-09-25; last green 3130898, 2026-09-22) on `tests/test_compute_latent_variable.py::test_latent_euclid_variables_traces_under_jax_jit`
Witness: `bash -n activate.sh`; fake-base witness (source `activate.sh` with a fake `PYAUTO_HPC_BASE`: every cache variable lands under `${PYAUTO_HPC_CACHE:-$(dirname "$PYAUTO_HPC_BASE")/.cache}`, a preset `JAX_COMPILATION_CACHE_DIR` wins, an explicitly empty one stays empty, and it survives `set -e` as a SLURM script would run it); repo pytest green.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-25

## What

The euclid half of `hpc-cache-off-home-phase2` (autolens_profiling#310), re-filed at
the partial-merge close-out on 2026-09-25 — record:
`complete/2026/09/hpc-cache-off-home-phase2.md` (autolens_profiling half shipped as
autolens_profiling#311). Apply phase 1's cache block to the `PYAUTO_HPC_BASE` branch of
`euclid_strong_lens_modeling_pipeline/activate.sh` — the block below, identical to
autolens_assistant's. Only `activate.sh` changes.

It was held, not rejected: the patch passed `bash -n` and the fake-base witness, but the
repo's pytest fails on the branch AND on main (`total_source_flux` 3.511 under
`jax.jit` vs 3.320 eager, rel=1e-3) — unrelated to `activate.sh`, which no test
sources. Ship once the bug above has turned main green (or on a human call to push
onto a red main with an override).

The commit also survives as `a7f0d0a` on the local branch
`feature/hpc-cache-off-home-p2` of the canonical `lens/euclid_strong_lens_modeling_pipeline`
checkout (never pushed); cherry-pick it or apply the patch below onto current main.

Parallel claim: `vis-lp-inspection-bundle` (feature/vis-lp-inspection-bundle) also
claims this repo; its diff (catalogue/, scripts/build_inspection_bundle.sh,
scripts/tools/build_inspect.py, hpc/batch_cpu/submit_build_inspection_bundle, tests/,
READMEs) does not touch `activate.sh` — a parallel claim is fine.

## Ready patch (a7f0d0a)

```diff
From a7f0d0a223971eb26171d7d65aaef55106adb902 Mon Sep 17 00:00:00 2001
From: Jammy2211 <JNightingale2211@gmail.com>
Date: Fri, 25 Sep 2026 21:08:41 +0100
Subject: [PATCH] maintenance: keep Python/JAX caches off $HOME on HPC
 (autolens_profiling#310)

Phase 2 of autolens_inference#13 (RAL admin, 2026-09-25: ~/.cache filling node root
disks). The PYAUTO_HPC_BASE branch of activate.sh now carries phase 1's cache block
(verbatim from autolens_assistant): every cache variable lands under
${PYAUTO_HPC_CACHE:-$(dirname "$PYAUTO_HPC_BASE")/.cache}, filling only unset variables.
Laptop .venv users never reach this branch.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
---
 activate.sh | 19 +++++++++++++++++++
 1 file changed, 19 insertions(+)

diff --git a/activate.sh b/activate.sh
index e2ca106..b2a8eb7 100644
--- a/activate.sh
+++ b/activate.sh
@@ -23,6 +23,25 @@ $BASE/PyAutoFit:\
 $BASE/PyAutoArray:\
 $BASE/PyAutoGalaxy:\
 $BASE/PyAutoLens
+    # --- Keep caches OFF $HOME on HPC ---------------------------------------
+    # On many clusters (RAL: every node) /home sits on a small root disk, so tools that
+    # default to ~/.cache — the PyAutoNerves JAX compile cache (~/.cache/pyauto_jax), pip,
+    # matplotlib, numba, CUDA/Triton kernels — fill it and break the node (RAL admin,
+    # 2026-09-25). Send them to the shared project filesystem instead: by default a
+    # `.cache/` next to PYAUTO_HPC_BASE (override with PYAUTO_HPC_CACHE). Only unset
+    # variables are filled, so a submit script's own JAX_COMPILATION_CACHE_DIR still wins
+    # (and an explicitly EMPTY one still disables the JAX cache). Laptop `.venv` users
+    # never reach this branch.
+    export PYAUTO_HPC_CACHE="${PYAUTO_HPC_CACHE:-$(dirname "$PYAUTO_HPC_BASE")/.cache}"
+    mkdir -p "$PYAUTO_HPC_CACHE" 2>/dev/null || true
+    export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$PYAUTO_HPC_CACHE}"
+    export PIP_CACHE_DIR="${PIP_CACHE_DIR:-$PYAUTO_HPC_CACHE/pip}"
+    export MPLCONFIGDIR="${MPLCONFIGDIR:-$PYAUTO_HPC_CACHE/matplotlib}"
+    export NUMBA_CACHE_DIR="${NUMBA_CACHE_DIR:-$PYAUTO_HPC_CACHE/numba}"
+    export CUDA_CACHE_PATH="${CUDA_CACHE_PATH:-$PYAUTO_HPC_CACHE/nv}"
+    export TRITON_CACHE_DIR="${TRITON_CACHE_DIR:-$PYAUTO_HPC_CACHE/triton}"
+    export JAX_COMPILATION_CACHE_DIR="${JAX_COMPILATION_CACHE_DIR-$PYAUTO_HPC_CACHE/pyauto_jax}"
+    export ASTROPY_CACHE_DIR="${ASTROPY_CACHE_DIR:-$PYAUTO_HPC_CACHE/astropy}"
 else
     echo "No local .venv found (set PYAUTO_HPC_BASE for a shared/HPC PyAuto checkout)." >&2
 fi
-- 
2.34.1

```
