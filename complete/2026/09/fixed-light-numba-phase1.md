## fixed-light-numba-phase1
- Target: autolens_profiling
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/263 (closed, completed)
- PR: https://github.com/PyAutoLabs/autolens_profiling/pull/264 (MERGED, merge commit `92856833`, feature commit `a993cf8`)
- Epic: fixed-lens-light-numba-cpu
- Phase: 1
- completed: 2026-09-14

## What shipped

Phase 1 of the `fixed-lens-light-numba-cpu` campaign: the **mechanism** for measuring the
whole `AnalysisImaging.log_likelihood_function` on PyAutoArray's numba path — the production
CPU route the completed GPU epic never touched — and decomposing it in ONE process rather
than by arithmetic across two cells. Three new files, zero library edits.

**`scripts/misc/likelihood_breakdown/call_accounting.py` (407 lines)** — an access-counting
instrumentation harness. It wraps a named spec of ~35 library descriptors for the duration of
one pass and reports inclusive time, **exclusive** (self) time and `n_calls` per site;
exclusive times are additive by construction. It handles `cached_property`,
`autonerves.CachedProperty` and plain `property` (which differ in whether `__get__` fires on
every access), plus module-level functions, so the solve row is the solver itself rather than
the edge subsetting around it.

Access counting rather than the sequential-touch walk the sibling numba cells use, because
`Inversion.curvature_reg_matrix` is a plain `@property` that rebuilds an `(n,n)` sum on every
access and is reached `>= 3x` per evaluation — a sequential walk measures one build and loads
the other two into its "solve" and "log det" rows. A test asserts `n_calls >= 2` so a future
PyAutoArray fix fails loudly rather than silently shifting the numbers.

**`scripts/misc/likelihood_breakdown/fixed_light_system.py` (491 lines)** — the jax-free half
of `active_set_steps.py`, extracted so a numba cell can build the S3 system without pulling
JAX into the process. `jacobi_scaled_np` promoted out of the private phase-2 module;
`linear_system_from` gained `scaling={jax,numpy}` with the jax path a function-local import so
existing pins stay bit-identical; `fixed_light_system_from` gained
`sparse_operator={drop,carry,rebake_cpu}` and now carries through
`convolve_over_sample_size_*` / `noise_covariance_matrix`, which the old rebuild silently
dropped. `active_set_steps.py` re-exports the moved names and `fixed_light_cpu_kernels` keeps
its alias, so every existing caller and pin is untouched — `test_active_set_steps.py` passes
22/22 unchanged.

**`scripts/imaging/likelihood_breakdown/fixed_light_numba.py` (2081 lines)** — the cell.
Routes a (S0) / b (S3 via the library fnnls) / c (S3 unconstrained) x `{dense, sparse_numba}`
= six rows. No certified-active-set routes: phase 2 of the GPU epic concluded a CPU
assessment should score the library's fnnls path.

**`likelihood_breakdown/__init__.py` made lazy (PEP 562)** — it eagerly imported `timing`,
which imports jax at module level, so ANY `likelihood_breakdown.*` import pulled JAX in and
the cell's no-jax guarantee was unreachable. Every consumer imports submodules, so nothing
else changes.

42 new tests; full `scripts/misc/test/` suite **440 passed**; ruff clean.

Smoke-leg gates all PASS on real HST data: P1 re-baked operator 3/3 arrays bitwise identical,
P2 D 1.31e-15 / F(mapper) 3.39e-15 at rtol 1e-9, P3 2.18e-11 nats with ZERO passive-set
differences, S3==S0 mapper-block log-dets rel 0.0. Coverage — the phase's contract — is
0.08-0.36 % unattributed on every row against a `<= 5 %` requirement. Instrumentation
overhead measured by an ABBA counterbalanced estimator at ~0.8 % (mean 1.0085, median
1.0071), against the untouched 1.03 gate; a sequential clean-vs-instrumented ratio was
drift-dominated on this hardware (0.71 to 1.37, including instrumented apparently *faster*).

## Timing legs NOT run

**This phase shipped the mechanism, not the measurement.** Legs 1 (`t1`) and 2 (`t8`) were
deliberately **not run**: the laptop was oversubscribed (load average 8.41 on 8 cores, another
session running a 4-way parallel suite, two other Claude sessions live), and leg 2 is the
thread-scaling comparison, which oversubscription makes actively misleading rather than merely
noisy. Human decision 2026-09-15: land the code, run the legs on an idle machine.

The committed artifact is the smoke leg only (N=484), stamped
`timing_status: wiring_only_not_measured`, carrying no pins (`pinned_drift` empty), so it
enters no drift surface. **No verdict note was written** —
`results/notes/fixed_lens_light_numba_2026_09.md` does not exist.

Indicative magnitudes from that smoke leg (wiring, not measurement): sparse-numba is ~4.4x
dense on S0 (452 vs 1981 ms) and S0->S3 is ~1.66x on the sparse-numba path (452 -> 272 ms)
against 1.31x on the A100. Route c costs +12.889 nats with 2 negative entries, the same order
as the GPU epic's +8.4 at N=500 HST — an independent corroboration on a different backend.

**The measurement is carried by phase 2**, `fixed-light-numba-solver`, whose prompt is
`draft/research/autolens_profiling/fixed_light_numba_phase2_source_only_solver.md` (phase 1's
t1 leg becomes phase 2's Leg A). This record is closed on the mechanism's merge, not on the
numbers; nothing in phase 1 is left half-merged.

## Traps

- **`Inversion.curvature_reg_matrix` is a plain `@property`** (`abstract.py:358-370`) that
  rebuilds an `(n,n)` sum on **every** access, and it is accessed `>= 3x` per likelihood call
  (`:613`, `:647`, `:397`); under edge zeroing two of those add a further full fancy-index
  copy. The existing numba decomposition (`delaunay_numba.py:596-672`) is a sequential-touch
  walk and therefore silently loads those rebuilds into its "solve" and "log det" rows —
  anyone reading those rows today is over-attributing to the solver. Filed separately as a
  PyAutoArray bug.
- **`likelihood_breakdown/__init__.py` eagerly imported `timing`**, which imports JAX at
  module level — so any `likelihood_breakdown.*` import pulled JAX into the process and no
  cell in that package could honestly claim to be jax-free. Fixed here by making the package
  lazy (PEP 562); a future eager import at that level re-breaks every no-JAX guarantee in the
  package silently.
- **The S3 subtraction rebuilds the dataset and drops the sparse operator**, so measuring S3
  without a re-bake would measure a path nobody runs. The re-bake is provably
  identity-preserving on the *numba* class (it recomputes `psf_weighted_data` from live data
  every evaluation, `imaging_numba/sparse.py:94-101`) but **not** on the JAX class, which
  reads a weight map baked at `apply_sparse_operator` time
  (`imaging/sparse.py:64`) — do not transplant the re-bake to the JAX path.

## Original prompt

# Numba phase 1 — the whole numba likelihood call on HST, decomposed in one process

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- pixelization
- cpu
- numba
Difficulty: large
Autonomy: human-required
Priority: high
Status: filed 2026-09-14
Epic: fixed-lens-light-numba-cpu
Phase: 1
Consequence: judge
Witness: The decomposition's exclusive-time rows plus an explicit `unattributed` row sum to the
separately measured clean call within 5 %, on every row, with instrumentation overhead <= 1.03;
and the re-baked numba sparse operator is bitwise equal to the original's on all three arrays.
Review-minutes: 25
Unattended: never
Filed: 2026-09-14

The first phase of the `fixed-lens-light-numba-cpu` campaign. Measure the whole
`AnalysisImaging.log_likelihood_function` on PyAutoArray's **numba** path — the production CPU
route, which the completed GPU epic never touched — and produce a decomposition of where that
call actually goes, measured in one process rather than attributed across two.

## Why this is phase 1 and not phase 0

The campaign map originally opened with a numba **kernel** measurement, mirroring GPU phase 0.
That phase is folded into this one, by decision 2026-09-14. GPU phase 2 already measured the
CPU kernel rows (`results/notes/fixed_lens_light_hardware_2026_09.md`) and concluded in its own
words that a CPU assessment "should score the library's `fnnls` path, not the certified active
set". Re-measuring kernels would re-answer a settled question and delay the decomposition the
campaign's `Witness:` actually demands.

## Why a decomposition, and why the existing one will not do

The GPU epic's headline is that ~21 of a 25.4 ms certified Delaunay A100 call is **not the
solver**. But that 21 ms is attribution arithmetic — phase-0 kernel rows subtracted from
phase-1 library calls, two cells, two processes — and phase 1's note says so.

The numba cells' own decomposition (`scripts/imaging/likelihood_breakdown/delaunay_numba.py`)
has a sharper version of the same problem. `Inversion.curvature_reg_matrix` is a plain
`@property` that rebuilds an (n,n) sum on **every** access, and it is accessed at least three
times per call; under edge zeroing two of those accesses each add a further full fancy-index
copy. A sequential-touch walk measures one of those builds and silently loads the other two
into its "solve" and "log det" rows. Anyone reading those rows today is over-attributing to the
solver — which is exactly the error this campaign exists to eliminate.

So this phase's mechanism is **access counting**, not sequential touching: wrap a named set of
library descriptors for the duration of one instrumented pass, maintain a call stack, and
report inclusive time, exclusive (self) time and `n_calls` per site. Exclusive times are
additive by construction. `n_calls` is what turns the multi-build from an invisible cost into a
reported one — and into a concrete PyAutoArray finding for a later phase.

## What to measure

Three routes, two formalisms, six rows:

- **a** — S0, the joint MGE-lens-light + source system the library runs today.
- **b** — S3, source-only after the lens light is converted to regular profiles and subtracted,
  solved by the library's own `fnnls`. The reference every S3 number is scored against.
- **c** — S3 with positivity dropped. Never quoted as a bare millisecond: it carries
  Δlog-evidence against **b**, the negative-pixel count and negative-flux fraction, and the fact
  that edge zeroing goes off with it.

Routes **d/d0/e** (the certified active set) are deliberately absent — the GPU harness injection
is `lax.cond`-shaped, and phase 2's note says the certified scheme is the wrong thing to time on
CPU.

Each route runs on both **dense numpy** and the **re-baked numba-sparse** dataset. The S3
subtraction rebuilds the dataset and drops the sparse operator, so without the re-bake this leg
would measure a path nobody runs.

## The parity pin

Re-baking the CPU sparse operator on the subtracted dataset is safe, and the phase must prove
it rather than assume it. Three layers, strongest first: the operator arrays bitwise equal
(it is built only from the noise map, the PSF kernel and the mask, none of which the
subtraction touches); the dense and sparse-numba S3 `data_vector` and mapper-block
`curvature_matrix` equal to 1e-9; the log-evidences equal to 1e-6 with the exact Δ in nats and
the passive-set difference count recorded beside it.

## Scope

HST, fp64, Delaunay, N=1500, on the 8-core laptop, at one and eight threads. Euclid, the
rectangular mesh, an iid instance stream and a source-pixel sweep are later phases. No
PyAutoArray, PyAutoLens or PyAutoGalaxy edits: everything is a read, a scoped
install-and-uninstall monkeypatch, or an existing public method.

`NUMBA_NUM_THREADS` must be recorded — it is absent from the shared thread-env block and a
numba millisecond is uninterpretable without it. Do not widen the shared block to add it; that
would change every existing numba cell's recorded environment and invalidate their pins.

## Deliverable

`results/notes/fixed_lens_light_numba_2026_09.md` in the format the six GPU notes set: a
provenance and gate table, the decomposition table, a "read this before quoting a number"
scope section, and a verdict — with every numerical result RECORDED rather than asserted,
since no pin exists for any numba fixed-light configuration.

## Execution

Planned and judged by a Fable / Astra session; execution delegated. Full approved plan at
`.claude/plans/` (session 2026-09-14).
