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

### CONFIRMED (run 33103725546) — a pool of one cannot deadlock

ABAB again, 600s cap (raised from 300s on purpose: a one-CPU run is serial and
slower, and a false "hang" from too tight a cap would have wrecked the test).

| Arm | 3.12 | 3.13 | Pooled |
|---|---|---|---|
| control (pool of 4) | 1 pass / 2 hang | 0 pass / 3 hang | **1 / 5** |
| one (affinity=1)    | 3 pass / 0 hang | 3 pass / 0 hang | **6 / 0** |

Fisher exact two-sided p = 0.015 within the dispatch; p = 0.0002 pooling the
twelve control-equivalent runs from 33099502356. All five native dumps are
control-arm — the `one` arm never reached the 300s dump threshold, which is the
cleanest confirmation available.

Exactly what the re-entrancy predicts: with one worker ducc0 gets nthreads=1 and
runs inline, so there is no latch to wait on. The deadlock needs >= 2 pool
threads.

CONFOUND, stated because it bounds the claim: affinity=1 changes both pool size
and total parallelism, so it cannot separate "a pool of one cannot deadlock"
from "one CPU serialises everything". The mechanism makes the first reading
natural; this experiment alone does not.

**And it settles the ~15% from the other side.** `one` completes in 56.2-62.5s
against control's single completion at 48.1s — ~20-30% on a working four-thread
run, i.e. about what the current flag already costs at ~62s. There is no cheaper
setting: pool sizing recovers nothing, by quota-matching (no quota exists) or by
shrinking (same cost as the flag). Recoverable only upstream.

### Q2 CLOSED — standalone reproducer deadlocks (80d7bc5)

`autolens_workspace_test/.github/scripts/xla_fft_pool_reentrancy_repro.py`.
jax + numpy only, no PyAuto import. 8 trials per arm:

    default                              0 pass / 8 hang
    --xla_cpu_multi_thread_eigen=false   8 pass / 0 hang, 3-4s each

Perfect separation, Fisher two-sided p = 0.000155. The flag does not merely
avoid the hang, it completes the same work in seconds — which is what shows the
script reproduces THE bug, not some other stall. Sharper than the workspace
script it stands in for (8/8 vs ~5/6), so a reader need not run it repeatedly.

**What unblocked it: mge_group.py reproduces on an ordinary 4-CPU box.** With it
hanging locally I could dump the real HLO and read the answer instead of
guessing upward from a synthetic graph.

Two ingredients, each established by removing it:
1. **A scatter feeding each FFT.** Without it XLA fuses the chain into a
   YnnFusionThunk, ducc0 runs inline, no latch is taken, no deadlock. The real
   HLO reads `fft(%wrapped_scatter.423)` for all 282 of its fft ops.
2. **Transforms big enough for ducc0 to fan out.** 180x180 runs inline here;
   512x512 fans out and deadlocks. ducc0's own threshold, machine-dependent.

CORRECTIONS to what this record said earlier (kept, not dropped):
- "Worker::Parallelize/CountDown/RunWaiter is the missing ingredient" — WRONG.
  The reproducer deadlocks with zero such frames, as does the real script.
- "CI runs 15x15 grids under PYAUTO_SMALL_DATASETS" — WRONG. mge_group.py
  declares `ENV: jax full_datasets`, which unsets it; it runs full resolution
  and size mattered.
- Several "zero ducc0 frames" readings were sampling artifacts: $! was the
  `timeout` wrapper, not python, so they watched the wrong process.

### Q4 DECIDED (2026-08-27) — report written and reviewed, deliberately NOT filed

The acceptance criterion is "an upstream issue filed, OR a recorded decision not
to with the reason". This is the decision.

**Reason:** filing posts to jax-ml/jax, a third-party tracker outside this
session's GitHub scope (PyAutoLabs repos only) — an outward-facing act on
someone else's project, so it needs a person behind it. The hold is about WHO
POSTS, not about whether the finding stands; nothing in the evidence is
provisional.

The report is written, human-reviewed and committed, so filing later costs only
the paste: autolens_workspace_test 51512af,
`.github/scripts/xla_fft_pool_reentrancy_upstream.md`, beside the reproducer.
Committed rather than left in scratch on purpose — the CI job logs holding the
original stacks expire in 90 days, and a scratch dir does not survive a session.

Two late measurements folded in after review:
- float64 is NOT required: default float32 hangs 0 pass / 6 hang. Report keeps
  the float64 block (measured 8/8) and notes the shorter form is equally good.
- The repeat loop IS load-bearing: a single call passed 5/5, the 20-iteration
  loop hangs 8/8. A reader who trimmed it would wrongly conclude no repro.

Recorded on the issue: comment 5445381638.

### ALL FOUR ACCEPTANCE CRITERIA MET

| Criterion | Status |
|---|---|
| Native stack naming where the workers are parked | YES — 11/11 CI dumps + local + standalone |
| Q3 answered either way | YES — no; no quota exists, pool of 1 costs what the flag costs |
| Upstream filed OR recorded decision not to | YES — recorded decision, above |
| Flag removed from all four profiles, family re-timed | Deliberate non-action |

The last row is conditional in the prompt on "if a better fix lands", and none
has. The workaround stays in both smoke and release profiles of both test
workspaces; the seven entries stay un-quarantined as they are.

Open follow-up whenever wanted: the filing itself. If upstream fixes FftThunk,
the ~15% comes back and the flag can be removed from all four profiles with the
family re-timed, exactly as the last criterion describes.

### Still open

- ~~Q2 reproducer PARTIAL~~ — SUPERSEDED by the section above; kept for the
  dead ends it records. Original text: **Q2 reproducer — PARTIAL, committed** as
  `autolens_workspace_test/.github/scripts/xla_fft_pool_reentrancy_repro.py`
  (fdd289a). Nothing in CI runs it. It reproduces the RE-ENTRANCY
  deterministically (3 of 4 workers in FftThunk -> ducc0 latch::wait, held over
  six samples; 27.8s vs 67.5s on two identical runs) but NOT a full deadlock:
  3 of 4, never 4 of 4, so one worker always drains. Missing ingredient is
  identified, not guessed — the script shows ZERO Worker::Parallelize /
  CountDownAsyncValueRef / RunWaiterAndDeleteWaiterNode frames, the path two of
  CI's four wedged workers take. Closing it needs XLA to split a kernel into
  >1 workgroup there. Three dead ends are recorded in its docstring (large FFTs;
  many tiny FFTs; taskset to 2-3 CPUs) so they are not re-run.
- **Q4 upstream — FILABLE NOW.** The bug is FftThunk handing ducc0 the pool it is
  already running on; the full deadlock is its worst case, and the committed
  script demonstrates the re-entrancy standalone. Not yet filed.
- Optional: pool=2/3 on the real script would map the dose-response (my local
  pool=2/3 trials used the synthetic repro, not mge_group.py).

## Acceptance

- A native stack naming where the XLA workers are parked, or a recorded finding
  that it could not be obtained and why.
- Question 3 answered either way, since it decides whether the ~15% is
  recoverable.
- An upstream issue filed, or a recorded decision not to with the reason.
- If a better fix lands, the flag is removed from all four profiles and the
  family re-timed before anything is called done.
