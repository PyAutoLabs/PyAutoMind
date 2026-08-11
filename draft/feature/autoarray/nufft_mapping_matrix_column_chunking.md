# Column-chunk the interferometer inversion mapping-matrix NUFFT so alma_high fits on an A100

Type: feature
Target: PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: low
Status: STOOD DOWN 2026-08-11 — premise looks overtaken; read the 2026-08-11 block first

## 2026-08-11 — stood down: the classification this prompt rests on no longer exists

Investigated to answer "is this legacy?" — **probably yes**, on the evidence
below, but the last step needs a human who knows the campaign's intent. Left in
`draft/` (not archived) so it resurfaces in the dashboard and `intake reconcile`
carrying this evidence.

### The cited classification is gone

This prompt's § Origin rests on the `interferometer delaunay @ alma_high` cell
being classified `gpu_unusable_breakdown` in autolens_profiling#59. On
autolens_profiling `main` today, **the string `gpu_unusable` appears nowhere in
the repo** — not in code, notes, or results.

The cell it names has since **run to completion on an A100**.
`results/breakdown/datacube/delaunay_hpc_a100_fp64.json` records real output for
`instrument: alma_high`, `model: delaunay`, `n_channels: 34`, on an
`NVIDIA A100 80GB PCIe`, with `transformer_chunk_size: 1000000` and a populated
`cube_log_evidence_eager` plus 34 per-channel evidences. The `mp` variant and the
two `inversion_*` variants are present too.

### Why it ran — and why that may retire this prompt

The same JSON records `"dense_breakdown": false`, and the flag's source is
explicit at `scripts/interferometer/likelihood_breakdown/datacube/delaunay.py:468`:

```python
dense_breakdown_feasible = False  # always sparse — matches production likelihood path
```

The 61.44 GB allocation this prompt exists to chunk is on the **dense** mapping-matrix
extraction path. The consumer hardcoded that path off, not as a workaround for the
OOM but because the **sparse path is what production actually uses**. So the
allocation is not merely unreachable at alma_high — it is off the path the campaign
decided to measure.

If that is right, the column axis has no live consumer, and this is legacy.

### Revisit when

1. Someone wants `dense_breakdown_feasible = True` back — i.e. the dense
   decomposition is judged worth measuring again. **This is the load-bearing
   trigger**; without it there is no consumer.
2. A production (non-breakdown) code path is found that takes the dense
   mapping-matrix extraction at alma_high scale. Not found in this pass, but this
   pass read the profiling repo, not every library caller.

### What is NOT the reason to retire it

The § below correctly states that the sibling `nufft_simulator_chunking` gather-axis
chunking "does nothing for this allocation". That is still true and is not affected
by any of the above — the two axes remain orthogonal. This prompt stands down on
*absence of a consumer*, not on the sibling having covered it.

**Before retiring, confirm with whoever set `dense_breakdown_feasible = False`**
that it is a permanent design call rather than a temporary measurement choice. That
one answer decides retire-vs-revive, and it is not inferable from the tree.

---

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
