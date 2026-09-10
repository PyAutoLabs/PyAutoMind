Guarded the JAX x64 config layer in 54 workspace scripts that imported `jax`
before anything pulling in `autonerves/jax_wrapper.py`, which sets
`JAX_ENABLE_X64`, `XLA_FLAGS=--xla_disable_hlo_passes=constant_folding` and
`JAX_COMPILATION_CACHE_DIR` at import time. JAX reads all three at its first
import, so those scripts ran in float32 with constant folding on, and every
precision and timing figure they printed described a different program from the
one they claimed.

The fix is one line per file, the idiom the repo already used in
`jax_profiling/simulators/*`:

    from autolens import jax_wrapper  # noqa: F401 — must be first

placed first (after any `__future__` import). 54 files, each exactly +2/-0; no
existing import moved.

## PRs

- autolens_workspace_developer#140 (merged 2026-09-10, `516ff1c`) — issue #139

## The reported count was wrong in both directions — 33 vs 54

The prompt's list came from comparing the first `^import jax` line number
against the first `^import auto\(lens\|galaxy\|array\|fit\)` line number. Re-survey
by **guard mechanism**, not line number, before trusting a count like this:

- It **over-counted**: 6 `jax_profiling/simulators/*.py` were already fixed, and
  are inside the reported 33. The pattern cannot see
  `from autolens import jax_wrapper`.
- It **under-counted**: it misses `from jax import …`, and it misses the 25
  `searches_minimal/` scripts entirely because they import no PyAuto library
  directly. Those 25 were the largest group and **reordering could not have
  fixed any of them** — the prompt's prescribed fix was inapplicable to half
  the real work.

`searches_minimal/_setup.py` imports `autolens` at line 27 and imports no `jax`,
so it is the chokepoint every one of those 25 already reaches. The same guard
line worked there with no new dependency.

## Trap: a Witness can be true and still be measuring the wrong thing

The branch's first commit message claimed the Witness held 54/54 on
`jax.config.jax_enable_x64`. The adversarial pass falsified that against the
branch's own diff:

- **48 of 54** — `False` on `main` → `True`. The Witness as written.
- **6 of 54** — already `True` on `main`. Those six `searches_minimal/` files
  self-patch with `jax.config.update("jax_enable_x64", True)` a few lines after
  importing `jax`. What the guard actually fixes for them is **`XLA_FLAGS`**:
  `None` on `main`, the wrapper's flags after. That one cannot be recovered
  after the `jax` import — no `jax.config` call reaches it.

Corrected to 48/54 before the branch was pushed. The general lesson: a
measurement harness that stops at the first `jax` import measures *import
order*, which is not the same claim as *the flag's final value*. Both are worth
knowing; only one was what the prompt asked for.

## Traps and findings

- **`from __future__` imports must stay first.** 5 of the 54 carry them, and an
  insertion harness that prepends anything above them yields
  `SyntaxError: from __future__ imports must occur at the beginning of the
  file`. The same error appeared identically on both refs, which is what
  identified it as a harness artefact rather than a code defect.
- **`jax.config.update("jax_enable_x64", True)` is a half-fix.** It restores the
  dtype and nothing else; `XLA_FLAGS` and the compilation cache dir are read at
  backend init and are gone by then.
- **This repo has no CI and no test directory.** The only Actions entry is the
  dynamic Copilot reviewer agent; `check_runs` is 0. `check_x64_guard.py` was
  added so the invariant is at least provable on demand. Not wired into CI —
  there are no workflows to wire it into.
- **The Mind ledger branch failed to auto-merge twice** before this close-out,
  on a content conflict in `active.md` + both dashboards after two other ledger
  branches landed on `main` first. `mind_ledger_merge.yml` reports this as a
  plain workflow failure; resolve by merging `main` in, keeping both `active.md`
  entries, and **regenerating** the dashboards rather than hand-resolving them.

## Decision taken (decide-and-flag, one per PR)

The approved plan said to delete the six now-redundant
`jax.config.update("jax_enable_x64", True)` calls. They were **kept**: three
carry comments that make deletion a judgement, not a mechanical stretch —
`pix_multi_start.py:66-70` is a five-line science rationale attached to the call
("dropping to fp32 to dodge the OOM would be a science compromise"), and
`probe_nonfinite_pix.py:90` says the ordering is deliberate ("exactly as the
harness under test does"). Keeping them also left the diff perfectly uniform:
54 identical hunks. Revert is one `sed`, in the PR body.

## Numeric confirmation

`jax_profiling/jit/imaging/mge.py`, no env var preset:

    eager baseline     27373.152646517716
    step-by-step JIT   27373.15264651771
    full-pipeline JIT  27373.152646517705

~4e-16, against the reported float32 `27373.1328125` / `27373.130859375`
(~8e-7). No pinned constant changed — the diff contains no numeric literal.

## Ship gate

Legs 1 (tests) and 2 (smoke) are **n/a by the gate's own applicability rule** —
no test directory, no `smoke_tests.txt`, not one of the six curated workspaces.
Leg 3's surface was prepared and its one lifted claim disposed basis-cited.
**Leg 4 (Heart) was never consulted**: PyAutoHeart is not in a web session's
repo scope and `pyauto-heart` is not on PATH. It was recorded as not-consulted
rather than passed, and the human merged with that stated.

## Environment

Remote web session, no task worktree. `autolens_workspace_developer` was not in
the session's initial repo scope and was attached mid-session with `add_repo`.
`pip install autolens jax` from PyPI is what made the runtime Witness possible
at all — worth knowing that a web container can measure a workspace repo's
behaviour without the source libraries checked out.

## Adjacent, not actioned

- `PyAutoMemory/wiki/methods/concepts/gradient-optimizer-benchmarks.md:113`
  already records "RAL GPU is float32 (x64 off), tolerated here", so the A100
  benchmark record survives this bug. But it attributes the float32 to the GPU,
  where the CPU legs were most likely float32 for *this* reason.
- `draft/research/autonerves/pair_jax_xla_env_vars_with_measured.md` is the
  adjacent `too-large` research prompt on measuring these env vars per backend.

## Original prompt

# jax_profiling scripts import jax before autolens, silently running in float32

Type: bug
Target: autolens_workspace_developer
Repos:
- autolens_workspace_developer
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-09-10
Consequence: glance
Witness: for each swept script, importing it with no env var preset leaves jax.config.jax_enable_x64 True, where it is False on main.
Review-minutes: 3
Unattended: ready

33 scripts in @autolens_workspace_developer import jax before they import the PyAuto libraries. That defeats the config layer's jax_wrapper, which sets JAX_ENABLE_X64=True, XLA_FLAGS=--xla_disable_hlo_passes=constant_folding and JAX_COMPILATION_CACHE_DIR at import time - too late once JAX is already imported, exactly as its own docstring warns.

Measured 2026-09-09 while re-pinning the MGE HST regression constant (@autolens_workspace_developer issue 137, PR 138). In jax_profiling/jit/imaging/mge.py (jax at line 53, library import at line 61), a bare 'python mge.py' runs with jax_enable_x64=False and dtype float32: the JIT leg returns 27373.130859375 and the step-by-step leg 27373.1328125, agreeing with the eager NumPy value only to about 8e-7 - not the ~1e-11 the file's own comment asserts. Presetting JAX_ENABLE_X64=True restores float64 and 4e-16 agreement.

No pinned constant is wrong because of this: the eager reference is pure NumPy (xp=np) and identical either way, and PR 138's value was measured with x64 forced on. What is wrong is every JIT and vmap timing and precision claim these scripts print and write into jax_profiling/results/, unless the runner happened to preset the env var.

The fix is to move the jax import below the library import in the affected scripts, then confirm jax.config.jax_enable_x64 is True at runtime rather than assuming the reorder took. The full list of 33 is reproducible by comparing the first 'import jax' line number against the first library import line number in each file.

Witness: for each swept script, importing it with no env var preset leaves jax.config.jax_enable_x64 True, where it is False on main.

<!-- formalised by the Intake (Conception) Agent on 2026-09-09 from user-intake -->

### The 33 files (2026-09-09, `main` @ 96937c9)

Reproduce with:

```bash
for f in $(grep -rl '^import jax' --include=*.py .); do
  jl=$(grep -n '^import jax' $f | head -1 | cut -d: -f1)
  al=$(grep -n '^import auto\(lens\|galaxy\|array\|fit\)' $f | head -1 | cut -d: -f1)
  [ -n "$jl" ] && [ -n "$al" ] && [ "$jl" -lt "$al" ] && echo "$f (jax:$jl before lib:$al)"
done
```

33 of the 60 files that import jax. They cluster in `jax_profiling/`
(gradient/, jit/, misc/, simulators/), plus `plotting_alignment/` (3),
`searches_minimal/` (3) and `legacy/quantity/` (1) — all written from the
same template, which is why the fix is a sweep rather than a one-file edit.

### Out of scope

- Re-measuring any pinned constant. The eager references are pure NumPy and
  unaffected; `jax_profiling/jit/imaging/mge.py` was already re-pinned under
  forced x64 in PR 138. If the swept scripts' *timings* should be re-recorded
  under float64, that is a profiling run, not this fix.
- The XLA:CPU vmap deadlock on 4-core machines
  (`XLA_FLAGS=--xla_cpu_multi_thread_eigen=false` works around it) — a
  container artefact noted in PR 138, not this bug.
