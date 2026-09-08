## delaunay-nn-constant-split-assembly

- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/536
- completed: 2026-09-08
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/537
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/309
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/231
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/537
- scope: **whole prompt** — the investigation priced every candidate reformulation, the winner shipped, and the pin is unchanged, so nothing is left over. The follow-ups below are new levers the measurement exposed, not unshipped scope.

### What shipped

The JAX path of `regularization_util.pixel_splitted_regularization_matrix_from` scattered the
full `(4P, K, K)` outer product of the split stencil. For the natural-neighbour `DelaunayNN`
mesh the stencil tables are padded to `K = 33` (`SIBSON_MAX_NEIGHBORS` 32 + 1 self column)
while the real occupied width on a production HST cell is min 1 / median 5 / p99 9 / max 11 —
so ~97 % of the 6.5 M scattered entries per lane were padding, at a cost **quadratic** in the
padded width. This was the largest remaining block of the DelaunayNN params→H prefix after
Phase A (PyAutoArray#533).

It now scatters only the first `kc = min(K, 12)` columns and supplements the 256 widest rows
with the head×tail, tail×head and tail×tail blocks the compact pass did not cover, in one
masked `.at[].add`.

- **The result is exact, not approximate.** Padded columns carry mapping `0` / weight `0`, so
  a row whose occupied size is `≤ kc` is reproduced bit-for-bit by the compact pass alone.
- **Width 12 was measured, not guessed** — `SPLIT_REG_COMPACT_WIDTH = 12`, from the sweep
  below.
- **Top-256 widest rows** — `SPLIT_REG_WIDE_ROW_BUDGET = 256`, selected by `jax.lax.top_k` on
  the *integer* `splitted_sizes`, which is not differentiated through, so the Sibson weights
  stay fully differentiable (no `stop_gradient` was needed).
- **NaN on budget overflow**, never silent truncation — the same convention
  `mesh/interpolator/sibson.py` already uses for its neighbour caps: the likelihood evaluates
  to NaN and the sampler discards the sample.
- **`K ≤ 12` callers are untouched** — the `Delaunay` mesh's `K = 4` and the adapt-split family
  take today's single scatter, no supplement, no guard. **The NumPy path is unchanged.**

Plus the evidence machinery: `scripts/misc/delaunay_nn/assembly_bench.py` in
`autolens_profiling` (V0–V6 variants + the width sweep, run against frozen real HST tables),
the A100 A/B submits, and the parity assertions and per-geometry wide-row count in
`autolens_workspace_test`'s `jax_assertions/delaunay_nn{,_caps}.py`.

### The numbers (A100, jobs 342334–342338, same node, same window)

| | before | after | |
|---|---:|---:|---|
| assembly row, per call @`vmap` 16 | 10.03 ms | **0.84 ms** | **12.0×** |
| params→H prefix, per call @`vmap` 16 | 16.423 ms | **7.260 ms** | **2.26×** |
| params→H prefix, unbatched | 24.341 ms | **15.189 ms** | **1.60×** |
| whole likelihood, single JIT | 75.6 ms | **66.1 ms** | **1.14×** |
| whole likelihood, per call @`vmap` 16 | 50.04 ms | **40.86 ms** | **1.22×** |

Full note (design, priced alternatives, width sweep, cap audit):
`autolens_profiling/results/notes/delaunay_nn_constant_split_assembly.md`.

### Witness verdict — met, with margin

The pre-registered witness asked the assembly row to drop from 10.0 ms/call to **under 3 ms**
and the params→H prefix from 16.4 to **under 11 ms**, with
`EXPECTED_LOG_EVIDENCE_HST = 29144.581944` unchanged and the `delaunay_nn.py` jax_assertions
passing. All four met: **0.84 ms** and **7.260 ms**, the pin **bit-identical** on both legs
with `pinned_drift: []`, and the assertions pass. The pin held exactly because this is a pure
reformulation — the tolerance clause the prompt allowed for a summation-order change was never
needed.

### Why width 12, and why not the alternatives

Investigation jobs 342331/342332 priced every candidate on the same real HST tables *before*
the design was fixed — this is the bench choosing the design, not confirming it:

| approach | A100 fp64 ms/call | verdict |
|---|---:|---|
| compact scatter, width 12 (shipped) | 0.58 | chosen |
| dense GEMM assembly | 10.1 | a wash with today's scatter |
| BCOO sparse assembly | 21 | 2× worse |
| dedup / segment-sum assembly | 39 | 4× worse |
| today's scatter (width 33) | 10.03 | baseline |

Compact-width sweep (`vmap` 16, real HST tables): 12 → 0.58 ms, 16 → 1.47, 20 → 2.78,
24 → 4.53, 28 → 6.71, 32 → 9.31, 33 (uncompacted) → 10.03. Width 12 is **17× on GPU and 5.8×
on CPU** over the uncompacted scatter (12.6 vs 72.8 ms/call), so no backend gate was needed —
unlike Phase A's unroll, which had to be gated off CPU.

The prompt's third candidate — truncating the regularization stencil to its k largest weights
— was **not needed and not taken**: it would have changed the regularization scheme and the
pin, and the exact compaction reaches the witness without it. That science decision stays
unmade.

### The budget is sized against a real ensemble

The cap audit (`delaunay_nn_caps.py`) over **101 ensemble geometries**, 4800 split rows each,
sees a **max of 50** rows wider than 12 and a **mean of 2.8** — a ~5× margin to the 256
budget. The widest single stencil in that ensemble is 21 natural neighbours (99.9th pct 11,
99.99th pct 15). The NaN overflow path is therefore never reached on audited data; it is a
contract, not a live branch.

### Caveats

- **The differenced "H, ConstantSplit assembly" cell reads −1.6 ms on the feature leg.** That
  is a prefix-boundary artifact of the differencing, not a negative cost: the row is a
  subtraction of two prefixes and the assembly is now small enough that the boundary noise
  exceeds it. **Judge on `regularization_matrix_prefix_s`** (the params→H prefix), which is
  the row the witness was written against. This is the same class of trap as Phase A's
  35.4 → ~0 ms "Split-point Sibson" collapse.
- **The wide-row supplement costs ~0.26 ms/call on geometries that never use it** — it is
  unconditional work in the traced graph, since which rows are wide is not known at trace
  time. On a `K ≤ 12` mesh it is not emitted at all.

### Follow-ups

- **The cavity early exit (Phase B of the Phase A prompt) is now the largest single lever on
  the params→H prefix** — ~1.3 ms/call, ≈ 3 % of an evaluation. It was deferred at the Phase A
  close-out precisely because the assembly was worth 10 ms and it was worth 1.3; with the
  assembly gone it is the top of the list. Still unfiled: re-cost it against the post-#537
  figures before planning.
- **The profiling cells all use `ConstantSplit`, whereas production SLaM pipelines use
  `AdaptSplit`.** The human's call at close-out: the DelaunayNN cell should be re-based on
  `AdaptSplit`, like the Delaunay pipelines already are, and the remaining prefix re-costed —
  the shipped compaction applies to both (both go through the same changed function), but the
  *share* of an evaluation it recovers is measured on a geometry production does not run.
  Re-cost, then decide what the next lever is.

### Traps worth remembering

- **Padded-width cost is quadratic.** The stencil tables are padded to the cap
  (`SIBSON_MAX_NEIGHBORS`), and anything forming a `K × K` outer product over them pays `K²`
  for a median occupancy of 5. Raising a neighbour cap therefore costs the regularization
  assembly quadratically, not linearly — worth remembering the next time a cap is raised.
- **`top_k` on an integer size array is gradient-safe.** Row selection had to not disturb
  differentiability of the weights; keying it on `splitted_sizes` (integers, never
  differentiated) rather than on the weights themselves is what avoided a `stop_gradient` that
  would have needed the same justification `_jax_delaunay_tables` and the walk carry.
- **A "N commits behind origin" Heart reading mid-ship is local staleness**, not a real RED —
  ff-pull the canonical checkout and tick vitals.

### Heart

- heart-ack: 2026-09-08 in-session, YELLOW score 70, two reasons "workspace validation not
  passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb,
  autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"
  and "release validation incomplete: no rehearsal for current source" — organism-scope; the
  cloud smoke run predates this branch and the two delaunay legs it names
  (`jax_grad/delaunay.py`, `jax_likelihood/delaunay.py`, both `reg.AdaptSplit` through the
  changed function) were re-run on this branch and both pass.

### Notes

- CI at close-out: PyAutoArray#537 Tests 3/3 legs green (unittest 3.12, 3.13, unittest-nojax);
  autolens_workspace_test#309 Smoke Tests 3/3 green (changes, smoke 3.12, smoke 3.13) — Heart's
  reusable smoke workflow branch-matches the library checkout, so it exercised the feature
  branch of PyAutoArray, not `main`; autolens_profiling#231 lint green. No freeze window open.
- 1,468 PyAutoArray unit tests pass, including a new
  `test_autoarray/inversion/regularizations/test_pixel_splitted_jax.py` (8 tests: compact-vs-full
  parity on padded tables, the `K ≤ kc` no-op path, wide-row supplement exactness,
  NaN-on-overflow, NumPy/JAX agreement).
- `autolens_profiling` was under a three-way parallel claim (`retire-gpu1-mig-exclusion`,
  `interferometer-preload-cpu`); file sets were disjoint and the worktree was taken under the
  same precedent. No conflict materialised.

## Original prompt

# DelaunayNN ConstantSplit regularization assembly: the 10 ms per call that Phase A left behind

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
- autolens_workspace_test
Themes:
- jax-gpu
- delaunay
- profiling
- performance
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: on the A100 DelaunayNN breakdown (`results/breakdown/imaging/delaunay_nn_hpc_a100_fp64_launch_latency.json` is the post-#533 baseline) the "Regularization matrix (H, ConstantSplit assembly)" row drops from 10.0 ms per call at vmap 16 to under 3 ms and the params→H prefix (`regularization_matrix_prefix_s`) from 16.4 ms per call to under 11 ms, with `EXPECTED_LOG_EVIDENCE_HST = 29144.581944` unchanged (or, if the assembly is reformulated so the fp summation order changes, matching to a stated relative tolerance with the change justified) and the `delaunay_nn.py` jax_assertions passing
Review-minutes: 40
Unattended: ready
Filed: 2026-09-08
Issued: 2026-09-08

Original request (verbatim):

> i agree with your recommendation but its bed soon so once its a good time to stop do that too, but getting some prm done first is good!

(The recommendation agreed to: after DelaunayNN Phase A shipped as PyAutoArray#533, point the
next prompt at the ConstantSplit assembly rather than the cavity early exit.)

## The measurement (A100, post PyAutoArray#533, `results/notes/delaunay_nn_launch_latency.md`)

Phase A cut the DelaunayNN params→H prefix from 143.9 to 28.2 ms unbatched (5.1×), but only
from 24.3 to 16.4 ms per call at vmap 16 (1.48×). The new split-Sibson breakdown stage
(autolens_profiling#227) attributes the remaining per-call cost: the data-side Sibson pass is
~6.4 ms per call, the split-side Sibson ~1 ms, and the **ConstantSplit regularization
assembly ~10.0 ms per call at every chunk size and on the control** — 143× barycentric
Delaunay's equivalent H row (0.07 ms per call) and ~19 % of the 52.6 ms batched whole
likelihood. The assembly is `reg_split_from` fed by `InterpolatorDelaunayNN._mappings_sizes_weights_split`:
6,000 split-cross points, each with a 33-wide (32 neighbours + 1 spare column) Sibson stencil,
scattered into the N×N regularization matrix — ~6.5 M scatter entries per lane versus
~96 k for Delaunay's 4-wide stencil.

The planned "Phase B" cavity early exit targets only the ~6.4 ms Sibson share and is worth
~1.3 ms per call; it is deferred in favour of this.

## Investigation first (one A100 session, then decide)

1. Instrument the assembly: time `reg_split_from` alone under `jax.jit` and `jit(vmap)` at
   batch 16 on the production tables (N = 1500, S = 6000, width 33) and identify whether the
   cost is the scatter-add (`.at[].add` into N×N), the gathers over the padded stencil, or
   the `hstack` spare-column plumbing. Compare against the 4-wide Delaunay call on the same
   inputs to calibrate.
2. Candidate reformulations, measured on the same session:
   - **Dense matmul**: build the split mapping matrix `M_s` (S × N, 33 non-zeros per row) as a
     dense array and form `H = M_sᵀ diag(w) M_s` (or the actual ConstantSplit combination) as
     one GEMM: 6000 × 1500 × 1500 ≈ 13.5 GFLOP per lane, ~0.2 TFLOP at batch 16, i.e. ~10 ms
     fp64 on an A100 — no better unless the split combination lets the GEMM shrink, so measure
     before believing.
   - **Segment-sum over stencil pairs**: sort the (i, j) pairs once per fit (they depend only on
     the frozen tables) and accumulate with `segment_sum` instead of a random scatter into N×N.
   - **Stencil truncation for the regularization only**: keep the 32-wide Sibson stencil for the
     data mapping but regularize the split points with their k largest weights (k = 8–12,
     renormalized). This changes the regularization scheme and the pin; it is a science
     decision to be presented, not taken.
3. Ship the winner that keeps the pin unchanged, or present the pin-changing one with its
   evidence-tolerance argument.

## Contracts

- `EXPECTED_LOG_EVIDENCE_HST` in `scripts/imaging/likelihood_breakdown/delaunay_nn.py` stays
  unchanged for any pure-reformulation change; a pin shift is a bug unless the reformulation
  is explicitly a summation-order change, in which case the note states the tolerance.
- Judge on `regularization_matrix_prefix_s` and the new "ConstantSplit assembly" row.
- Gradient: the assembly is differentiable through the Sibson weights; any `stop_gradient`
  must be justified the way `_jax_delaunay_tables` and the walk do.
- `SIBSON_MAX_NEIGHBORS` / caps unchanged unless the truncation option is chosen.

## Verification on the A100

Same-node control (merge base) vs feature A/B with
`scripts/imaging/likelihood_breakdown/delaunay_nn.py --config-name hpc_a100_fp64 --split-setup
--vmap-batch 16` plus the runtime cell; report all rows unbatched and per call at vmap 16,
against the post-#533 baseline.

Related: `complete/2026/09/delaunay-nn-launch-latency.md` (Phase A record),
`results/notes/delaunay_nn_launch_latency.md` (numbers), the deferred cavity early-exit
(Phase B of the Phase A prompt) which stays unfiled until this lands.
