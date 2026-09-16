# Fixed-light follow-up round 3 — the non-solver levers on numba CPU and the A100 together

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoArray
Themes:
- profiling
- pixelization
- cpu
- numba
- gpu
- inversion
Difficulty: large
Sizing-note: the intake sizing faculty derived too-large (score 15); large is kept per this prompt's own
instruction under "Scope and guards" — if it must be split, split along the levers (1, then 2, then 3),
never between a lever and its A100 row.
Autonomy: human-required
Priority: high
Status: formalised
Epic: fixed-lens-light-numba-cpu
Phase: 3
Consequence: judge
Witness: At HST Delaunay N=1500 on both hosts, each lever returns the library's own log evidence
to <= 1e-9 relative; the rebuilt regularization matrix is bit-identical to the retained pure-Python
reference on the numba path; the phase-2 cell's decomposition sums to the measured clean call within
1 %; and the note carries one before/after whole-call table per host (RAL numba CPU, A100 fp64) with
every thread and backend block recorded per leg.
Review-minutes: 30
Unattended: never
Filed: 2026-09-16
Issued: 2026-09-16
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/267

## Original request (verbatim)

> Ok so have we finished the nnls speed up? HAppy if so but want to mark that milestone and
> complete issue and intake new issue for the next round of follow up (Which will be paired with
> A100 speed up)

## Where the campaign stands — the NNLS round is closed

Phase 2 (autolens_profiling#265, PR #266) answered the solver question and the answer is **no
further solver work**:

- **Fixing the lens light is worth 2.03x on the production numba CPU path** — HST Delaunay
  N=1500, sparse numba operator, 1 thread, RAL SLURM job 343311 on an idle `gpu`-partition node
  used CPUs-only: route a (S0 joint, 1560 params) **932.387 ms** -> route b (S3 source-only,
  1500 params) **459.220 ms** on medians, with **no library change at all**, corroborated at
  2.036x on a second host and a different CPU vendor.
- **The solver is finished.** The library's own cross-evaluation NNLS memo — ON by default and
  therefore already in production — takes the call to **404.597 ms (1.134x)**; the factor-reuse
  NNLS built for phase 2 reaches only 412.556 ms (1.112x). They are 1.97 % apart, so the
  conditional `nnls_seed_factor_reuse` PyAutoArray prompt phase 2 was authorised to file was
  **deliberately not filed**. What is left inside `fnnls_cholesky` is ~37.7 ms, 9.3 % of the
  call, against an unconstrained floor — a <= 1.1x lever. This phase does not reopen it.

This phase goes after what phase 2's own verdict named as bigger than the solver, and pairs each
lever with the A100, which is what the request asks for.

## The residue this phase attacks

Leg D, route b, memo ON (`results/breakdown/imaging/fixed_light_numba_delaunay_hpc_ral_cpu_fp64_fixed_light_numba_sparse_b_warm_t1.json`),
the 404.597 ms call production actually pays. Exclusive per-site ms:

| site | ms | % of 404.6 ms call |
|---|---:|---:|
| `inversion.regularization_matrix` | **111.501** | **27.6** |
| `sparse_numba.curvature_matrix` | 87.416 | 21.6 |
| `solver.fnnls_cholesky` | 62.789 | 15.5 |
| `inversion.log_det_curvature_reg_matrix_term` | 40.172 | 9.9 |
| `inversion.log_det_regularization_matrix_term` | 37.468 | 9.3 |
| `delaunay.triangulation` | 18.508 | 4.6 |
| `inversion.curvature_reg_matrix` (`n_calls` = 2) | 4.056 | 1.0 |

**The three target sites are 189.1 ms, 47 % of the call**, and every one of them is invariant
under the memo — Leg A's memo-off decomposition reads 112.252 / 40.803 / 37.753 ms for the same
three. The solver's share moves with the memo; these do not.

The A100 counterpart, from the paired campaign map
(`draft/research/autolens_profiling/hst_gpu_non_solver_residue_programme.md`, epic
`hst-gpu-non-solver-residue`): of the certified 25.39 ms Delaunay call at HST N=1500, the
`F + lambda*H` build is **4.92 ms**, the two log-dets **1.17 + 1.20 = 2.37 ms**, and
**~13.9 ms is mesh, mapper and weights** — i.e. ~21 of 25.4 ms is not the solver there either.
Those GPU numbers are that map's phase-1 *attribution*, not a measured decomposition; this phase
measures its own A100 rows rather than quoting them as truth.

## The three levers, in order — 1, then 2, then 3

### Lever 1 — jit the split-regularization assembly on the numpy/numba path

`AdaptSplit` / `ConstantSplit` / `AdaptiveBrightnessSplit` build their regularization matrix
through two **pure-Python loops** in PyAutoArray:

- `reg_split_np_from` — `autoarray/inversion/regularization/regularization_util.py:115-168`
- `pixel_splitted_regularization_matrix_np_from` — `:274-312`, a 4-deep loop doing
  **~120k interpreted scalar writes** into a dense `(P, P)`

The file contains **zero numba** (`grep -n "numba_util\|@numba"` returns nothing). PyAutoArray#536
(`04152bb7`, "compact the ConstantSplit split-stencil scatter") optimised the **JAX branch of
`pixel_splitted_regularization_matrix_from` only** and explicitly left the numpy path alone. That
is why this is the largest site in the numba call and why no cost model in the campaign flagged it.

**The fix.** Two `@numba_util.jit()` kernels replicating the accumulation order **bit-for-bit**:
the `2e-8` diagonal jitter written first, both-triangle adds in the same `l` / `l+m` order, the
trailing `/= 2.0` on the diagonal last. Wrap them in copy-then-jit functions that keep the public
`_np_from` names, because `test_autoarray/inversion/regularizations/test_pixel_splitted_jax.py`
uses `pixel_splitted_regularization_matrix_np_from` as its ground truth for the JAX branch
(lines 74-75, 121, 139, 152, 181, 221). Three defects to fix while the loops are being rewritten,
each of which must be recorded as a behaviour change rather than smuggled in:

1. **The inputs are mutated in place.** `reg_split_np_from` writes
   `splitted_mappings[i][j+1]`, grows `splitted_sizes[i]` and writes into `splitted_weights`, and
   the arrays it is handed come from the interpolators' **`cached_property` `_mappings_sizes_weights_split`**
   tables (`autoarray/inversion/mesh/interpolator/knn.py:391+`, and the Delaunay sibling). Copy on
   entry. **Read `knn.py:374` and `:428-432` before touching this** — those comments document the
   in-place growth and the reserved pad column as deliberate, so the copy must preserve the
   returned `(mappings, sizes, weights)` contract and the pad column, not remove them.
2. **The `size == 0` `j`-leak.** `for j in range(splitted_sizes[i])` leaves `j` from the previous
   row when a row is empty, and the flag-zero branch then writes at `j + 1`. Use an explicit
   `insert = sizes[i]`.
3. **No bound on the insert.** Guard `insert < K` before writing into the reserved column.

Keep the current pure-Python bodies as `_reference` implementations and pin the jitted kernels
against them in the test suite — the precedent is
`autoarray/inversion/mesh/interpolator/rectangular.py:144-160`, where a windowed numba kernel
replaced a blocked numpy sum and the numpy implementation is retained as the JAX-path reference.

**Expected.** 111.5 ms -> a few ms; whole call ~405 -> ~295 ms, **~1.37x**. That is the single
largest number available anywhere in this campaign.

**A100 row.** Confirm that #536's compacted scatter is the path the A100 Delaunay cell actually
runs (`SPLIT_REG_COMPACT_WIDTH`, `SPLIT_REG_WIDE_ROW_BUDGET`, the wide-row supplement and the NaN
overflow poison), then **measure** it, rather than assuming the GPU map's attributed
`F + lambda*H` 4.92 ms already covers it. If the compaction is not on the running path, that is
the A100 finding of lever 1.

### Lever 2 — `log_det_regularization_matrix_term` factorises a sparse matrix densely

`AbstractInversion.log_det_regularization_matrix_term`
(`autoarray/inversion/inversion/abstract.py:896-941`) falls through to `_log_det_symmetric_from`
(`:850-880`), i.e. a **dense `cholesky` of `regularization_matrix_reduced`** — a matrix with
~20 non-zeros per row at N=1500 under the split stencil. 37.5 ms on numba CPU.

Two things to establish before optimising:

- **The docstring at `:903` is stale.** It claims the term "uses scipy sparse linear algebra to
  solve the determinant efficiently". It does not. Fix the docstring in whatever PR touches this,
  regardless of which option below lands.
- **The shortcut is not reachable by default.** `log_det_regularization_matrix_term_from` is
  consulted only under `settings.log_det_method == "slogdet"` **and**
  `all_linear_obj_have_regularization`, and it returns `None` for every non-kernel scheme — so on
  the default `"cholesky"` path with `AdaptSplit` it never runs.

**Options, in the order to try them:** `scipy.sparse.linalg.splu` log-det on the numpy/numba path;
a banded Cholesky after an RCM permutation; or a cache keyed on the mesh and weights — noting that
`AdaptSplit`'s weights **move with the adapt image**, so a "mesh is fixed" cache is wrong for the
scheme this campaign actually measures. Whichever lands must leave the JAX/GPU branch untouched.

**A100 row.** Measure the dense counterpart on the GPU (the map attributes 1.20 ms to `log det(H)`),
so the verdict says whether this lever is CPU-only or worth carrying to both.

### Lever 3 — one shared Cholesky of `F + lambda*H` for the solve, the seed and the log-det

`log_det_curvature_reg_matrix_term` (`abstract.py:882-893`) calls `_log_det_symmetric_from` on
`curvature_reg_matrix_reduced`, i.e. a **full `potrf` of `F + lambda*H`**. The same matrix is
factorised twice more in the same call:

- `fnnls_cholesky` (`autoarray/util/fnnls.py:102-120`) factorises the warm-start passive set once
  into `U_buffer` and keeps it — Leg B measured `n_passive` 1485 of n=1500 on the library's own
  cold row (1483-1490 across the Leg B rows) — and **never returns that factor**;
- the dense seed `np.linalg.solve(curvature_reg_matrix, data_vector) > 0`
  (`autoarray/inversion/inversion/inversion_util.py:434-436`) factorises it again to decide the
  starting passive set. That seed is exactly what the memo removes: Leg D shows
  `solver.reconstruction_positive_only_from` collapsing 59.811 -> 7.545 ms while
  `fnnls_cholesky` is unchanged.

At a passive set of ~1485 of 1500 the three factorisations are **bit-identical work**. The lever is
**one shared full Cholesky**: seed via `cho_solve` from it, have `fnnls` down-date the handful of
active columns out of it (`choldeleteindexes_inplace`, `autoarray/util/cholesky_funcs.py:243`, which
`fnnls_cholesky` already calls — Leg B's K3 row measured **1 factorisation and 15 downdates**)
instead of factorising a fresh k x k, and read the log-det off the same factor.

**S3 only.** Route a solves 1560 parameters against the reduced system's 1500, and its NNLS runs
23 outer / 10 inner iterations against route b's 0 / 1, so the shared-factor argument holds only
for the source-only system this campaign is about. Do not quote it for S0.

**Fold in the `curvature_reg_matrix` rebuild bug.**
`draft/bug/autoarray/curvature_reg_matrix_rebuilt_every_access.md` is the same matrix, the same
property: `AbstractInversion.curvature_reg_matrix` (`abstract.py:358-370`) is a plain `@property`
doing an out-of-place `_xp.add`, and the Leg D JSON measures it at `n_calls` = 2, 4.056 ms. Phase 1's
test asserting `n_calls >= 2` on that property is the **intended handshake**: if this phase lands a
cache, that assertion fails loudly and the published decomposition is updated deliberately. Resolve
the bug prompt's first question (is the stale-cache hazard its docstring describes still real?) as
part of this lever, and if the honest answer is "the hazard is gone, fix the docstring only", that
is a complete outcome for that part.

**A100 row.** `log det(F + lambda*H)` is attributed 1.17 ms there; measure whether the shared-factor
saving survives on a device where the factorisation is launch-bound.

## Pairing — every lever gets a CPU row and an A100 row

This is the "paired with A100 speed up" the request asks for, and it is a per-lever requirement,
not a follow-up phase.

**CPU leg.** RAL `gpu` partition **CPUs-only** — `--partition=gpu --cpus-per-task=4 --mem=32gb`
and **no `--gres`**, so the A100s stay free; the `ral` CPU partition has been saturated for days
and the idle `imp` partition does not mount `/mnt/ral`. `NUMBA_NUM_THREADS=1` and the whole BLAS
family (`OMP`/`OPENBLAS`/`MKL`/`VECLIB`/`NUMEXPR`) pinned to 1, recorded per leg in
`configuration.thread_env` / `numba_thread_env`. A/B the library change against a **private
merge-base PyAutoArray checkout on `PYTHONPATH`** — never against the shared
`/mnt/ral/jnightin/PyAuto` install, which other work depends on. Laptop legs are corroboration
only (phase 2 measured 70.9-187.6 % clean spreads there against RAL's 0.77-16.25 %).

**A100 leg.** fp64, budget 7 on Delaunay, PDIP fallback, positivity never dropped — the same cell
family and settled configuration as the `hst-gpu-non-solver-residue` map. The A100 legs have a
submit -> wait -> harvest step, which is a **human resume point, not a park**.

**Pins, on every leg of both hosts:**

- the library's own **log evidence** to **<= 1e-9 relative** (the standard both epics have met);
- the **regularization matrix bit-identical** to the retained pure-Python `_reference`, asserted
  on the numba path, not merely close;
- `log_likelihood` is **not comparable across legs** — `--instances iid` rotates a call index and
  route counts differ between legs (phase 2's route b read 19651.457885 in Leg A and 18665.014334
  in Legs C and D). Compare per-instance, per-leg only.
- no comparison crosses a thread setting silently; route c (positivity off) is a diagnostic and
  never a headline millisecond.

## Witness

At HST Delaunay N=1500 on both hosts, each lever returns the library's own log evidence to
<= 1e-9 relative, the regularization matrix is bit-identical to the retained Python reference on
the numba path, the phase-2 cell's decomposition sums to the measured clean call within 1 %, and
the verdict note carries one before/after whole-call table per host with the thread and backend
blocks recorded per leg.

## Scope and guards

**In.** Library edits in PyAutoArray, witnessed from `autolens_profiling` using phase 2's existing
cells (`scripts/imaging/likelihood_breakdown/fixed_light_numba.py`, `call_accounting.py`) and the
A100 Delaunay cell. The JAX branch of the split-regularization assembly is **untouched** — #536
owns it and its compaction is exact by a different argument.

**Out.** Rectangular meshes; Euclid; the sparse-operator / profile-subtracted-image bug
(`draft/bug/autoarray/sparse_inversion_ignores_profile_subtracted_image.md`); JWST; any reopening
of the NNLS solver scheme; and **the memo-robustness question, which moves to phase 4** (does
`seed_source` stay `"memo"` and `warm_start_fallback` stay false over the seeded graded draw set,
or does a bad model pay the cold 116 ms path?).

**If intake sizes this too-large**, split it along the levers rather than along the hosts: **this
phase carries lever 1** (the jitted split-regularization assembly, the biggest and most independent
of the three) and the campaign map holds **levers 2 and 3 as phases 3b and 3c**. The CPU/A100
pairing stays inside whichever phase carries a lever — it is the pairing that makes a lever a
verdict, so never split a lever from its A100 row.

## Execution

Fable plans and judges; Opus subagents execute with a progress heartbeat. **One lever at a time,
in order 1 -> 2 -> 3**, each landing its own PyAutoArray PR (pending-release) plus an
`autolens_profiling` follow-up PR carrying the cell changes, the JSONs and the note. `/prm` is
human. The deliverable is a `results/notes/` verdict note in the format of the six GPU notes and
phase 2's own — provenance and gate table, before/after decomposition per host, per-lever verdict,
and a "read this before quoting a number" scope section.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b7af7f44-1297-458f-858f-91aada0b33f1/scratchpad/intake_draft_fixed_light_round3.md -->
