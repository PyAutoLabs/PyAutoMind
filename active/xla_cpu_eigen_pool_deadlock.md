# Why does XLA CPU's Eigen thread pool wedge on the multi_dataset vmap graphs?

Type: research
Target: ci
Repos:
- @PyAutoFit
- @autolens_workspace_test
- @autogalaxy_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-08-27
Issued: 2026-08-27

## Why this exists

`complete/2026/08/jax-vmap-materialisation-hang.md` shipped a **workaround, not
a root cause**. We know *where* it hangs and *what* avoids it:

- the hang is materialising a vmap result — stacks at
  `jax.block_until_ready`/`try_to_block` and at `jax.Array._value` via
  `__str__`, with compilation finished ~12-18s earlier;
- `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false` avoids it, ABAB, 12 passes /
  0 hangs against 2 passes / 14 hangs (Fisher exact p ~ 3e-6).

We do **not** know why the pool wedges. `faulthandler` reports Python frames
only, so the wedged XLA worker threads are exactly the part still invisible.

Two costs of leaving it here. Every JAX script in both test workspaces now runs
single-threaded Eigen, ~15% slower on the heaviest; and the flag is a load-bearing
line whose removal silently brings back seven quarantines.

## The questions, in order

1. **A native stack from the wedged threads.** `faulthandler` cannot see them.
   Attach `gdb -p` (`thread apply all bt`) or `py-spy dump --native` to a hung
   process. Where in XLA's runtime are the workers parked — a condition variable
   in the Eigen pool, a work-queue steal loop, a barrier?
2. **A minimal reproducer outside the workspace.** Strip to the smallest jaxpr
   that still wedges: how much of the `multi_dataset` composition is needed, and
   does batch size or vmap axis count move the probability? A standalone script
   is what an upstream report needs.
3. **CPU count versus cgroup quota.** The likeliest mechanism, and untested. A
   hosted runner advertises more CPUs than the container can schedule, so a pool
   sized from `nproc` can oversubscribe and deadlock. Compare
   `os.cpu_count()` / `os.sched_getaffinity` / `/sys/fs/cgroup/cpu.max` on a
   runner, and A/B `--xla_cpu_multi_thread_eigen=true` with the pool sized to
   the real quota. If this is it, the fix is sizing the pool correctly rather
   than disabling threading, and the ~15% comes back.
4. **Upstream.** File with JAX/XLA once 1-3 give a reproducer and a native
   stack. Link the report from both workspaces' `no_run.yaml` block comments.

## Do not repeat

Refuted in phase 3, with evidence in the record: the persistent compilation
cache; the jax/jaxlib version (identical `0.11.1` stack on the day it hung 3/3
on both legs); the 3.12-vs-3.13 split. Do not re-run these.

## Method notes that cost a day to learn

- **The hang rate wanders.** The same script passed 2/2 and hung 2/2 on the
  identical commit hours apart. Any claim needs ABAB against a re-measured
  control, never before/after.
- The dispatchable harness is `retime.yml` in either workspace; its `STALL` /
  `NEITHER` verdicts are the classifier to quote.
- CI picks up library branches by **matching branch name** across the dependency
  chain, so an experiment needs the same branch name in every repo it touches.

## FOUND (2026-08-27, run 33099502356) — questions 1 and 3 are answered

**The wedge is a re-entrant thread-pool deadlock in XLA CPU's `FftThunk`, not
oversubscription.** 11 hangs / 12 runs, and 11 of 11 native dumps carry the
identical signature — every dump, not a sample.

All four `tf_XLAEigen` workers are parked here (frames trimmed):

```
#4  absl::CondVar::WaitCommon
#5  ducc0::detail_threading::latch::wait()
#8  ducc0::detail_threading::execParallel(...)
#11 ducc0::google::r2c<double>(..., Eigen::ThreadPoolInterface*)
#12 xla::cpu::FftThunk::Execute(xla::cpu::Thunk::ExecuteParams const&)
#16 Eigen::ThreadPoolTempl<tsl::thread::EigenEnvironment>::WorkerLoop(int)
```

Frames 16 and 11 are the bug. `FftThunk` runs **on** an Eigen pool worker and
hands ducc0 that same pool; ducc0 fans the FFT back **into the pool it is
already running on** and blocks on a latch waiting for sub-tasks that need a
free worker. Four workers, four concurrent FFT thunks, every worker waiting
for a worker. All 26 threads in `futex_do_wait` — nothing spinning, which is
why a month of wall-clock evidence read as "no progress" rather than "slow".

The main thread is the door #1528 already knew: `jax::PyArray::BlockUntilReady`
-> `jax::AwaitBuffersReady` -> `absl::Notification::WaitForNotificationWithTimeout`.

This accounts for every previously unexplained feature: the flag works because
without a pool `FftThunk` runs inline; the rate wanders because saturating all
workers at once is a scheduling race; only the composite multi_dataset/MGE-group
graphs reach it because they carry the most concurrent FFT convolutions; and the
compile always finished first because FFT thunks execute at execution time.

**Question 3 answered: NO.** The topology banner, identical on both legs —
`os.cpu_count()` 4, `sched_getaffinity` 4, `/proc/cpuinfo` 4,
`cpuset.cpus.effective` 0-3, and `cpu.max` **absent**: no CFS quota in force on
`ubuntu-latest`. The pool is sized correctly and the runner advertises nothing it
cannot schedule. So `affinity=auto` was a measured no-op (the banner says so
rather than letting a null read as a result), the twelve runs are twelve
controls, and **the ~15% is NOT recoverable by sizing the pool** — only by an
upstream fix or by keeping these graphs off the FFT convolution path. The flag
stays.

Recorded on the issue: PyAutoFit#1530 (comment 5443451389). Job logs expire in
90 days; the stacks are quoted there and here.

### Still open

- **Q2 minimal reproducer** — much smaller than first scoped. Not "strip the
  multi_dataset composition": just enough concurrent FFT-backed convolutions
  under vmap to saturate the intra-op pool, batch >= `os.cpu_count()`.
- **Q4 upstream** — actionable now; the reproducer is what makes it land.
- **One cheap confirmation first.** If the deadlock needs concurrent FFT thunks
  >= pool size, pinning to one CPU must pass:
  `--arm one:XLA_FLAGS=,affinity=1` against the control. That converts a
  described mechanism into a demonstrated one.

## Acceptance

- A native stack naming where the XLA workers are parked, or a recorded finding
  that it could not be obtained and why.
- Question 3 answered either way, since it decides whether the ~15% is
  recoverable.
- An upstream issue filed, or a recorded decision not to with the reason.
- If a better fix lands, the flag is removed from all four profiles and the
  family re-timed before anything is called done.
