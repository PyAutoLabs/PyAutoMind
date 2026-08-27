# JAX vmap materialisation hang — root-caused to XLA CPU's Eigen thread pool, all seven quarantines cleared (jax-compile-stall phase 3)

- **Issue:** PyAutoFit#1528 (closed) · autolens_workspace_test#245 (closed) · **PRs:** PyAutoFit#1529 (`4130b22`), PyAutoHands#269 (`ad64e12`), autolens_workspace_test#281 (`69ee97c`), autogalaxy_workspace_test#114 (`adf5ffe`) — all merged 2026-08-27
- **Repos:** PyAutoFit (`non_linear/jax_compile.py`), PyAutoHands (`autohands/build_util.py`, `autohands/env_config.py`), both `*_workspace_test` (`config/build/profile_{smoke,release}.yaml`, `no_run.yaml`, `smoke_tests.txt`)
- **Epic:** `jax-compile-stall`, phase 3 of 3 — **CLOSES the epic.** Phase 1 shipped the instrumentation, phase 2 measured and stopped short, phase 3 found the cause and restored the coverage.
- **Task slug:** `jax-stall-block-until-ready` (the `active.md` entry and the branch name; this record is filed under the corrected name, since the task slug still carries the "stall" misnomer)
- **Status: SHIPPED, with the root cause deliberately unfinished** — see "What is still not known".

## The headline: the epic's name was wrong for a month

Every marker, prompt and issue called this an *"intermittent XLA compile stall"*. **It is not a compile stall.** Compilation completes in ~12-18s; what never returns is **materialising the vmap result**. Captured at both doors, in the same run:

```
jax/_src/api.py    2764 try_to_block          jax/_src/array.py    642 _value
jax/_src/api.py    2781 block_until_ready     jax/_src/profiler.py 420 wrapper
jax_compile.py      249 _block_until_ready    jax/_src/array.py    391 __str__
jax_compile.py      339 wrapper               mge_group.py         319 <module>
mge_group.py        313 <module>
```

One failure, two doors. The line-313 door is the first `_vmap` call; the line-319 door is `print()` of the second, which short-circuits `log_on_first_compile` and so logs nothing at all.

## The trigger: XLA CPU's multithreaded Eigen thread pool

`XLA_FLAGS=--xla_cpu_multi_thread_eigen=false`, in `profile_smoke.yaml` **and** `profile_release.yaml` of both test workspaces so gate, mega-run and release-integrate cannot disagree. ABAB on `imaging/jax_likelihood/mge_group.py`, 3 repeats x 2 legs, 300s cap:

| Arm | Result | Run |
|---|---|---|
| default | 4/4 HANG | 33076408637 |
| compilation cache disabled | 6/6 HANG | 33078033016 |
| flag + `host_platform_device_count=1` + `OMP_NUM_THREADS=1` | 6/6 PASS, 63.2s | 33080638510 |
| **flag alone** | **6/6 PASS, 62.3s** | 33082896277 |
| default again | 4/6 HANG, verdict `STALL` | 33085024710 |

**12 passes / 0 hangs with the flag; 2 passes / 14 hangs without. Fisher exact p ~ 3e-6.** The other two variables did nothing — 62.3s alone vs 63.2s together. Cost ~15%; reaches only JAX/XLA scripts since nothing else reads `XLA_FLAGS`.

## Coverage restored — the point of the campaign

Family re-times 33087267785 (al) + 33087271848 (ag): **42/42 completions, `NEITHER` on every entry and every leg**, slowest 20% of cap.

| Repo | Entry | 3.12 | 3.13 | was |
|---|---|---|---|---|
| al | `imaging/jax_likelihood/mge_group.py` | 61.2s | 61.3s | NEEDS_FIX 08-24, **16/16 lifetime cap hits, zero completions** |
| al | `multi_dataset/jax_likelihood/delaunay.py` | 24.4s | 23.2s | NEEDS_FIX 08-01 (#245) |
| al | `multi_dataset/jax_likelihood/mge.py` | 16.0s | 14.5s | smoke_tests.txt 08-22 |
| al | `multi_dataset/jax_likelihood/shared_preloads.py` | 43.9s | 43.8s | smoke_tests.txt 07-22 |
| ag | `multi_dataset/jax_likelihood/rectangular.py` | 20.0s | 21.9s | NEEDS_FIX 08-01 |
| ag | `imaging/jax_likelihood/mge_group.py` | 32.8s | 32.6s | NEEDS_FIX 08-23 |
| ag | `imaging/jax_likelihood/rectangular_mge.py` | 22.9s | 24.1s | NEEDS_FIX 08-23 |

Both exclusion-list disagreements resolved, and they ran opposite ways: al excluded `shared_preloads.py` from `smoke_tests.txt` as "300s+, the heaviest entry" while `no_run.yaml` admitted it to the weekly sweep (where it burned a cap on 08-25) — it measures **43.9s**, so that 300s+ was the stall, not slowness. ag had `rectangular.py` NEEDS_FIX in `no_run.yaml` but still live in `smoke_tests.txt`.

## The finding that unlocked everything: the evidence was being thrown away

**Nothing set `PYTHONUNBUFFERED`**, and the runners capture through `subprocess.PIPE`. A pipe is not a tty, so a child's `print()` is block-buffered and flushed only at exit; `logging` goes to stderr and arrives immediately. A script SIGKILLed at its cap loses its **entire stdout buffer**.

So every *"and then silence"* tail in this campaign — the 08-01, 08-23, 08-24 and 08-25 markers — was silence of **stderr alone**. Five scripts were quarantined on evidence truncated before anyone read it. Proven from the *passing* leg, not inferred: its logging lines interleave by timestamp and then all eight prints arrive in one block at exit.

## Traps recorded

- **A phase-blind heartbeat is worse than none.** It said `"still compiling"` in both halves, so a stalled run produced *positive evidence for the wrong cause*. Five markers were written against it. Instrumentation that can be confidently wrong is a liability, not a diagnostic.
- **A summary line emitted after both halves finish describes only the runs that did not fail.** The compile/execute split never appeared on a stalled run.
- **`faulthandler` under SIGABRT works while a C extension holds the GIL** — that is why it is the right tool, and why SIGKILL alone had produced nothing for a month. It shows Python frames only, so XLA's own threads stay opaque.
- **A watchdog scoped to one function cannot see a hang outside it.** PyAutoFit's watchdog is disarmed the moment the first compile returns; the general fix belongs in the runner (`kill_group`), not the library.
- **`env_config.apply_profile` does `env[key] = str(value)`** — an unquoted empty YAML value becomes the literal string `"None"`, i.e. a truthy cache directory named `None`. Quote empty values.
- **Every pre-existing test in `test_script_timeout.py` passed `flush=True`**, so the suite proved output survives in the one case real scripts never hit. A test suite can be uniformly blind in exactly the dimension that matters.
- **The tenant firewall is real and will catch you.** Citing `PyAutoLabs/PyAutoFit#NNNN` in a `.py` under an organ fails CI. Fix by removing the instance fact, never by growing `FIREWALL_ALLOWLIST` — each entry is another file an adopting fork must rewrite. Organ names are fine (framework identity).
- **Sufficiency is not necessity.** The hang rate wanders: this script passed 2/2 at 02:18 and hung 2/2 at 13:33 on the identical commit. Twelve passes with a flag prove nothing without re-measuring the control — hence ABAB, not before/after.

## Hypotheses refuted (so nobody re-runs them)

- **Persistent compilation cache** — 6/6 hangs with it disabled. Verified applied: no "cache has been enabled" line, compiles dropped 15.7s → ~12s.
- **jax/jaxlib version** — the 2026-08-24 run, hanging 3/3 on *both* legs, had byte-identical jax `0.11.1` / jaxlib `0.11.1` / ml_dtypes `0.6.0` / numpy `2.5.2` / scipy `1.17.1`. No bisect needed.
- **3.12 vs 3.13** — 3.13 passed 2/2 then hung 2/2 on the same commit hours apart. Not causal.
- **`vmap(jit)` ordering** — untested at power here; phase 2's p=0.070 stands, and the flag result makes it moot.

## What is still not known

**This is a workaround, not a root-cause fix.** We know *where* it hangs and *what* avoids it. We do not know **why** XLA's CPU thread pool wedges on these graphs — `faulthandler` reports Python frames only, so the wedged worker threads are still opaque. Getting further needs a native stack (gdb / py-spy) and a minimal jaxpr reproducer outside the workspace, then an upstream JAX/XLA report. Filed as a follow-up research prompt.

Both `no_run.yaml` block comments record this, and say that removing the flag brings the entries back.

## Heart

**Not consulted** — `pyauto-heart` unreachable from the `web-github` environment, as on phases 1 and 2. Every merge was on the human's explicit `/prm`.

## Provenance

Planned, implemented, measured and shipped by one `web-github` session on 2026-08-27 (`claude/jax-compile-stall-root-cause-d33hi0`), against direct clones rather than worktrees. Eleven CI dispatches of the phase-2 `retime.yml` harness did the measuring.

## Original prompt

# Phase 3: root-cause the XLA vmap compile stall and clear every NEEDS_FIX it caused

Type: bug
Target: ci
Repos:
- @PyAutoFit
- @autogalaxy_workspace_test
- @autolens_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Epic: jax-compile-stall
Phase: 3
Campaign: bug/ci/jax_vmap_jit_compile_stall.md (Phase 3 — the fix; blocked on phases 1 and 2)
Filed: 2026-08-23
Issued: 2026-08-27

## Blocked on phase 1

Do not start this before phase 1's watchdog has shipped and a CI stall has
actually dumped a traceback. Diagnosing a hang that leaves no evidence is what
produced three quarantines and no root cause; repeating it without the
instrumentation would be a fourth.

## Reproduce deliberately

Loop `imaging/jax_likelihood/mge_group.py` under its declared CI env profile
until it hangs, rather than waiting for CI to hit it. Attach `py-spy dump` to
the hung process as well as reading phase 1's own `faulthandler` output — the
two see different things, and `py-spy` can read native frames the in-process
dump cannot.

## Hypotheses, in the order they are cheapest to test

1. **`vmap` of `jit`, the inverted ordering.** `Fitness._vmap`
   (`autofit/non_linear/fitness.py`) builds `jax.vmap(jax.jit(self.call))`;
   `autofit/non_linear/analysis/latent.py` builds
   `jax.jit(jax.vmap(compute_latent_for_model))`, the conventional order. The
   stalling path is exactly the `vmap` path, and the `_jit`-only scripts in the
   same directories do not stall. One-line A/B — try it first.
2. **Persistent compilation cache contention.** `JAX_COMPILATION_CACHE_DIR` has
   defaulted on since PyAutoConf#128 (merged 2026-07-17). Both NEEDS_FIX stalls
   post-date it; the eight SLOW entries predate it. A/B with the cache dir set
   to empty (which disables it) and see whether the stall probability moves.
3. **JAX/XLA version interaction.** This repo has form: `delaunay_mge.py` is
   disabled outright because `jax 0.7` removed
   `jax.interpreters.xla.pytype_aval_mappings`, and the smoke installer once
   clobbered a working `tfp-nightly`. Pin-bisect jax/jaxlib across a run set.
4. **Runner CPU contention.** `complete/2026/07/jax-compile-time-research.md`
   records that XLA compiles on **host** CPUs and that compile timing is
   load-sensitive by up to 7×, which is why a hosted runner is the place this
   reproduces and a workstation is not.
5. **Graph size in the vmap trace.** The affected set has a shape: plain `mge.py`
   passes in 9.4s, while the *composite* variants — group, rectangular-MGE,
   delaunay-MGE — stall or are already out. Complexity-driven compile blowup was
   argued against by the autolens_profiling#71 research ("compile cost is
   op-pattern-driven, not complexity-driven"), so treat this as the hypothesis
   of last resort, not the first.

## Then restore the coverage

The point of the campaign. Quarantining removes exactly the heaviest JAX paths,
which are the ones most worth testing.

1. Clear the NEEDS_FIX markers this campaign inherits — including the
   2026-08-01 `multi_dataset/jax_likelihood/rectangular.py` one and the
   `autolens_workspace_test` `delaunay.py` entry citing #245.
2. Re-enable `multi_dataset/jax_likelihood/mge.py` and `shared_preloads.py` in
   `autolens_workspace_test`'s `smoke_tests.txt` (folded in from the superseded
   2026-08-22 filing).
3. Anything that stays out after the fix stays out with a **recorded deliberate
   reason**, not as an accumulated one-off.

## Acceptance

- A stated root cause, or an explicit recorded decision that it is an
  infrastructure limit to be worked around rather than fixed. Not another
  quarantine.
- Every entry marked NEEDS_FIX for this signature restored to its suite, or
  re-marked with the real reason phase 2 established.
- The `multi_dataset/jax_likelihood/` family back under CI coverage in both test
  workspaces, or its absence recorded as a deliberate choice.
