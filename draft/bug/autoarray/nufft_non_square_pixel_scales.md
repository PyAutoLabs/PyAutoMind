# TransformerNUFFT ignores non-square pixel_scales (uses pixel_scales[0] for both axes)

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
Themes:
- interferometer
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: glance
Witness: on an all-false (10, 12) mask with pixel_scales (0.5, 0.25), `TransformerNUFFT.visibilities_from` agrees with `TransformerDFT.visibilities_from` to 1e-10 relative (today ~0.8 relative error), or `TransformerNUFFT` raises a clear error on non-square pixel scales.
Review-minutes: 3
Unattended: ready
Lane: any
Source: independent review of the PyAutoArray#707 branch (shift 2026-11-26-pm), PRE-EXISTING on main.

`autoarray/operators/transformer.py` `TransformerNUFFT.__init__` builds `pixel_scale_rad` from `self.grid.pixel_scales[0]`
and uses it for both `self._x` (columns) and `self._y` (rows), so non-square pixels give wrong visibilities, dirty images and
mapping-matrix transforms. Fix: scale `_x` by the x pixel scale (`pixel_scales[1]`) and `_y` by the y pixel scale (and the
origin offset of #707 per axis), or refuse non-square pixel scales; add a NUFFT-vs-DFT parity test on a non-square mask.
