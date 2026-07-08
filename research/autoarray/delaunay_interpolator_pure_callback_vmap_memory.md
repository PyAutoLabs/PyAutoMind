# PyAutoArray Delaunay interpolator's `pure_callback` vs vmap — minor efficiency follow-up

Type: research
Target: PyAutoArray
Difficulty: too-large
Autonomy: supervised
Priority: low
Status: formalised

## Status

**Not the root cause of the NSS Delaunay A100 OOM.** The control test
(NSS pixelization × HST × fp64, A100 job 322604) crashed at
**28,055,330,400 bytes** — identical site (`mapper_util.py:315` →
`scatter_op`), within 1.4% of NSS Delaunay's 27,668,233,200 bytes —
despite `RectangularAdaptImage` using zero `pure_callback`. The OOM
is a vmap-fan-out × inversion-scatter problem; see
`PyAutoPrompt/autofit/nss_chunked_vmap_for_inversion_heavy_likelihoods.md`
for the actual fix.

This prompt is kept as a minor efficiency cleanup — the `pure_callback`
in the Delaunay interpolator still adds compile-time HLO surface and
host-callback round-trips that aren't free, even if they aren't what
runs the GPU out of memory.



## Context

Surfaced by the first-class A100 NSS profiling sweep in
`autolens_profiling/searches/`. The HST MGE × fp64 cell completes
cleanly with NSS (12.1 ms/eval Nautilus → 1.61 ms/eval NSS; jobs
322560, 322590). The HST **Delaunay** × fp64 cell completes for
Nautilus (84.8 ms/eval, job 322601) but **every** NSS attempt OOMs
the A100 at ~27.7 GB allocation:

```
jaxlib.xla_extension.XlaRuntimeError: RESOURCE_EXHAUSTED:
  Out of memory while trying to allocate 27668233200 bytes
  in PyAutoArray:autoarray/inversion/mappers/mapper_util.py:315
    mat = mat.at[flat_parent, flat_pixidx].add(flat_contrib_out)
```

The OOM **site** is the mapping-matrix scatter (image_pixels ×
source_pixels). The **likely cause** is one step upstream — the
Delaunay triangulation at
`PyAutoArray:autoarray/inversion/mesh/interpolator/delaunay.py:80-94`,
which wraps `scipy.spatial.Delaunay` via `jax.pure_callback`:

```python
return jax.pure_callback(
    lambda points, qpts: scipy_delaunay(
        np.asarray(points), np.asarray(qpts), areas_factor
    ),
    (points_shape, simplices_padded_shape, mappings_shape,
     split_points_shape, splitted_mappings_shape),
    points, query_points,
    vmap_method="sequential",
)
```

This is the only `pure_callback` in the Delaunay likelihood path.
`vmap_method="sequential"` correctly avoids parallel host-callback
fan-out, but the JIT-lowered XLA HLO still has to thread the
5-element output pytree through each vmap instance — and downstream
ops (the scatter at `mapper_util.py:315`) operate on the
callback's outputs.

The project memory note `feedback_jax_pure_callback_const_fold.md`
records a related lesson on this same code: under
`jit.lower().compile()` `pure_callback` outputs were getting
constant-folded as XLA constants. That meant the JIT compile was
*caching the host callback's result*, producing single-JIT-vs-vmap
discrepancies of 20-30× speedup. The mechanism here would be the
mirror image: under vmap (where the constant-fold doesn't apply
because each instance has different inputs), the HLO retains the
full callback-output pytree per instance — and downstream
scatter-add buffers scale by that.

## The control test

Memory budget per replica is essentially identical between Delaunay
and RectangularAdaptImage on the same instrument (per the
`autolens_profiling/vram/config.py:VMAP_BATCH` probe):

```
("imaging", "delaunay",      "hst"): 16   #  922 MB / replica
("imaging", "pixelization",  "hst"): 16   #  931 MB / replica
```

The same applies on Euclid (64 each) and JWST (8 each). The two
cells differ only in:

- Delaunay: mesh interpolator uses `pure_callback` to call
  `scipy.spatial.Delaunay`.
- RectangularAdaptImage: mesh interpolator is pure JAX —
  `PyAutoArray:autoarray/inversion/mesh/interpolator/rectangular*`
  has zero `pure_callback` calls.

If a single first-class NSS fit at `n_live=150, num_delete=16` runs
to completion on RectangularAdaptImage but OOMs identically on
Delaunay, the difference is the `pure_callback`. A100 jobs 322603
(Nautilus pixelization) + 322604 (NSS pixelization) are queued; the
NSS one is the decisive test.

## Desired fix (if the control confirms it)

Two options, ranked:

1. **JAX-native Delaunay triangulation.** Replace
   `scipy.spatial.Delaunay` with a pure-JAX implementation. The mesh
   has fixed `pixels` count and the triangulation is computed once
   per likelihood eval from the source-plane mesh vertex grid. A
   plane-sweep or incremental Bowyer–Watson implementation in JAX
   exists in research code (e.g. `jax_zero_contour`-style approach
   on the `tomographic-jax` family) — fixed-size output buffers
   match the existing `simplices_padded_shape` etc., so the
   downstream code doesn't change.

2. **Cache the triangulation across vmap instances.** The mesh
   triangulation depends on the *source-plane* vertex positions,
   which differ per particle (the lensed image_plane_mesh_grid is
   ray-traced through that particle's mass model). So *true*
   caching across particles isn't possible — but caching across
   *outer iterations* might be: the source-plane vertex positions
   change slowly for live particles surviving multiple outer
   iterations, so the connectivity *might* be stable enough to
   re-use. Riskier (could quietly degrade convergence) and only
   profiles can confirm whether it actually saves memory.

Path 1 is the proper fix. Both paths require care:
`scipy.spatial.Delaunay` returns variable-size output (number of
simplices depends on point distribution); the current implementation
pads to `max_simplices = 2 * N`. A JAX-native version needs the same
padding contract.

## Test plan

- **Confirm or rule out:** wait for jobs 322603 + 322604 to land.
  If 322604 (NSS pixelization) completes and 322602 (NSS Delaunay,
  already failed) didn't, the `pure_callback` is implicated.
- **Memory analysis:** `jax.jit.lower(...).compile().memory_analysis()`
  on a single-batch (num_delete=1) and a num_delete=16 trace of the
  Delaunay likelihood; compare peak temp size against the same trace
  with the `pure_callback` short-circuited (e.g. by hard-coding a
  fake triangulation). If peak drops by an order of magnitude when
  the callback is removed, the HLO blow-up is real.
- **Unit test:** in `test_autoarray/inversion/mesh/`, the existing
  Delaunay tests must continue to pass on the JAX-native
  implementation (path 1) — bit-identical scatter-add output is
  required since the inversion solution depends on the exact
  mapping matrix.
- **End-to-end:** `autolens_profiling/searches/nss/imaging/delaunay
  × hst × fp64` on A100 must produce a real metric JSON after the
  fix. Compare timing against the Nautilus baseline (84.8 ms/eval).

## Affected callers / interaction surface

- **PyAutoArray Delaunay model in production fits.** Every SLaM
  `source_pix[1]` / `source_pix[2]` phase that uses
  `al.mesh.Delaunay` (i.e. the standard pixelized source phase in
  every modern PyAutoLens pipeline) goes through this `pure_callback`
  on every likelihood eval. If the HLO blow-up reproduces under
  Nautilus too (it likely does, just less dramatically because
  Nautilus's vmap fan-out is `n_batch` not `num_delete × inner_state`),
  the fix benefits both samplers, not just NSS.
- **`af.NSS` on Delaunay/datacube cells.** Currently unusable on A100
  for inversion-heavy lensing without this fix.
- **NUFFT path.** `PyAutoArray:autoarray/operators/transformer.py:380`
  has another `pure_callback` for the interferometer NUFFT. It's
  outside this prompt's scope but is likely the same shape of issue
  for `searches/nss/interferometer/delaunay` / `datacube/delaunay`
  cells when those are eventually profiled.

## Cross-references

- **Companion prompt:** `PyAutoPrompt/autofit/nss_chunked_vmap_for_inversion_heavy_likelihoods.md`
  covers the NSS-side generic chunked-vmap fix. Scenarios A
  (pure_callback root cause) and B (vmap-too-wide independent of
  callback) are mutually exclusive — the pixelization control
  decides which prompt is the real fix and which becomes a defense-
  in-depth followup.
- **Project memory:**
  `feedback_jax_pure_callback_const_fold.md`,
  `feedback_vmap_batch_investigation.md` — both record prior
  lessons on the same `pure_callback` + vmap interaction in this
  code.
- **PyAutoArray source:**
  `autoarray/inversion/mesh/interpolator/delaunay.py:66-94` (the
  callback wrapper); `autoarray/inversion/mappers/mapper_util.py:315`
  (the OOM site).
- **A100 evidence:** jobs 322592, 322596, 322600, 322602 (NSS
  Delaunay OOMs at 27.7 GB); job 322601 (Nautilus Delaunay
  completes at 37.4 GB peak); jobs 322603 + 322604 (pixelization
  control pair, in flight).

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
