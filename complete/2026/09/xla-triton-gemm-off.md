## xla-triton-gemm-off
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/161
- completed: 2026-09-08
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/162 (merge 0e7163bc)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/230 (merge fb532c01)
- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/162
- summary: |
    `autonerves/jax_wrapper.py` keeps its default `--xla_gpu_autotune_level=0` (cold-compile time) and, in
    the same block, now also appends `--xla_gpu_enable_triton_gemm=false` unless the user pre-set the Triton
    flag; an explicit autotune level leaves Triton GEMM to XLA, where it is autotuned against cuBLAS. With
    autotuning off XLA otherwise lowers dense fp64 dots to a Triton fusion with an un-tuned default tile:
    the pixelized-inversion curvature matrix (15361x1560) took 25.5 ms on the A100 against 4.8 ms for
    cuBLASLt. The new flag reaches cuBLAS with 0.07 s of compile and results bit-identical to the old
    default. Log message rewritten; tests extended (183 pass).
- reconfirmation: |
    The filed prompt claimed the bug from a single 2026-09-05 A/B (F 25.63 vs 4.90 ms) that four later
    level-0 runs contradicted (F 4.8 ms). The user asked for reconfirmation before any edit. Read-only
    evidence could not separate the flag from cluster state, so a pure-jax five-arm probe ran on one A100
    with a fresh `JAX_COMPILATION_CACHE_DIR` per arm (RAL job 342333): level 0 fresh 25.5 ms (Triton),
    level 4 fresh 4.9 ms (cuBLASLt), level 0 on the level-4 cache 4.8 ms, level 0 on its own cache 25.5 ms,
    level 0 + Triton GEMM off 4.8 ms. The prompt's proposed cure (drop level 0) was replaced by the cheaper
    one arm E measured, chosen by the user.
- trap: |
    JAX persists XLA's per-fusion autotune cache next to the compilation cache by default
    (`jax_persistent_cache_enable_xla_caches`), keyed by fusion fingerprint and not by the autotune flag.
    RAL `$HOME` is node-local, so one level-4 run seeds a node and every later level-0 run there inherits
    the cuBLAS choice. An autotune A/B is only valid with a fresh cache dir per arm or on an untouched
    node; the F compile time is the tell (~2 s autotuned, ~0.4 s Triton default, ~0.07 s cuBLAS or a
    cache hit). `device.xla_flags` in a JSON proves the flag reached the env, never which kernel ran.
- workspace: |
    autolens_profiling gains `scripts/misc/jax_compile/gemm_probe.py`,
    `hpc/batch_gpu/submit_xla_autotune_gemm_probe`, `results/notes/xla_autotune_triton_gemm.md`, a corrected
    README "Settings suffice" bullet, an amendment to the jax_compile close-out and an addendum to the
    delaunay_nn_breakdown autotune A/B section. CI lint failed once on the new probe (import order, `%`
    formats, ruff format); fixed on the branch before merge. Smoke not runnable locally (GPU/SLURM probe;
    autolens_profiling has no smoke harness entry).
- heart: |
    Shipped under an acknowledged YELLOW: "workspace validation not passing (5 failed, 2 timeout,
    cloud#34099198772 ...)" and "release validation incomplete: no rehearsal for current source";
    organism-scope, neither touching PyAutoNerves or autolens_profiling. Not frozen at merge.
- follow-ups: |
    Witness still to run on RAL after `HPCPullPyAuto` syncs the merged Nerves main: a fresh-cache
    `submit_breakdown_imaging_delaunay_a100_hst_fp64` run with F < 6 ms, `curvature_matrix_jit_compile`
    < 0.2 s and `--xla_gpu_enable_triton_gemm=false` in `device.xla_flags`. Filed as
    `draft/research/autolens_profiling/rerun_a100_fp64_delaunay_rows_fixed_xla_default.md`, which also
    reruns the four `hpc_a100_fp64` Delaunay/DelaunayNN dashboard cells so the dashboard does not straddle
    the flag change. Bug Agent gap: it classified this library defect as workspace-owned from mention
    counts (owner=autolens_profiling, confidence low); a fix-locus rule for env-var defaults set in
    PyAutoNerves would route it right.

## Original prompt

# `--xla_gpu_autotune_level=0` default lowers the fp64 curvature GEMM to a slow Triton kernel (5x) on the A100

Type: bug
Target: autonerves
Repos:
- PyAutoNerves
- autolens_profiling
Themes:
- jax-gpu
- performance
- hpc
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: a fresh-cache A100 Delaunay breakdown run (JAX_COMPILATION_CACHE_DIR pointed at an empty dir) with the library defaults reports "Curvature matrix (F)" under 6 ms, curvature_matrix_jit_compile under 0.2 s, and the JSON's device.xla_flags contains --xla_gpu_enable_triton_gemm=false
Review-minutes: 10
Unattended: ready
Filed: 2026-09-05
Issued: 2026-09-08

`PyAutoNerves/autonerves/jax_wrapper.py` (lines 58-73, introduced in e8d5842 on
2026-07-17, "enable JAX persistent compilation cache by default + fix XLA_FLAGS clobber")
appends `--xla_gpu_autotune_level=0` to `XLA_FLAGS` whenever no explicit level is set,
with the rationale that autotuning "dominates cold JAX compile times on GPU (measured up
to ~7 minutes for a single fusion) while giving no measurable evaluation speed-up on
PyAuto likelihoods". The compile-time half of that rationale still holds; the evaluation
half does not, because turning autotuning off also changes which kernel XLA emits for a
dense fp64 matrix product.

## Reconfirmation (2026-09-08, RAL job 342333)

A five-arm pure-JAX probe on the RAL A100 (node euclid-ral-gpu-2, A100 80GB PCIe, jax
0.10.2), each arm given its own fresh `JAX_COMPILATION_CACHE_DIR`, timing the dense fp64
GEMM at the heart of the curvature matrix F (15361x1560):

| arm | flags | cache | F (ms) | compile (s) | lowering |
|---|---|---|---:|---:|---|
| A | level 0 (current default) | fresh | 25.523 | 0.461 | Triton `__triton_nested_gemm_fusion` (num_warps=2, tiles [16,8]) |
| B | level 4 (XLA default) | fresh | 4.918 | 2.080 | cuBLASLt algorithm 1 |
| C | level 0 | reads B's cache | 4.832 | 0.072 | cuBLASLt algorithm 1 (read `xla_gpu_per_fusion_autotune_cache_dir`, 3 entries) |
| D | level 0 | own cache | 25.510 | 0.005 | Triton (executable-cache hit; writes 0 autotune entries) |
| E | level 0 + `--xla_gpu_enable_triton_gemm=false` | fresh | 4.789 | 0.074 | cuBLASLt algorithm 1 |

F[0,0] is bit-identical across A/D/E; B/C differ by ~2 ULP. Arm E is the fix: it keeps
the cold-compile win of level 0 (0.074 s vs 2.080 s for level 4) and recovers the full
cuBLAS GEMM speed, with results bit-identical to today's level-0 output.

The mechanism is that JAX persists XLA's per-fusion autotune cache next to the
compilation cache by default (`jax_persistent_cache_enable_xla_caches` sets
`xla_gpu_per_fusion_autotune_cache_dir`), and that cache is keyed by fusion fingerprint,
not by the autotune flag. RAL `$HOME` is node-local, so the 2026-09-05 level-4 jobs
seeded gpu-2's cache, and **every level-0 run on gpu-2 after 09-05 read that seeded cache**
(342315, 342316, 342321, 342322 all report F at 4.8 ms) and therefore looked as if the
default had been fixed. The original A/B in this prompt (jobs 342277 vs 342282, F 25.63
vs 4.90 ms) was itself valid only because it predated any level-4 run on that node; any
later repeat of it on a seeded node is confounded.

## Fix

1. In the same default block that appends `--xla_gpu_autotune_level=0`, also append
   `--xla_gpu_enable_triton_gemm=false` unless `--xla_gpu_enable_triton_gemm` is already
   present in `XLA_FLAGS`. An explicit autotune level is respected as before, and in that
   case Triton GEMM is left to XLA (it is autotuned against cuBLAS there).
2. Rewrite the `logger.info` message that describes the default, and the
   `test_autonerves/test_jax_wrapper.py` tests that cover it.
3. autolens_profiling: add the probe script and its submit script, a results note, correct
   the README bullet and the `jax_compile` README close-out, and add an addendum to the
   A/B section of `results/notes/delaunay_nn_breakdown.md`.
4. Verification per the Witness above: a fresh-cache A100 run post-merge on RAL.

## Downstream

The `hpc_a100_fp64` dashboard rows in autolens_profiling recorded between 2026-07-17 and
2026-09-08 are systematically slow on every GEMM-bound step, *unless* the node's per-fusion
autotune cache happened to be seeded by an earlier level-4 run — so those rows are not
merely slow, they are inconsistent with each other. After the fix lands, the
Delaunay/DelaunayNN breakdown and runtime rows should be re-run so the dashboard is not
comparing across the flag change; the `_autotune4` rows from PR #221 are the reference.
