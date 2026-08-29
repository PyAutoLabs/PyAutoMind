# Pair JAX/XLA env vars with measured compile and run times, per backend

Type: research
Target: PyAutoNerves
Repos:
- autogalaxy_workspace_test
- autolens_workspace_test
- PyAutoNerves
- workspaces
Themes:
- jax-compile
- profiling
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

# Pair JAX/XLA env vars with measured compile and run times, per backend

Type: research
Target: autonerves
Repos:
- @PyAutoNerves
- @autolens_workspace_test
- @autogalaxy_workspace_test
Difficulty: too-large
Autonomy: supervised
Priority: high

## Why this exists

`complete/2026/08/xla-cpu-eigen-pool-deadlock.md` root-caused a real hang:
`xla::cpu::FftThunk::Execute` runs on an Eigen intra-op pool worker and hands
ducc0 that same pool, which fans the transform back into it and deadlocks. The
avoidance is `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false`, which costs ~15%.

Two things that campaign exposed, neither of which it fixed:

1. **The flag is CI-only.** It lives in `config/build/profile_{smoke,release}.yaml`
   of the two test workspaces. No library sets it — verified against a fully
   installed stack: zero hits for `xla_cpu_multi_thread_eigen` anywhere in
   site-packages. So a **real science run on CPU has neither the protection nor
   the 15%**, while CI pays the 15% on every JAX script. Both halves of that are
   chosen by accident rather than by measurement.
2. **Nobody has measured which JAX/XLA env vars actually matter.** `autonerves/
   jax_wrapper.py` already manages `XLA_FLAGS` — it sets
   `--xla_disable_hlo_passes=constant_folding` and `--xla_gpu_autotune_level=0`
   — so there is a place a measured default belongs. Those two were set for
   reasons that were true when written; neither has a current number attached,
   and the eigen flag was added to CI without one either.

## The question

For each backend (CPU and GPU) and each candidate env var, what does it do to
**compile time** and to **execution time**, separately? Those two are different
budgets — this stack has repeatedly optimised one while paying in the other, and
the epic that produced this task spent a month with a hang misnamed a "compile
stall" precisely because they were not measured apart.

## Scope

Sweep candidate env vars across representative JAX likelihood scripts, record
compile and run time separately per backend, and produce a **recommended default
set per backend** with the measurement behind each entry. Candidates at least:

- `--xla_cpu_multi_thread_eigen` (the incident flag; CPU)
- `--xla_disable_hlo_passes=constant_folding` (already set; unmeasured)
- `--xla_gpu_autotune_level` (already set to 0; unmeasured)
- `JAX_COMPILATION_CACHE_DIR` / the persistent cache (on by default for a while
  now; its effect on a warm vs cold runner is unquantified)
- `JAX_ENABLE_X64` (correctness-bearing, but the cost is unrecorded)
- thread-pool sizing knobs, and process CPU affinity, which the incident showed
  changes behaviour even when no env var does

## The constraint that shapes the plan

**GPU measurement cannot run in GitHub Actions** — there are no GPU runners. The
GPU leg has to go through the RAL HPC `gpu` partition via the project's
`hpc/sync push-submit gpu` path, which is a different harness, a different
cadence and a different results-ingest from the CPU leg. Plan the two legs as
separate phases rather than assuming one sweep covers both; a design that only
works on GitHub runners silently answers half the question.

## Suggested phasing

Sized `too-large` deliberately — split at start_dev.

1. **CPU sweep harness + baseline.** Extend or sibling the `retime.py` harness,
   which already has `--arm` for env overlays dealt round-robin within one
   dispatch (added by the incident above). Record compile and run time
   separately. Deliverable: a per-var CPU table.
2. **GPU sweep** via `hpc/sync push-submit gpu`, same measurements, GPU-relevant
   vars. Deliverable: a per-var GPU table.
3. **Decide and land the defaults** in `autonerves/jax_wrapper.py`, per backend,
   each with its number. Includes the decision on whether the eigen flag becomes
   a user-facing CPU default — which is the science-run exposure question — and
   whether CI should keep paying 15% on scripts that never trip the deadlock.

## Do not re-measure

Established by the incident and in its record; re-running these is waste:

- The eigen flag's *effect on the deadlock* is settled: standalone reproducer
  hangs 0/8 by default and 8/8 with the flag, Fisher p = 0.000155; on the real
  script, pool of 4 hung 5/6 and pool of 1 passed 6/6.
- Its cost on `imaging/jax_likelihood/mge_group.py` is ~15% (62.3s vs 54.4s).
- The persistent compilation cache is **not** the deadlock's cause (6/6 hangs
  with it disabled) — that says nothing about its *timing* effect, which is what
  this task should measure.
- There is no CFS quota on `ubuntu-latest`, so pool mis-sizing against a cgroup
  quota is not a live variable there.

## Acceptance

- A per-backend table: env var x {compile time, run time}, with the script set
  and repeat count stated, and a re-measured control (the incident's own lesson:
  timings and hang rates wander, so before/after is not evidence — ABAB is).
- A recommended default set per backend, each entry carrying its number.
- An explicit decision on the CPU eigen flag for science runs: made a library
  default, left CI-only, or documented for users — with the reason and the cost.
- Whatever is decided is landed, not just written down.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-0/-home-user/fa910b96-e557-5368-a11e-13292ea18dec/scratchpad/intake_raw.md -->
