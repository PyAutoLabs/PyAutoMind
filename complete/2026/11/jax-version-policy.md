# JAX version policy and the recurring XLA:CPU deadlocks

Research, PyAutoNerves#213 (closed 2026-11-11). Tier glance; Heart RED development override at
start (human, 2026-11-10), YELLOW acknowledged at ship (2026-11-11).

## What shipped
- PyAutoLabs/PyAutoDNA#5 (ad0242fc): `PyAutoDNA` research validation authority (shown, can block
  promotion, never satisfies it); `dna import-matrix`; public XLA-option allowlist; JAX CPU
  policy panel + yellow item for an observed environment on a hanging setup; decision
  `decisions/jax-cpu-policy-2026-11.md` (supersedes jax-2026-10-04); public records.
- PyAutoLabs/autolens_profiling#527 (a66136c4): `scripts/misc/jax_version_policy/`
  (hang_case, library_case, run_matrix, export_reproducers, make_venvs) +
  `hpc/batch_cpu/submit_jax_version_policy_hang_matrix_ral_cpu`.

## Findings
- jax/jaxlib 0.11.2 (users' resolved version) deadlocks XLA:CPU likelihoods with no flag. RAL
  415009 (600 cells, 180,000 calls): 25/25 cells hung at 4 cores (first call), 0/25 at 16;
  laptop (8 cores) intermittent (call 1-94), including Delaunay through the library with the
  PyAutoNerves default flags.
- jax 0.12.0 / 0.12.0.1: 0 hangs in 30,000 calls, no flag. FFT part = jax-ml/jax#41265, fixed by
  openxla/xla#50091 in 0.12.0; no upstream issue needed for the MGE hang.
- Eigen flag on 0.12: free for MGE, +18 % (4 cores) to ~+50 % (16 cores) on rectangular;
  scheduler flag 1.5-2x on MGE. The LAPACK case never reproduced #274, even on 0.10.2.

## Decision (human-approved 2026-11-11)
Floor `jax>=0.12.0,<0.13` and `jaxlib>=0.12.0,<0.13` after a Heart validation on 0.12; no
default XLA:CPU flag. Release-chat prompt: Science/scratch/jax_version_policy/release_prompt.md.

## Follow-ups (Mind drafts, 36a06b3f9)
- draft/feature/autonerves/raise_jax_floor_to_0_12.md (release-coupled)
- draft/feature/pyautoheart/jax_cpu_hang_guard_writes_dna.md
- draft/maintenance/workspaces/remove_xla_eigen_flag_workarounds_after_jax_0_12.md
- draft/docs/pyautopulse/point_xla_deadlock_notes_at_dna_policy.md

## Original prompt

# JAX version policy and the recurring XLA:CPU deadlocks: what is the general…

Type: research
Target: PyAutoNerves
Repos:
- autolens_profiling
- PyAutoNerves
- HowToLens
- PyAutoHeart
- PyAutoPulse
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-11-10
Consequence: glance
Witness: a written recommendation (one policy covering JAX version range + any default XLA flags) backed by a repro matrix: each candidate jax/jaxlib version x flag setting, run on the laptop and a RAL CPU node, records hang / no-hang over N repeated calls of the known reproducers, plus per-call cost of the flag on at least one MGE and one pixelized likelihood.
Review-minutes: 3
Unattended: needs-slicing
Lane: ral

Human request (2026-11-10): "make this more general research on what to do with JAX version and what might be the most general sensible solution". Raised while regenerating HowToLens#130 stored results on RAL, where tutorials 4 and 6 deadlocked at 0 % CPU.

## The problem: the same bug class keeps being patched locally

XLA:CPU on JAX CPU hangs: a compiled (often vmapped) executable runs, then a later call never returns, process at 0 % CPU (futex wait in `CpuPjRtRawLoadedExecutable::Execute` → `tsl::BlockUntilReady` → `absl::Mutex`). Every fix so far has been scoped to one place; no fix reaches users' installs.

| When | Where seen | Fix | Scope |
|---|---|---|---|
| 2026-09 | 4-core containers, vmap ("intra-op thread-pool starvation") — Mind complete/2026/09/mge-jit-regression-rebaseline.md, jax-import-order-x64.md, jit-visualization-outputs.md | `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false` | container/CI only |
| 2026-10-04 | CPU batched LAPACK (Cholesky) on jax 0.10.x / 0.11.0 — PyAutoHeart#274 | PyAutoNerves `249ba9e`: `jax>=0.7.0,<0.12.0,!=0.10.*,!=0.11.0` (+ README "JAX compatibility") | everyone |
| 2026-10-05 | CPU FFT pool deadlock in release validation | PyAutoHeart `ad9bbc4`: eigen flag in workspace-validation release mode, release-diagnostic, jax-compatibility; test asserts smoke mode does NOT set it | Heart release legs only |
| 2026-10-29 | likelihood-lifecycle 2d: every JAX CPU cell on jaxlib 0.11.2 (MGE, rectangular, Delaunay) — decision D12 | eigen flag in `scripts/misc/likelihood_breakdown/galaxy_group_standard.py` (`XLA_CPU_WORKAROUND_FLAG`) | autolens_profiling only |
| 2026-11-10 | HowToLens ch2 tutorials 4 (MGE) and 6 (MultiStartProdigy) on RAL, jaxlib 0.11.2 | eigen flag in the private RAL job script | one task |

Key facts:
- PyAutoNerves names **0.11.2 the "recommended validation baseline"** and it is what users resolve today (laptop and RAL venvs are jax/jaxlib 0.11.2), yet 0.11.2 has the 2d/HowToLens deadlock. The 0.10/0.11.0 exclusion fixed a different (LAPACK) path.
- **jax/jaxlib 0.12.0 and 0.12.0.1 are on PyPI** and excluded by the `<0.12.0` cap. Untested whether they fix either path.
- PyAutoNerves `autonerves/jax_wrapper.py` already edits `XLA_FLAGS` before JAX starts (appends `--xla_disable_hlo_passes=constant_folding`, `--xla_gpu_autotune_level=0`, Triton GEMM off), env-respecting — a natural home for a CPU flag if that is the answer.
- Known reproducer with no PyAuto code: PyAutoPulse `knowledge/xla_cpu_deadlock_jaxlib_0_11_2.md` (exported group MGE prefix-3 function, hangs ~call 14 by default, 300 calls fine with either flag). Decision record: PyAutoPulse `decisions/xla-cpu-deadlock-eigen-workaround.md`.
- Two flags avoid it: `--xla_cpu_multi_thread_eigen=false` (D12 chose it; ~+25 % per call vs default on group/mge, ~2x faster than the alternative on MGE) and `--xla_cpu_enable_concurrency_optimized_scheduler=false`.
- Hang is intermittent (call 1 to ~35): short smokes and test mode pass by luck. Smoke tests run in test mode and never hit it; readers running tutorials live (HowToLens ch2 tutorial 1 runs a real JAX search) are exposed.
- Prior human constraint (CI timing epic): keep the eigen flag and the Eigen-pool bug-class reproduction (jax-compile-stall epic in epics.md).

## Questions to answer
1. Do jax/jaxlib 0.12.0 / 0.12.0.1 fix the 0.11.2 XLA:CPU deadlock (Pulse reproducer + one real tutorial fit) and the PyAutoHeart#274 LAPACK path? Any upstream JAX issue / fix commit?
2. Which versions in the allowed range are actually safe on CPU, with and without each flag? Is "recommended baseline 0.11.2" still right?
3. Is a library default (e.g. PyAutoNerves `jax_wrapper` appending a CPU-only XLA flag, skipped when the platform is GPU, never overriding a user's explicit setting) the most general fix? Cost across likelihood families (MGE, rectangular, Delaunay, interferometer, point source), CPU core counts (4 vs 8 vs RAL nodes), and fp64.
4. Alternatives: pin/cap changes (exclude 0.11.2, move to 0.12.x, raise the floor), the scheduler flag instead, per-feature workarounds, or documentation only. Interaction with the GPU path (flag inert? D12 2d fix skipped it for cuda).
5. How should this be guarded so it stops recurring: a Heart check that runs a known reproducer for N calls on each allowed jax version, rather than test-mode smokes.
6. Should an upstream JAX issue be filed (the Pulse reproducer's exported module is the evidence)?

## Deliverable
A short decision page (PyAutoPulse knowledge/decision or Nerves README section) with the repro matrix, a recommended single policy, and follow-up implementation prompts (library change, pin change, Heart guard, docs). Research only: no library change in this task.

## Constraints
- Laptop for short pilots only; repeated-call matrices longer than ~30 min go to a RAL array per the no-long-laptop-runs rule (private checkout, never the shared install).
- Measure through `pyauto-brain profiling` conventions where timing rows are recorded.

<!-- formalised by the Intake (Conception) Agent on 2026-11-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5ee98b5f-b187-4b0a-83a9-3ad898ce13b8/scratchpad/jax_policy.md -->
