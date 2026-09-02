# JAX vmap result never materialises — campaign map (SHIPPED 2026-08-27; the "XLA compile stall" name was wrong)

Type: bug
Target: ci
Repos:
- @autogalaxy_workspace_test
- @autolens_workspace_test
- @PyAutoFit
Themes:
- jax-compile
- ci-smoke
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: campaign map — phases route through /start_dev one at a time; this
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: jax-compile-stall
        file is never issued itself and nothing here is bulk-issued
Filed: 2026-08-23

Surfaced 2026-08-23 by the per-script timeout backport
([`backport_per_script_timeout.md`](../../maintenance/ci/backport_per_script_timeout.md)),
which put a 300s cap on `autogalaxy_workspace_test`'s previously uncapped smoke
gate. The cap fired on its very first run — not on the change under test, but on
a latent hang the uncapped runner had been absorbing.

## What was observed

`autogalaxy_workspace_test#109`, `smoke (3.13)`, 36/37 passed:

```
TIMEOUT (300s)  imaging/jax_likelihood/mge_group.py
```

The captured tail — preserved precisely because the cap keeps the killed child's
output — names the stall:

```
18:47:53  autoarray...dataset - INFO - IMAGING - Data masked, 1264 image-pixels
18:47:55  jax._src.xla_bridge - INFO - Unable to initialize backend 'tpu' ...
18:47:55  autofit.non_linear.jax_compile - INFO - JAX jit compiling vectorized
          (vmap) likelihood function, could take seconds or minutes...
          [silence for the full 300s]
```

It never emitted another line. This is a stall inside JAX vmap/JIT compilation,
not a slow script:

- its sibling `imaging/jax_likelihood/mge.py` passes in **9.4s**, reporting
  `JAX Time To VMAP + JIT Function: 2.50s`;
- `multi_dataset/jax_likelihood/mge_group.py` — same basename, same tier —
  passes in **28.8s** in the same run;
- the script passes on `main`.

So the same code path completes in seconds normally and occasionally never
completes at all.

## It is not one script — the second leg named a second one

The two matrix legs of the **same commit** disagreed, and the slower leg found
more:

| Leg | Result | Timed out |
|---|---|---|
| `smoke (3.13)` | 36/37 | `imaging/jax_likelihood/mge_group.py` |
| `smoke (3.12)` | **35/37** | `imaging/jax_likelihood/mge_group.py` **and `imaging/jax_likelihood/rectangular_mge.py`** |

`rectangular_mge.py` **passed on 3.13 and stalled on 3.12, on the same commit**.
So the stall is not a property of one script, and not deterministic per Python
version either — it is a per-compile probability that two runs of the same code
sample differently.

The affected set has a shape. Of `imaging/jax_likelihood/`:

| Script | State |
|---|---|
| `mge.py` | passes, 9.4s (2.5s vmap+JIT) |
| `mge_group.py` | stalled on both legs |
| `rectangular_mge.py` | stalled on 3.12, passed on 3.13 |
| `delaunay_mge.py` | already disabled (jax 0.7 removed `jax.interpreters.xla.pytype_aval_mappings`) |

The plain `mge` is fine; the **composite** MGE variants — group, rectangular-MGE,
delaunay-MGE — are the ones that stall or are already out. That points at compile
graph size/complexity in the vmap trace, not at any one script's logic, and it
predicts which other entries are at risk.

**This is why quarantining is the wrong end state.** Parking scripts as they
stall is whack-a-mole against a probability: each park removes coverage of
exactly the heaviest JAX paths, which are the ones most worth testing.

## Why this is worth a task rather than a marker

This is the **third** repo/script to hit the same signature, and the pattern in
the `no_run.yaml` files is that each occurrence gets quarantined and the
underlying stall is never diagnosed:

| Entry | Marker | Note |
|---|---|---|
| `multi_dataset/jax_likelihood/rectangular.py` (autogalaxy_workspace_test) | NEEDS_FIX 2026-08-01 | "hung to the 1800s release cap … passes ~19s otherwise; intermittent XLA compile stall, same family as autolens_workspace_test delaunay" |
| autolens_workspace_test delaunay | — | `autolens_workspace_test#245` |
| `imaging/jax_likelihood/mge_group.py` (autogalaxy_workspace_test) | NEEDS_FIX 2026-08-23 | this one |

Plus six `interferometer/jax_likelihood/*` and two `jax_grad/*` entries
SLOW-skipped on 2026-07-14 for "flaking at the 1800s cap" (PyAutoHeart#74) —
which, given this evidence, may not be slowness at all but the same stall
wearing a different label. **That distinction matters**: a SLOW marker says
"make it faster", a stall says "it never finishes", and the Profiling Agent has
been handed a set of scripts under the first description when some may belong to
the second.

The cost was invisible until now because nothing was capped.
`autogalaxy_workspace_test` has **four** runs cancelled at the 6-hour Actions
ceiling (runs 30088422799, 30051301212, 30289779988, 31319423047) — roughly 24
hours of runner time, with no diagnostic output, because the uncapped runner sat
on a held stdout pipe. Those runs are now impossible: the cap turns a 6-hour
silent hang into a 300s TIMEOUT with the compiling-step tail attached. That is
what made this diagnosable at all.

## Task

1. Establish whether the SLOW-marked `jax_likelihood`/`jax_grad` entries are
   genuinely slow or are this stall mislabelled. Re-time them against the real
   caps; a slow script has a tight timing distribution, a stalling one is
   bimodal.
2. Reproduce the stall deliberately — loop `imaging/jax_likelihood/mge_group.py`
   until it hangs, then attach `py-spy dump` / `faulthandler` to see where inside
   the XLA compile it is parked.
3. Determine whether the trigger is a JAX/XLA version interaction (this repo has
   prior form: `delaunay_mge.py` is disabled outright because `jax 0.7` removed
   `jax.interpreters.xla.pytype_aval_mappings`, and the smoke installer once
   clobbered a working `tfp-nightly`), a `vmap` shape/donation issue, or
   contention on the runner.
4. Fix, then remove the NEEDS_FIX markers — including the 2026-08-01 one, which
   this task inherits.

## Acceptance

- A stated root cause for the stall, not another quarantine.
- Every entry currently marked NEEDS_FIX for this signature is either restored to
  its suite or re-marked with the real reason.
- The SLOW-vs-stall question in step 1 answered in writing, so the Profiling
  Agent is not chasing speedups on scripts that are hanging.

## CORRECTION — the stack says this is NOT a compile stall

Captured after close-out, from both test workspaces independently: the stalled
process is parked in `jax.block_until_ready` / `try_to_block`, i.e. the
**execution** half of the first call, not tracing/lowering/compiling. The title
of this file, and every marker calling this an "intermittent XLA compile
stall", inherit a guess made before there was any evidence. See the record's
final section.

## SHIPPED — 2026-08-27

All three phases are done. Record:
[`complete/2026/08/jax-vmap-materialisation-hang.md`](../../../complete/2026/08/jax-vmap-materialisation-hang.md).

Phase 3 established that the hang is **materialising the vmap result**, not
compiling it — captured at `jax.block_until_ready`/`try_to_block` and at
`jax.Array._value`, with compilation finished ~12-18s earlier. The trigger is
XLA CPU's multithreaded Eigen thread pool; the workaround is
`XLA_FLAGS=--xla_cpu_multi_thread_eigen=false` in both test workspaces' smoke
and release profiles (ABAB, 12 passes/0 hangs with vs 2 passes/14 hangs
without, Fisher exact p ~ 3e-6). All seven quarantined entries are restored,
42/42 completions.

**Why the pool wedges is still unknown** — a workaround, not a root-cause fix.
The follow-up lives under `draft/research/ci/`.

The section below is kept as the 2026-08-23 state, for the history of how this
was worked.

## CLOSED AS PARTIAL — 2026-08-23

Phase 1 shipped. Phases 2 and 3 were taken to a deliberate stopping point and the
epic closed: the stall is **instrumented and characterised but not root-caused**,
and nothing was un-quarantined. The full account, including the two live leads and
every trap, is the record
[`complete/2026/08/jax-compile-stall-slow-vs-stall-audit.md`](../../../complete/2026/08/jax-compile-stall-slow-vs-stall-audit.md).
Resume through [`../../research/ci/smoke_timing_and_profiling.md`](../../research/ci/smoke_timing_and_profiling.md).

## Phase map (added 2026-08-23 at /start_dev)

The Bug Agent sizes this `too-large` and returns `split-into-phases`. It is one
root cause but three separable deliverables, and phases 2 and 3 are both blocked
on evidence that does not exist today. Each phase is its own prompt, issued one
at a time — nothing here is bulk-issued.

| Phase | Prompt | Deliverable | Repos |
|---|---|---|---|
| 1 | ~~`jax_compile_stall_1_evidence.md`~~ **SHIPPED 2026-08-23** — record [`complete/2026/08/jax-compile-stall-evidence.md`](../../../complete/2026/08/jax-compile-stall-evidence.md) (PyAutoFit#1516, PR#1517 merged) | A stalled compile reports itself: heartbeat, `faulthandler` dump, compile-vs-execute split | PyAutoFit |
| 2 | [`jax_compile_stall_2_slow_vs_stall_audit.md`](jax_compile_stall_2_slow_vs_stall_audit.md) | The SLOW-vs-stall question (task step 1) answered in writing; every marker carries its real reason | autogalaxy_workspace_test, autolens_workspace_test |
| 3 | [`jax_compile_stall_3_root_cause.md`](jax_compile_stall_3_root_cause.md) | Root cause + fix; every NEEDS_FIX for this signature cleared (task steps 2–4) | PyAutoFit, both `_workspace_test` |

Acceptance for the campaign as a whole is the § Acceptance section above; each
phase carries only its own slice of it.

## Supersedes an earlier filing of the same defect

[`complete/2026/08/multi-dataset-jax-likelihood-xla-stall.md`](../../../complete/2026/08/multi-dataset-jax-likelihood-xla-stall.md)
(filed 2026-08-22 as `draft/bug/autolens_workspace_test/multi_dataset_jax_likelihood_xla_stall.md`, never issued, recorded 2026-08-24) describes this same stall from the
`autolens_workspace_test` side. It is superseded by this campaign rather than
run alongside it — one root cause is one task. Its two asks that this filing did
not already carry are folded in: the runner leaving diagnostic evidence behind
(phase 1) and re-enabling `multi_dataset/jax_likelihood/mge.py` +
`shared_preloads.py` in `smoke_tests.txt` (phase 3).

## Two source-level findings from the /start_dev read of PyAutoFit

Recorded here because they are the leads phase 3 starts from, and neither was
known when this prompt was filed.

**1. The stalling wrapper is `vmap` *of* `jit`, the inverted ordering.**
`Fitness._vmap` (`autofit/non_linear/fitness.py`) builds
`jax.vmap(jax.jit(self.call))`, while `latent.py`'s batched latent computation
builds `jax.jit(jax.vmap(compute_latent_for_model))` — the conventional order.
The path that stalls is exactly the `vmap` path; the `_jit`-only scripts in the
same directories do not stall. Whether the ordering is causal is unproven, but
it is a one-line A/B and it is the first thing phase 3 should try.

**2. The silence spans two different waits, and nothing distinguishes them.**
`log_on_first_compile` (`autofit/non_linear/jax_compile.py`) logs
`JAX jit compiling {description}...`, calls the wrapped function, then calls
`jax.block_until_ready(result)` — trace/lower/compile and execution, with one
log line covering both and no heartbeat in between. That is why three
quarantines produced no diagnosis: the captured tail cannot say whether the
process is in XLA, in execution, or blocked on a lock. Phase 1 fixes exactly
this.

**Timeline worth testing in phase 3.** Both NEEDS_FIX stalls (2026-08-01,
2026-08-23) post-date the persistent-compilation-cache default (PyAutoConf#128,
merged 2026-07-17); the eight SLOW entries predate it. `complete/2026/07/jax-compile-time-research.md`
also records that XLA compiles on host CPUs and that compile timing is
load-sensitive by up to 7×. Cache-lock contention and runner CPU contention are
therefore both live hypotheses alongside the version-interaction one already in
§ Task step 3.

## New occurrence — 2026-08-24, `multi_dataset/jax_likelihood/mge.py`

Verified via the Actions API. `autogalaxy_workspace_test` `Smoke Tests` run
**32680155872** (main, push, commit `2a294d5` — the `run_smoke.py`
runner-collapse merge, PR#111), job `smoke / smoke (3.12)` (97295321230):

```
TIMEOUT (300s)  multi_dataset/jax_likelihood/mge.py
```

34/35 other scripts passed, including its sibling
`multi_dataset/jax_likelihood/mge_group.py` in **42.2s** in the same run.

It is the known per-compile probability, not a runner-collapse regression: the
**identical commit** passed the PR-gate run 32679570426 eleven minutes earlier
(01:22–01:31); only the 3.12 leg failed (3.13 green); and
`autolens_workspace_test`'s equivalent collapse merge run 32679945097 was green
on main at 01:29. Same signature as § "It is not one script".

**Affected-set shape.** This extends the family to
`multi_dataset/jax_likelihood/mge.py` — previously `imaging/jax_likelihood/`
`mge_group.py` + `rectangular_mge.py` (parked 2026-08-23,
autogalaxy_workspace_test#109) and `multi_dataset/jax_likelihood/rectangular.py`
(parked 2026-08-01, autolens_workspace_test#245). Composite/multi-dataset MGE
vmap graphs remain the common factor — note the plain `imaging` `mge.py` still
passes in 9.4s, so it is the multi-dataset composition, not the MGE alone.

**Consequence.** First `Smoke Tests` red on `autogalaxy` main after the collapse,
and Heart's sole RED blocker (PyAutoHeart README strip, 03:14). The failed job
was re-run at ~14:00 UTC to clear the gate; the script was deliberately **not**
parked, per #109's own warning against whack-a-mole parking that strips coverage
of the heaviest JAX paths. The per-script cap behaved exactly as designed: a 300s
TIMEOUT and exit 1 rather than a six-hour silent hang.

## New occurrence — 2026-08-25, `multi_dataset/jax_likelihood/shared_preloads.py`

**This one refutes a refutation.** The entry had its SLOW marker removed the day
before and was returned to coverage; it stalled on the next weekly run.

Verified via the Actions API. PyAutoHeart `Workspace Smoke` run **32902243623**
(2026-08-25, `workflow_dispatch` on the `weekly-smoke-timings-naming` branch),
job `smoke / run_scripts (3.12, autolens_test, multi_dataset)` (**97978549465**).
16 of 17 scripts passed:

```
scripts/multi_dataset/jax_likelihood/shared_preloads.py ...   TIMEOUT (300s)
```

Siblings in the same job, same commit, same runner:

| Script | Result |
|---|---|
| `jax_likelihood/mge.py` | PASS 11.7s |
| `jax_likelihood/rectangular_mge.py` | PASS 20.7s |
| `jax_likelihood/mge_group.py` | PASS 49.3s |
| `jax_likelihood/delaunay_mge.py` | PASS 20.2s |
| `jax_likelihood/rectangular.py` | PASS 15.8s |
| `jax_likelihood/rectangular_mge_rtu.py` | PASS 21.9s |
| `jax_likelihood/rectangular_rtu.py` | PASS 16.3s |
| `jax_likelihood/lp.py` | PASS 8.6s |
| `jax_likelihood/dataset_model.py` | PASS 12.9s |
| **`jax_likelihood/shared_preloads.py`** | **TIMEOUT (300s)** |

A >6x outlier against the slowest sibling, with every other family member
completing comfortably — the bimodal signature § "It is not one script" describes.

### The 2026-08-24 retime put this script back in coverage

State verified 2026-08-25 against `autolens_workspace_test` at `7fc497d`:

- `config/build/no_run.yaml` — **no `shared_preloads` entry.** It is in mega-run
  and weekly coverage.
- `smoke_tests.txt` line 15 — still commented out: *"disabled 2026-07-22: exceeds
  the 300s smoke cap (measured 300s+ in CI, autolens_workspace_test#196) … it is
  the heaviest entry here and does not belong in the fast PR gate."*

`shared_preloads.py` was in the PyAutoHeart#74 "flakes at the 1800s cap" SLOW
family. The 2026-08-24 retime (5 repeats per Python leg, 300s cap; runs
32741371308 + 32741386752) removed eight of those entries because they "completed
5/5 on both legs (slowest 54.5s) and were removed — marker refuted, scripts back
in mega-run coverage".

**~10 executions at ≤54.5s cannot exclude a low-probability hang.** The retime
was right that this script is not *slow*; it was not powered to see that it
*stalls*. Its readmission to coverage is falsified by the very next weekly run.

This lands § Task step 1's slow-vs-stall question on the opposite side from where
the retime put this entry, and it is a caution about the retime protocol
generally: for a bimodal failure, N=5 per leg measures the fast mode and says
nothing about the tail. Any other entry readmitted by that sweep carries the same
uncertainty.

### The two exclusion lists now disagree

`smoke_tests.txt` (PR gate) excludes `shared_preloads.py` as too heavy;
`no_run.yaml` (mega-run / weekly) admits it. The gates read different lists, so a
script disabled since July was still able to burn a 300s cap in CI. Worth
resolving deliberately rather than by whichever list is edited next.

### First occurrence on the weekly `workspace-validation` channel

Every prior occurrence in this ledger comes from a workspace repo's own
`Smoke Tests` gate or from `release-integrate`. This is the first via
PyAutoHeart's weekly `workspace-validation.yml` sweep — a different harness
(PyAutoHeart-owned, `script_matrix.py`-driven, honouring `no_run.yaml` and not
`smoke_tests.txt`) reproducing the same signature. That is cross-harness
corroboration that the stall is not an artifact of one repo's runner
configuration.

### Affected-set shape

Extends the family to `multi_dataset/jax_likelihood/shared_preloads.py`, joining
`multi_dataset/` `mge.py` (2026-08-24) and `rectangular.py` (parked 2026-08-01,
autolens_workspace_test#245), and `imaging/` `mge_group.py` + `rectangular_mge.py`
(parked 2026-08-23, autogalaxy_workspace_test#109). Note `shared_preloads.py` is
not an MGE variant — it is the shared-preloads path — so the "composite MGE vmap
graph" common factor no longer covers the whole set. What the members share is
heavy `multi_dataset` vmap composition, not MGE specifically.

**Consequence — nothing was parked.** Recorded and left in coverage, following
this file's § "This is why quarantining is the wrong end state" and the
2026-08-24 precedent, where `multi_dataset/jax_likelihood/mge.py` was deliberately
not parked. Re-marking is phase 3's call with a root cause in hand.

Surfaced incidentally by `complete/2026/08/weekly-smoke-timings-naming.md`
(PyAutoHeart#182), whose verification sweep produced this run — the first
practical dividend of the weekly timing dataset that task shipped.

## Retired from epics.md (2026-09-02)

## jax-compile-stall
- title: JAX vmap result never materialises (was: "intermittent XLA compile stall" — the name was wrong)
- ledger: draft/bug/ci/jax_vmap_jit_compile_stall.md
- status: SHIPPED 2026-08-27 — all 3 phases done; record
  complete/2026/08/jax-vmap-materialisation-hang.md. Root cause is XLA CPU's multithreaded Eigen
  thread pool; workaround XLA_FLAGS=--xla_cpu_multi_thread_eigen=false in both test workspaces'
  smoke AND release profiles (ABAB: 12 pass/0 hang with vs 2 pass/14 hang without, Fisher p~3e-6).
  All 7 quarantined entries restored, 42/42 completions. PyAutoFit#1528, PRs PyAutoFit#1529,
  PyAutoHands#269, autolens_workspace_test#281, autogalaxy_workspace_test#114.
  NOT a root-cause fix: why the pool wedges is still unknown — follow-up never filed (the resume
  door was never written).
- NEW EVIDENCE 2026-08-25: multi_dataset/jax_likelihood/shared_preloads.py stalled at TIMEOUT (300s) in
  PyAutoHeart Workspace Smoke run 32902243623 — one day after the 2026-08-24 retime refuted its SLOW
  marker and returned it to mega-run coverage. N=5 per leg measures the fast mode of a bimodal failure
  and says nothing about the tail, so every entry that sweep readmitted carries the same uncertainty.
  Also the epic's first occurrence via the weekly workspace-validation channel (cross-harness
  corroboration), and smoke_tests.txt vs no_run.yaml now disagree about this script. Nothing parked.
  See the ledger's "New occurrence — 2026-08-25" section; surfaced by
  complete/2026/08/weekly-smoke-timings-naming.md.
- CORRECTION (post-close-out): the captured stack shows the hang is in jax.block_until_ready, NOT in
  compilation. The epic's name and every marker calling this an "XLA compile stall" are wrong. Resume
  from "why does block_until_ready never return", not from compiler behaviour.
- notes: phase 1 (watchdog) shipped in full; phases 2/3 stopped deliberately at a measured-but-not-root-caused state. The stall is instrumented and characterised (>100x bimodality inside one compile step; vmap-of-jit contributory at p=0.070 but NOT causal; the compile-cache hypothesis never tested) and NOTHING was un-quarantined. Resumed 2026-08-27 as phase 3 (PyAutoFit#1528) — NOT via draft/research/ci/smoke_timing_and_profiling.md,
  which the 2026-08-23 close-out named as the resume door but which was never written. Superseded complete/2026/08/multi-dataset-jax-likelihood-xla-stall.md (was draft/bug/autolens_workspace_test/multi_dataset_jax_likelihood_xla_stall.md).
