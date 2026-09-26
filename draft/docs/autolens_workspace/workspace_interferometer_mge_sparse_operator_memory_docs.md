# autolens_workspace: interferometer MGE modeling docs claim apply_sparse_operator() makes memory mask-only

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- interferometer
- mge
- docs
Difficulty: easy
Autonomy: supervised
Priority: low
Status: draft
Consequence: glance
Witness: `autolens_workspace/scripts/interferometer/features/multi_gaussian_expansion/modeling.py` (lines ~322-324 today) no longer says MGE memory "depends on the real-space mask alone" with `apply_sparse_operator()`; it states that an MGE-only fit takes the dense NUFFT path (memory scales with the visibility count) until the W~ route for MGE-only fits lands, and the notebook is regenerated.
Review-minutes: 3
Epic: interferometer-likelihood-campaign

Source: autolens_profiling#308, `results/notes/interferometer_mge_breakdown_2026_09.md`.

## Why

The `__VRAM__` section says: "With `apply_sparse_operator()` applied (which now supports
linear light profiles as well as pixelizations) it depends on the real-space mask alone."
PyAutoArray `inversion/inversion/factory.py:202-208` switches the sparse operator off when
every linear object is a func-list, so an MGE-only interferometer fit always takes the dense
path; on the A100 its one-shot transform asks for 65.9 GB at 1M visibilities.

## What

- Correct the paragraph (mixed mapper + MGE does use the sparse operator; MGE-only does not).
- If `interferometer_mge_w_tilde_route_mge_only` ships first, update the text to match the
  new behaviour instead.

<!-- filed from autolens_profiling#308 phase C (PR #312), 2026-09-26 -->
