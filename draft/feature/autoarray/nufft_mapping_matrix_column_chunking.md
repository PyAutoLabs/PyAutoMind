# Column-chunk the interferometer inversion mapping-matrix NUFFT so alma_high fits on an A100

Type: feature
Target: PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

## Origin

Filed from the `PreOptimizationTimes` breakdown campaign (autolens_profiling#59,
A100 tier). The `interferometer delaunay @ alma_high` cell is the one profiling
cell that cannot be decomposed on an A100 (80 GB) — classified
`gpu_unusable_breakdown`. It is a real library memory gap, not a profiling-tool
issue, so it is broken out here rather than fixed in the profiling repo.

## The blocker

The inversion path extracts the mapping matrix by NUFFT-ing **every mapping-matrix
column onto the fine real-space grid at once**. At alma_high scale that is all
**1500 source columns** onto the **1600² fine grid** in a single allocation:

```
1600 × 1600 × 1500 × 16 B = 61.44 GB      (exactly the failed A100 allocation)
```

The `16 B` is complex128 (fp64). At mixed precision (complex64, 8 B) the same
buffer is ~30.7 GB, so an `mp` run *might* fit — worth confirming, but fp64 is
the design center and must not OOM.

Crucially, the transformer's existing **1M-visibility chunking chunks the
*gather* (over visibilities `M`), not the *columns*** — so it does nothing for
this allocation, which is bounded by `N_fine_grid × N_source_columns`. There is
no escape valve on the column axis.

## The fix

Add **column-chunked mapping-matrix NUFFT** at the PyAutoArray/nufftax boundary:
batch the mapping-matrix columns (e.g. in blocks of a few hundred), NUFFT each
block, and assemble the extracted matrix block-by-block. The extraction is linear
in the column block, so the result is bit-identical to the one-shot call.

Plumbing concerns (mirror the sibling prompt's lessons — see below):
- Put the knob where the column loop lives (the inversion-matrix extraction in the
  interferometer transformer / `apply_sparse_operator` region — grep the extraction
  path that feeds the delaunay/pixelization inversion, not the simulator forward).
- Default to "no chunking" so small-N callers (`sma`, ~190 visibilities / few
  hundred columns) pay no overhead.
- Use `jax.lax.scan` / `jax.lax.map` for the column loop, **not** a Python `for` —
  a Python loop unrolls in JAX and blows up JIT compile time as
  `N_columns / chunk_size` grows.
- Pick the default chunk size by memory budget:
  `N_fine_grid_px × chunk_columns × dtype_size` under a ~40 GB A100 working budget.

## Related / cross-reference

- [[nufft_simulator_chunking]] — the **sibling** memory gap on the *simulator
  forward* NUFFT (chunks over visibilities `M`, OOMs at ~5M vis). Same nufftax
  memory-ceiling family, **different axis and code path** (visibilities vs
  mapping-matrix columns; simulator forward vs inversion extraction). Land the two
  independently but keep the chunking idiom consistent.

## Scope / validation

- In scope: fp64 correctness (bit-identical to one-shot) + A100 fit at alma_high;
  the `mp` fit check.
- Out of scope: the *fused runtime* likelihood path — phase 3 already marks
  alma_high runtime as GPU-only and its A100 runtime legs will report whether the
  fused path fits without this change. This prompt is specifically the **extraction
  / breakdown** path.
- Once landed, the autolens_profiling alma_high breakdown cell can be re-run and
  its `gpu_unusable_breakdown` classification lifted.

<!-- filed 2026-07-11 from autolens_profiling#59 comment (A100 breakdown tier) -->
