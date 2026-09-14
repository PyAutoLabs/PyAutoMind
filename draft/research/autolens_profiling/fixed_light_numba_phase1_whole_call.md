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
