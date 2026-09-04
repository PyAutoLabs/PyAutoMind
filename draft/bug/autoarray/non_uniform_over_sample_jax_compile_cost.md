# A non-uniform `over_sample_size` costs several times more JAX compile than a uniform one

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- jax
- hygiene
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Review-minutes: 5
Unattended: ready
Filed: 2026-09-04

Found while fixing autolens_workspace#533 (`scripts/multi_dataset/features/slam/simultaneous.py`
timing out at 1805 s against an 1800 s per-script cap in PyAutoHeart's Release Integrate run
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33847995194).

## The finding

Switching a dataset's `over_sample_size_pixelization` from a uniform `int` to a non-uniform
`Array2D` roughly **triples** the JAX compile time of the likelihood, even when the non-uniform
map evaluates **fewer** sub-pixels than the uniform one it replaces.

The workspace change that triggered it (autolens_workspace#523) replaced the dataset default
(uniform sub-size 4, i.e. 16 sub-pixels everywhere) with
`np.where(source_signal_to_noise > 3.0, 4, 2)` — 16 sub-pixels on the bright source, 4 elsewhere.
Strictly fewer sub-pixels, strictly more compile.

Measured on `simultaneous.py` from a task worktree under the `release` build profile
(`PYAUTO_TEST_MODE=1`, `PYAUTO_SMALL_DATASETS=1` → an 80-pixel mask, `PYAUTO_DISABLE_JAX=0`,
`JAX_ENABLE_X64=True`), the "JAX jit compilation of vectorized (vmap) likelihood function
complete in ..." line per SLaM stage:

| Stage | non-uniform pixelization map | uniform sub-size |
|-------|------------------------------|------------------|
| `source_lp[1]` | 8.6 s | 12.8 s |
| `source_pix[1]` (uniform in both) | 16.0 s | 11.2 s |
| `source_pix[2]` (map first applied) | **38.3 s** | **11.6 s** |
| `light[1]` | 31.6 s | 9.2 s |
| `mass_total[1]` | 34.3 s | 11.9 s |
| `subhalo[1]` | 14.1 s | 7.6 s |
| script total | 706.6 s | 366.3 s |

The within-run contrast is the clean one, because it is immune to machine load: with the map,
`source_pix[1]` → `source_pix[2]` goes 16.0 s → 38.3 s at exactly the stage the map is first
applied; without it, the same pair is 11.2 s → 11.6 s.

## Where it probably lives

`OverSampler.binned_array_2d_from`
(`autoarray/operators/over_sampling/over_sampler.py`) branches on the cached
`sub_is_uniform`:

- uniform → `array.reshape(shape_slim, sub_size[0] ** 2).mean(axis=1)`, one fixed-shape
  reduction;
- non-uniform → `jax.ops.segment_sum(array, self.segment_ids, pixels_in_mask)` twice (values
  and counts), a general scatter over ragged blocks.

The docstring on `sub_is_uniform` notes this is "called once per light profile evaluation, and
therefore many hundreds of times per likelihood evaluation" — so the branch multiplies across
the whole traced likelihood, which is consistent with a compile-time (not runtime) blow-up. The
same file already carries one perf fix in this area (PyAutoArray#507, caching the non-uniform
binning divisor), so the non-uniform path is known to be the expensive one.

Not verified: whether `segment_sum` is the whole story, or whether other non-uniform-only paths
(`sub_pixel_areas`, which is an uncached property with a Python double loop; the border
relocator; `mapping_matrix_over_sampled`, which reads `sub_size[0]` as if the sub-size were
uniform) contribute.

## What to do

1. Isolate the compile cost with a minimal reproducer — one `AnalysisImaging` likelihood, jitted,
   over the same small mask, uniform vs non-uniform `over_sample_size_pixelization` — and confirm
   the branch in `binned_array_2d_from` is what pays.
2. If it is, look for a lowering that keeps the fixed-shape reduction for the non-uniform case:
   the sub-sizes come from a small set (here {2, 4}), so the binning can be expressed as a
   padded/segment-free reduction over `max(sub_size)` blocks with a zero mask, rather than a
   general segment scatter.
3. Check `mapping_matrix_over_sampled`'s `int(self.over_sampler.sub_size[0])`, which reads the
   first pixel's sub-size as though it were the uniform one — harmless today (the imaging
   default is `convolve_over_sample_size_pixelization = 1`) but wrong for an adaptive map.
4. When the compile cost is gone, `autolens_workspace/scripts/multi_dataset/features/slam/simultaneous.py`
   can go back to the adaptive map that every other SLaM pipeline uses; its prose names this
   follow-up.
